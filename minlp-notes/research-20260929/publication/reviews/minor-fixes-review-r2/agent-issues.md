# Minor-fixes review, round 2: issues 1–22 (sub-agent A)

Date: 2026-10-03. Scope: the track-report side of the 22 round-1 issues in `reviews/minor-fixes-review-r1.md`, checked against the current files. The lead checks the integration items in `reviews/minor-fixes/summary.md`. All paths are relative to P = `research-20260929/publication/` unless stated otherwise. Line numbers refer to the current files.

Own checks used exact `fractions.Fraction` arithmetic on saved data only. Scripts and logs are in `scratch-issues/`. No scientific script in the main tree was imported or run.

## Per-issue verdicts

| # | verdict | evidence (current file:line) | suggested fix if needed |
|---|---|---|---|
| 1 lnts100 primal display | **resolved** (report side) | `primal/lnts/report.md:83` now limits the "valid upper bounds" statement to lnts50/200/400 and gives 0.5545954011669 → 0.5545954011670. Own check (`scratch-issues/lnts_check.log`): the enclosure upper end exceeds 0.5545954011669 by 1.116e-14, 0.5545954011670 ≥ f_hi, and the other three summary primals are ≥ f_hi. No stale "remain valid upper bounds" wording remains. | — |
| 2 dtoc5 primal display | **resolved** (report side) | `primal/dtoc5-lukvle10/report.md:19` gives 5.38967211918114 → 5.389672119181141 and keeps the dual. The value 5.389672119181141 exceeds the upper end …11404674…8314 (`:13`), and 5.38967211918114 lies below the verifier's lower end …114046742396472… (`:16`). | — |
| 3 water 6.89% | **resolved** | `primal/water-ann-kan/report.md:28` shows 6.90%. The checker asserts each percentage display against the exact ratio (`code/minor_review_check.py:22–26`). Own check (`scratch-issues/water_pct.log`): the ratios are 1.67396, 10.81153, 6.89396, 4.86685 and 5.89469 %, so the displays 1.674, 10.82, 6.90, 4.87 and 5.90 are all upper bounds. `:27` adds 1.68% as the upward two-decimal display for waterno2_06, which is correct. | — |
| 4 chain gap ≤ 1.01e-14 | **resolved** (report side) | `primal/chain/report.md:26` states that the gap cell must change from ≤ 1.0e-14 to ≤ 1.01e-14. This is consistent with `:14`, `:20` and `:32` and with check_r2.log (chain100 1.00276e-14 exact; 1.00575e-14 against the safe display). | — |
| 5 eg name / boxes | **resolved** (report side) | `eg-recheck/report.md` never used "eg_all"; `:28` and `:229` use "1,152,830 processed boxes, 1,114,361 leaves". | — |
| 6 audit slack floor | **resolved, one related stale sentence** | `audit-ir/report.md:63` adds the conservative-choice justification (0/158 screened pairs), which matches r1 Group C. Stale: `audit-ir/report.md:12` still says the "display unit" (half a unit in the coarser of the 10th significant digit and the 8th decimal) "is the coarsest rounding the page display could have applied". That rests on the refuted 10-digit display limit (`:60`). | Replace the second sentence of `:12` with: "This uses the audit's conservative 10th-significant-digit convention (Section 1); pages can show more than 10 significant digits." |
| 7 MINOTAUR cell | **resolved** (report side) | `literature/control/report.md:184` table cell and `:715` response row now describe the separate rules (upper default 100; lower default negative but unknown). | — |
| 8 lnts verifier duals | **resolved** | `primal/lnts/report.md:17` gives rounded-down displays; "full value" is gone. Data: `research-20260929/reviews/open-instances-verification/logs/lnts_verify.json`. The `cert_1e-12.h2` strings come from `mpmath.nstr(h2, 20)` (`v_lnts.py:209`), i.e. at most 20 significant digits rounded to nearest with trailing zeros stripped. So the true h2 is within ½ unit of the 20th digit, and N·h2 is known to within ±5e-20. Each safe display lies below the lower end of that bracket by 2.98e-17 (lnts50), 6.56e-17 (lnts100), 9.50e-17 (lnts200) and 3.64e-17 (lnts400), which is far more than the printing uncertainty. The printed h2 also agrees with h_star·(1−1e-12) from the 25-digit h_star. The claim is therefore rigorous, given that the certificate certifies N·h2 for the 60-digit h2. The old `bound` fields 0.5545954011663566 and 0.5545770161025291 lie above N·h2 by 3.44e-17 and 4.97e-18; the lnts50 and lnts400 fields are valid. Relative gaps to the safe displays are 1.000054e-12, 1.000118e-12, 1.000171e-12 and 1.000066e-12, so 1.01e-12 is the correct upward rounding (`:10–13`). Against certified N·h2 the relative gap is about 1.000000000001e-12, also ≤ 1.01e-12. | — |
| 9 lnts rounding | **resolved** | Own exact values: gaps to the summary duals are 5.7890e-13, 6.1116e-13, 5.8367e-13 and 5.8711e-13, so 5.79/6.12/5.84/5.88e-13 are upward roundings (`:10–13`, `:19`, `:117`). The relative values 1.0437, 1.1020, 1.0525 and 1.0587e-12 give 1.05/1.11/1.06/1.06e-12. Gaps to N·h2 or the safe displays are ≤ 5.5467e-13, so ≤ 5.55e-13 (`:19`, `:84`, `:116`). "approximately 3.25e-15–3.54e-15" is labelled approximate (`:108`, `:127`), and the log gives 3.2546e-15 to 3.5437e-15 ≤ 3.6e-15 (`:25`). "about 1e-12 relative" at `:116` is labelled. No stale 5.5e-13, 5.8e-13 or 6.2e-13 remains. | — |
| 10 lnts argument / files | **partially resolved — new error in the new proof text** | (a) The structure of the argument at `primal/lnts/report.md:57` is now correct: grouping equal \|θ_j\|, the positive coefficients, θ = 0 forcing vy ≡ 0 and hence py_N = 0 ≠ 5, and the need for rational h. However, the constant is wrong. With the weights the report uses (`:38`, tan θ_j = μ + ν c_j/w_j; `lnts_primal.py:162` and `crosscheck.py:57` give w = (1/2, 1, …, 1, 1/2)), the recursion at `:40` gives vx_N = 100h Σ w_j cos θ_j. So the condition is Σ w_j cos θ_j = 45/(100h), as in r1 `primal-lnts-review-r1.md:42`, not 45/(50h). The conclusion is unaffected. (b) The logs are labelled obsolete and the reviewer rerun is identified (`:96`). I verified with `cmp` that all four `scratch-A/lnts_repro/points/*.json` are byte-identical to `points/*.json`. (c) `minor_review_check.py` and its log are listed (`:92`), but the new `logs/review_r2_check.log` (cited in response-r2 row 10 and byte-identical to `minor_review_check.log`) is not in the Section 7 log list (`:94`). | `:57`: "45/(50h)" → "45/(100h)", and define the weights: "with trapezoid weights w_0 = w_N = 1/2 and w_j = 1 otherwise". `:94`: add `review_r2_check.log` (round-2 rerun of `minor_review_check.py`; identical output). |
| 11 chain display list | **resolved** | `primal/chain/report.md:26` lists all five documents plus the reproduction caveat, and describes the COPS verification report as "a bullet list and a table". grep confirms `verification-report.md:35,37` (bullets) and `:193,195` (table), `solver-campaign-review-r1.md:43` and `solver-runs/report.prev.md:39`. | — |
| 12 dtoc5 / powerflow wording | **resolved** | dtoc5 `:127` reworded ("No local or global optimality proof … was attempted"), and no other "local minimizer" statement remains. `:20` reads "The maximum row violation of p5 is 3.48e-15". Powerflow `:44` assigns 4.3e-4 → e215/0030p, 1.08e-3 → e346/0039p and 2.3e-3 → e306/0039r, matching table `:62–64` and r1 `scratch-B/check_powerflow.log:4,9,14` (0.0004304, 0.001082, 0.002293). The 0039r rows e363 (6.8e-13) and e386 (2.1e-13) are stated correctly. | — |
| 13 MINOTAUR rule | **resolved** | Source `literature/control/sources/QuadHandler_master_r2.cpp:184–236`: defaultLb_ starts at 1e12 and is set to the smallest lb in (−1e12, 1e12), then to 100·m if m < −1e-6, −100·m if m > 1e-6, else −1000. The upper default is symmetric (largest finite ub M, then ±100·M or +1000). The computation runs once and is cached. `report.md:296` states this exactly (−100\|m\|, 100\|M\|, ∓1000 for near-zero or no finite bound) and correctly says only the upper default is inferable. The saved log `sources/mittelmann_cnconv/logs/QPLIB_8585.mnt:27–28` shows 99983 lower and 99997 upper warnings. Own check of the saved `sources/qplib/QPLIB_8585.sol` (sha256 9d9f5c4f… matches the log): 99,998 listed x, min x49999 = 1.460728991e-05, max x2 = 8.057243524908399, x50001 = 1, and x1 omitted (zero). This matches `:296`. `:531` and `:698` are corrected. | Optional: `checks/dtoc5_reference_check.log:1` still begins "URL https://…", which reads like a fetch; it now reads the saved file. |
| 14 camshape log / README | **resolved** | `literature/control/checks/qplib_camshape_compare.log` was rewritten 2026-10-03 22:49 (after the script change at 21:32). It shows bound maxima 1.741e-10, 2.420e-10, 4.708e-10 (QPLIB_2703 x1 up) and 2.497e-10 (QPLIB_3177 x1 up), and coefficient maxima 1.306/2.237/2.164/1.218e-10. `checks/README.md:30` says "bound maximum about 4.7e-10; QPLIB_3177 about 2.5e-10", which is consistent. `report.md:172` (2.3e-10 coefficient and 4.7e-10 bound overall) and `:190`/`:697` (1.2e-10 and 2.5e-10) are consistent with the log. | — |
| 15 OPF novelty | **resolved** | `literature/network/report.md:135` now reads "found for this MINLPLib model", consistent with `:30` and `:368`. | — |
| 16 Müller / Göß citations | **resolved (one optional clarification)** | Saved PDF `literature/network/sources/mueller2020_arxiv1903.05521.pdf` (72 pages): Table 5 runs over PDF pp. 60–72. PDF p. 69 has powerflow0030r and 0039r at 1800.0 in all three column pairs, and p. 72 has waterno2_04–24 at 1800.0. PDF pp. 42/48 are "Table 3 continued" and pp. 56/59 are "Table 4 continued". `report.md:114` and `:268` now cite "Table 5, pp. 69 and 72". These are PDF page numbers; the printed page numbers are 67 and 70. Göß: the saved `goss2026_arxiv2603.16505.txt` front matter names one author, Adrian Göß; `:61` and the bibliography `:398` are single-author. No "Göß et al." for arXiv:2603.16505 remains (the "Göß et al." in `literature/small` is the multi-author JOGO paper). | Optional: write "PDF pp. 69 and 72 (printed pp. 67 and 70)" at `:114` and `:268`. |
| 17 SCIP mechanism scope | **partially resolved — new inaccuracy** | `scip-bug/report.md:38` ("In the instrumented seeds (8 and 14)") is correct for pair2236. `:243` now reads "All instrumented cutoffs in Section 5.3 (seeds 8 and 14) involve the 0.7 station". The parenthetical is wrong: the Section 5.3 table (`:210–224`) has 14 instrumented runs on tiny2, pumps_default, fm336, fm318, pair2236, p0, p4 and p5, with seed shifts 0, 2, 3, 8 and 14. Seeds 8 and 14 are only the two pair2236 runs. The section intro (`:206–207`) says every listed run involves an L = 0.7 station, which supports the unparenthesised r1 wording. | `:243`: delete "(seeds 8 and 14)", or write "All instrumented cutoffs in Section 5.3 (14 runs; for pair2236, seeds 8 and 14) involve the 0.7 station". |
| 18 SCIP low claims / binary64 scope | **partially resolved — new error** | `:36` is correct: 56.492 and 65.12 are refuted and 55.69 is not. `:173` (new) says: "For these five examined solutions, the wrong claims are refuted for the exact decimal model …; This does not refute every scanned claim, including the low claims discussed in Section 6." The five solutions (`:169`) are pumps_default, p0 seed 0, tiny2, and pair2236 seeds 0 and 7. Saved logs: `logs/binary64_scip_solution.log:5` shows tiny2 "claimed -1.337", the correct default-settings optimum (`:118`, `:529`), not a wrong claim. `logs/pair_semantics.log:1` shows pair2236 seed 0 "claimed optimum 55.68977300185796", which is exactly one of the low claims Section 6 says are not refuted (`:313`). So only three of the five (pumps_default 1.198, p0 seed 0 169.9503, pair2236 seed 7 65.124) are refuted wrong claims, and the sentence contradicts Section 6. | Replace `:173` with: "Of these five examined solutions, three are refuted wrong claims: pumps_default (1.198), p0 seed 0 (169.9503) and pair2236 seed shift 7 (65.124) lie above exactly feasible witnesses that SCIP itself accepts. tiny2 with default settings returns the correct decimal optimum −1.337, and pair2236 seed 0 returns the low claim 55.689773, which is not refuted (Section 6). All five returned vectors fail exact binary64 feasibility. This was not checked for the other scanned claims." |
| 19 SCIP draft / files | **resolved (minor provenance gap)** | The draft (`:433–564`) contains no `logs/`, `../reviews` or "review r1" references. `:504` reads "Witness acceptance was checked on master, 10.1.0, 10.0.2 and 10.0.3". The tiny2 inequality at `:529` is exact: 1.537/1.6 = 0.960625 and 0.960625² = 0.9228 > 0.8. Section 9 (`:360–361`) lists `minor_review_check.py`, its log, `sources/` and `MANIFEST.md`, and the four sha256 hashes and sizes match. Gap: once the path was removed from the draft, the report body (`:119`, Section 9) no longer cites evidence for the 10.0.2/10.0.3 fm336 acceptance; it exists only in `reviews/scip-bug-r1/rv_runs.log:55–57,155–157`. | Add to the Section 3.2 remark `:119`: "10.0.2 and 10.0.3 acceptance: `../reviews/scip-bug-r1/rv_runs.log`". |
| 20 water status / comment | **resolved (cosmetic)** | `primal/water-ann-kan/report.md:5` acknowledges r1. `code/nn_exact.py:143` now reads "inputs exactly; other variables as rationals or outward intervals {lo, hi}", which matches `:144–151`. `:5` is a comma splice: "…but by the same author, independent review r1 later verified…". | `:5`: "…written separately for waterno2, but by the same author. Independent review r1 later verified the numerical claims with its own code." |
| 21 audit count definitions | **resolved (one residual)** | `audit-ir/report.md:60–62` gives "35 displayed entries (18 distinct strings)", "38 displayed entries", "46 displayed entries", trailing integer zeros counted (−10000000000.), and "Values on three instances … occur in 17 display-tie pairs". All match r1 Group C (`group-C.md:96–111`) and `audit-ir/logs/minor_review_check.log`. Residual: the open-issues bullet `:202` still gives "35 … 38 … or 46" without "displayed entries". | `:202`: "define the counts as displayed entries (not distinct numbers): 35 …". |
| 22 cosmetics + disagreement | **resolved; the author is right on the disagreement** | See below. | Optional: state the gap definition (see below). |

### Issue 22 in detail

- **Disagreement: the author is correct, and the round-1 statement was wrong.** The saved logs `literature/control/sources/mittelmann_cnconv/logs/QPLIB_2738.mnt:2197`, `QPLIB_2480.mnt:2195` and `QPLIB_2703.mnt:2183` print `mntr-glob: gap percentage = 5.9096`, `= 13.3380` and `= 20.8425`. The preceding lines print the absolute gaps (0.2532, 0.5707, 0.8913), best solution values (−4.2842, −4.2787, −4.2765) and remaining-node bounds (−4.5374, −4.8494, −5.1678).
  - **Definition.** From those printed values, gap/\|best solution value\| × 100 = 5.9101, 13.3382 and 20.8418, while gap/\|bound\| × 100 = 5.58, 11.77 and 17.25. The printed percentage is therefore the gap relative to the incumbent (primal) value. The small differences come from the 4-decimal display of the inputs.
  - **Report text.** `literature/control/report.md:191` quotes "printed gap percentages 5.9096%, 13.3380% and 20.8425% (about 5.9%, 13.3% and 20.8%)", and the bounds −4.5374/−4.8494/−5.1678 match. This is correct.
  - **Optional fix.** Add "(MINOTAUR's gap relative to \|incumbent\|)". The same report quotes SCIP gaps under SCIP's definition at `:356`.
- **Blank line before `## Response to review`:** present (`literature/control/report.md:705`).
- **QPLIB_3177 scales:** "about 1.2e-10 for coefficients and 2.5e-10 for bounds" at `:190` and `:697`, which matches the log's 1.218e-10 and 2.497e-10.
- **`report.prev.md`:** line 1 now reads "Historical round-0 copy. Superseded by [report.md](report.md)".
- **VSDP URL:** both `literature/network/report.md:362` and `:403` use https://www.tuhh.de/ti3/jansson/vsdp_cj.html.
- **Network checker:** `:316` (in Section 7) lists `minor_review_check.py` and its log.
- **R3_H1_N4:** `:169` and `:514` say "the checked Default R3_H1_N4.log".
- **arXiv v2 Table 4:** `:74` reads "as in arXiv v2 Table 4" and "In arXiv v2 no method converged in 1e5 s". The saved `schweidtmann2019_arxiv1801.07114.txt` shows "arXiv:1801.07114v2" at line 14, Table 4 at line 1415 (794 variables at line 1419) and "none of the tested solution approaches con[verged]" at line 1435.
- **eg tree-free citation:** `eg-recheck/report.md:23` cites `../reviews/eg-recheck-r1/own_cover.py` and `logs/own_cover.log`. Both exist; the log prints "COVERAGE PROVED" and per-part leaves summing to 1,114,361.

## New problems in round-2 text (summary)

1. `primal/lnts/report.md:57`: "Σ w_j cos θ_j = 45/(50h)" should be 45/(100h) for the trapezoid weights w = (1/2, 1, …, 1/2) the report uses (`:38`; `lnts_primal.py:162`). The weights are also undefined in the sentence. The conclusion is unaffected.
2. `scip-bug/report.md:243`: the parenthetical "(seeds 8 and 14)" mislabels the 14 instrumented runs of Section 5.3, which use seed shifts 0, 2, 3, 8 and 14 on eight models.
3. `scip-bug/report.md:173`: says the claims of all "five examined solutions" are refuted wrong claims. tiny2's −1.337 is the correct optimum, and pair2236 seed 0's 55.689773 is a Section 6 low claim that is not refuted. The sentence contradicts `:313`.
4. `primal/lnts/report.md:94`: the Section 7 log list omits the new `logs/review_r2_check.log`.
5. `scip-bug/report.md:504` together with Section 9: after the evidence path was removed from the draft, nothing in the report body points to the 10.0.2/10.0.3 fm336 acceptance evidence (`reviews/scip-bug-r1/rv_runs.log`).
6. `primal/water-ann-kan/report.md:5`: comma splice (cosmetic).
7. Pre-existing but related to issue 6: `audit-ir/report.md:12`, "This is the coarsest rounding the page display could have applied", is stale after the 10-digit limit was refuted.
8. Residual for issue 21: `audit-ir/report.md:202` lacks "displayed entries".
9. Optional:
   - `literature/control/report.md:191`: add the MINOTAUR gap definition (relative to \|incumbent\|).
   - `literature/network/report.md:114` and `:268`: say "PDF pp." (printed 67 and 70).
   - `literature/control/checks/dtoc5_reference_check.log:1`: the "URL" label now describes a local read.
   - `literature/network/report.md:276–280`: the waterno2 gap displays 1.67%, 10.8% and 6.9% are rounded to nearest (exact 1.674%, 10.81%, 6.894%). This is not an error, because that table makes no upward-rounding claim, but it differs from the upward convention adopted in the water report.

All round-2 relative links in the ten "Round 2" sections resolve, checked by a shell loop over every `](…)` target.

## Commands run

All commands were read-only on the main tree. Scratch output is in `reviews/minor-fixes-review-r2/scratch-issues/`. There was at most one process at a time, with OMP_NUM_THREADS=1 where Python was used.

```sh
P=/workspace/minlp-notes/research-20260929/publication
ls $P/reviews/ $P/reviews/minor-fixes/ $P/reviews/minor-fixes/before-r2/ $P/reviews/minor-fixes-review-r2/; wc -l $P/reviews/minor-fixes-review-r1.md $P/reviews/minor-fixes/response-r2.md
cat $P/reviews/minor-fixes-review-r1.md; ls -R $P/reviews/minor-fixes-review-r2/; cat $P/reviews/minor-fixes-review-r2/PROGRESS.json
cat $P/reviews/minor-fixes/response-r2.md; wc -l $P/reviews/minor-fixes/report_changes_r2.patch
mkdir -p $P/reviews/minor-fixes-review-r2/scratch-issues; cat -n $P/primal/lnts/report.md
cd research-20260929; ls -la reviews/open-instances-verification/logs/lnts_verify.json; python3 -c "import json;...print(json.dumps(d,indent=1)[:4000])"
ls reviews/open-instances-verification/ reviews/open-instances-verification/logs; grep -rln "cert_1e-12\|sup_margin" reviews/open-instances-verification --include=*.py
cat -n reviews/open-instances-verification/v_lnts.py
cat primal/lnts/logs/minor_review_check.log; ls primal/lnts/logs/; cat primal/lnts/logs/review_r2_check.log
# own script scratch-issues/lnts_check.py (reads lnts_verify.json and points/*.json only)
cd scratch-issues && OMP_NUM_THREADS=1 python3 lnts_check.py 2>&1 | tee lnts_check.log
grep -n "full value\|5545954011663566\|...\|1\.0e-12" primal/lnts/report.md; diff reviews/minor-fixes/before-r2/primal__lnts__report.md primal/lnts/report.md
grep -n -i "lindemann\|linear.*independ\|45/" reviews/primal-lnts-review-r1.md; grep -rn "w_j\|weights" primal/lnts/report.md
grep -n "Fr(1, 2)\|def weights\|w = \[" primal/lnts/*.py
ls reviews/minor-fixes-review-r1/scratch-A/lnts_repro/ ...; for N in 50 100 200 400; do cmp <repro point> primal/lnts/points/lnts${N}_point.json; done
cmp primal/lnts/logs/review_r2_check.log primal/lnts/logs/minor_review_check.log; ls -l --time-style=full-iso primal/lnts/logs/ primal/lnts/minor_review_check.py; grep -rn "review_r2_check" primal/lnts/ reviews/minor-fixes/commands.md reviews/minor-fixes/response-r2.md
diff reviews/minor-fixes/before-r2/primal__dtoc5-lukvle10__report.md primal/dtoc5-lukvle10/report.md; grep -n "5\.3896721191811\|local minimi\|KKT point is\|row violation\|3\.48e-15" primal/dtoc5-lukvle10/report.md
sed -n 5,17p primal/dtoc5-lukvle10/report.md; grep -n "local minim\|minimizer" primal/dtoc5-lukvle10/report.md
grep -rn "3\.48\|row_viol\|rowviol\|max row" primal/dtoc5-lukvle10/logs/; grep -n "p5" primal/dtoc5-lukvle10/report.md
diff reviews/minor-fixes/before-r2/primal__powerflow__report.md primal/powerflow/report.md; grep -n "e215\|e346\|e306\|e363\|e386\|4\.3e-4\|1\.08e-3\|2\.3e-3" primal/powerflow/report.md
wc -l reviews/minor-fixes/check_r2.log; grep -n -i "powerflow\|e215\|..." reviews/minor-fixes/check_r2.log; ls reviews/minor-fixes-review-r1/; grep -n "e215\|e346\|e306" reviews/minor-fixes-review-r1/scratch-B/*.log
diff before-r2 water report/nn_exact.py/minor_review_check.py vs current; grep -n "6\.89\|independently reviewed\|upper bound\|Rounding" primal/water-ann-kan/report.md
sed -n 7,30p primal/water-ann-kan/report.md; ls primal/water-ann-kan/logs; cat primal/water-ann-kan/logs/minor_review_check.log
# own script scratch-issues/water_pct.py (report table values only)
python3 water_pct.py | tee water_pct.log
grep -n -i "independent" primal/water-ann-kan/report.md; grep -n "centre and radius\|centre, radius\|mid, rad" primal/water-ann-kan/code/*.py primal/water-ann-kan/report.md
sed -n 135,165p primal/water-ann-kan/code/nn_exact.py
diff reviews/minor-fixes/before-r2/primal__chain__report.md primal/chain/report.md; grep -n "1\.0e-14\|1\.01e-14\|two tables\|bullet list" primal/chain/report.md
cd research-20260929; for f in <5 docs>; do grep -n "5\.072261493982863\|5\.068917341793162" $f; done; grep -rln "5\.072261493982863\|5\.068917341793162" --include=*.md .
diff reviews/minor-fixes/before-r2/eg-recheck__report.md eg-recheck/report.md; grep -n "eg_all\|processed-leaf\|processed leaf\|1,152,830\|1,114,361" eg-recheck/report.md
ls reviews/eg-recheck-r1; ls reviews/eg-recheck-r1/logs; grep -n -i "COVERAGE\|guillotine" reviews/eg-recheck-r1/logs/own_cover.log; grep -n -i guillotine reviews/eg-recheck-r1/own_cover.py
diff reviews/minor-fixes/before-r2/audit-ir__report.md audit-ir/report.md
cat audit-ir/logs/minor_review_check.log; ls reviews/minor-fixes-review-r1/scratch-C/; grep -n -i "tie\|17\|distinct\|46\|floor" reviews/minor-fixes-review-r1/group-C.md
grep -n "\b35\b\|\b38\b\|\b46\b\|three are in\|display ties\|slack floor\|10th" audit-ir/report.md; sed -n 8,20p; sed -n 52,66p; sed -n 196,206p audit-ir/report.md
diff reviews/minor-fixes/before-r2/scip-bug__report.md scip-bug/report.md
sed -n 28,48p scip-bug/report.md; grep -n "56\.49\|55\.69\|65\.12\|real error\|tolerance effect" scip-bug/report.md; ls scip-bug/sources scip-bug/logs
grep -n "^#" scip-bug/report.md; sed -n 205,246p scip-bug/report.md; sed -n 155,175p scip-bug/report.md
cat scip-bug/logs/pair_semantics.log; grep -n -i "seed\|obj\|claim\|viol" scip-bug/logs/binary64_scip_solution.log
sed -n 100,150p scip-bug/report.md; grep -n "tiny2" scip-bug/report.md
awk 'NR>=431 && NR<=564' scip-bug/report.md | grep -n -i "logs/\|review\|\.\./\|minor_review\|r1\b\|author"; sed -n 355,383p scip-bug/report.md; cat scip-bug/sources/MANIFEST.md
sha256sum scip-bug/sources/*.json; wc -c scip-bug/sources/*.json
grep -n "rv_runs\|10\.0\.3.*accept\|accept.*10\.0\.3" scip-bug/report.md; sed -n 498,506p scip-bug/report.md; head -12 scip-bug/logs/checksol_witness.log
ls reviews/scip-bug-r1; grep -n "6.925926e-01\|10\.0\.[23]\|solution candidate storage" reviews/scip-bug-r1/rv_runs.log; grep -n "^==" reviews/scip-bug-r1/rv_runs.log | grep -i "sol\|witness\|read"
diff reviews/minor-fixes/before-r2/literature__control__report.md literature/control/report.md
find literature/control -iname "*QuadHandler*" -o -iname "QPLIB_2738*" -o -iname "QPLIB_2480*" -o -iname "QPLIB_2703*" -o -iname "*8585*"
ls literature/control/sources/mittelmann_cnconv/logs; wc -l QPLIB_{2738,2480,2703}.mnt
sed -n 2170,2201p QPLIB_2738.mnt; sed -n 2180,2199p QPLIB_2480.mnt; sed -n 2165,2187p QPLIB_2703.mnt
grep -n "gap percentage" QPLIB_2738.mnt QPLIB_2480.mnt QPLIB_2703.mnt QPLIB_3177.mnt QPLIB_8585.mnt; python3 -c "<gap/|ub| and gap/|lb| from printed values>"; head -5 QPLIB_2738.mnt; grep -n -i gap literature/control/report.md | grep ...
grep -n addDefaultBounds literature/control/sources/QuadHandler_master_r2.cpp; sed -n 184,264p QuadHandler_master_r2.cpp
grep -n "defaultLb_\|defaultUb_" QuadHandler_master_r2.cpp; grep -n "aTol_(" QuadHandler_master_r2.cpp; sed -n 715,740p; sed -n 785,805p QuadHandler_master_r2.cpp
grep -n -i default literature/control/sources/mittelmann_cnconv/logs/QPLIB_8585.mnt; ls literature/control/checks; cat checks/dtoc5_reference_check.log; diff before-r2 dtoc5_reference_check.log current
diff before-r2 dtoc5_reference_check.py current; head -5 literature/control/sources/qplib/QPLIB_8585.sol; sha256sum literature/control/sources/qplib/QPLIB_8585.sol
# own script scratch-issues/dtoc5_ref.py (reads the saved QPLIB_8585.sol)
python3 dtoc5_ref.py | tee dtoc5_ref.log
grep -n "100, 100\|100,100\|largest.*bound magnitude\|largest applicable\|max |x|" literature/control/report.md checks/README.md; grep -n "2e-10\|2\.5e-10\|4\.7e-10\|1\.2e-10" literature/control/report.md checks/README.md
ls -l --time-style=full-iso checks/qplib_camshape_compare.*; cat checks/qplib_camshape_compare.log; sed -n 20,40p checks/README.md; diff before-r2 README current
diff before-r2 qplib_camshape_compare.log current; grep -n "8\.921e-11\|..." literature/control/report.md
sed -n 168,194p literature/control/report.md
grep -n -B2 "^## Response to review" literature/control/report.md; head -5 literature/control/report.prev.md; diff before-r2 report.prev.md current; grep -rn report.prev.md literature/control/report.md checks/README.md
grep -rn "5\.5e-13\|5\.55e-13\|6\.89%\|1\.0e-14\|5\.9%\|13\.3%\|20\.8%\|Göß et al\|Goss et al" literature/control/report.md literature/network/report.md
sed -n 274,284p literature/network/report.md; diff before-r2 network report current
ls literature/network/sources; find literature -iname "*1903.05521*" -o -iname "*muller*" -o -iname "*mueller*"
for p in 42 48 56 59 69 72; do pdftotext -f $p -l $p -layout .../mueller2020_arxiv1903.05521.pdf scratch-issues/mueller_p$p.txt; grep -n -i "^ *Table\|time limit\|powerflow00[34]\|waterno2_..." mueller_p$p.txt; done
grep -n waterno2 mueller_p48.txt mueller_p59.txt mueller_p72.txt; pdfinfo ... | grep Pages; for p in 60..75: pdftotext ... | grep -q "Table 5"; pdftotext -f 60 -l 75 ... | grep -n "^ *Table 5"
tail -5 mueller_p69.txt; tail -3 mueller_p72.txt; pdftotext -f 60 -l 60 ... | sed -n 1,14p; head -15 literature/network/sources/goss2026_arxiv2603.16505.txt
grep -rn "Göß et al\|Goß et al\|Göss et al\|Goess et al" --include=*.md literature; grep -n "pp\. 42\|42,48\|56,59" literature/network/report.md; grep -n vsdp literature/network/report.md
sed -n 403p literature/network/report.md; grep -n tuhh ...; grep -n "R3_H1_N4\|Default log" literature/network/report.md; ls literature/network/checks
awk '<section of line 316>' literature/network/report.md; grep -n "1801.07114v\|Table 4\|794" literature/network/sources/schweidtmann2019_arxiv1801.07114.txt
grep -n "first rigorous" literature/network/report.md
for r in <10 tracks>; do awk '/### Round 2/{p=1} p' $r/report.md | grep -o '](...)' | while read l; do [ -e "$r/$l" ] || echo BROKEN; done; done   # no broken links
sed -n 1,20p; sed -n 29,78p; sed -n 81,90p reviews/minor-fixes/check_r2.log
grep -rln "gap percentage" literature/control/sources | grep -v .mnt; grep -n "gap percentage\|gap = " QPLIB_3177.mnt
ls reviews/minor-fixes/before; grep -n "coarsest rounding" reviews/minor-fixes/before/*audit* reviews/minor-fixes/before-r2/audit-ir__report.md
grep -n "Göß\|Goess\|Göss" literature/network/report.md literature/control/report.md
```

These are local targeted checks only, separate from CI.
