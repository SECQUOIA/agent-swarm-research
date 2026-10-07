Verdict: issues

# Review of the minor-fixes work, round 2

Reviewer: independent verifier. Date: 2026-10-03. Scope: the round-2 resolutions of the 22 issues in [minor-fixes-review-r1.md](minor-fixes-review-r1.md), the 40 exact integration replacements in [minor-fixes/summary.md](minor-fixes/summary.md) (machine-readable copy: `minor-fixes/integration-r2.json`), a scan of the whole `open-instances-summary.md`, and collateral damage from the round-2 edits. Paths are relative to `research-20260929/publication/` unless they start with `research-20260929/` or are bare top-level names such as `open-instances-summary.md` (relative to `research-20260929/`). Evidence is in [minor-fixes-review-r2/](minor-fixes-review-r2/): `scratch/` (lead), `agent-issues.md` with `scratch-issues/` (issues 1–22), and `agent-collateral.md` with `scratch-collateral/` (collateral damage).

## Summary

**The 40 integration replacements are correct.** This was the highest-priority check.
- **Old strings.** Each of the 40 old strings occurs in its current target file exactly as written: once in 36 cases, and twice in each of the four cops-report and verification-report items, which say "apply to every occurrence". Applied in order to scratch copies, all 40 succeed. `summary.md` and `integration-r2.json` agree block for block.
- **New displays.** My own exact computation checked every new number against the saved point or certificate:
  - Every new primal display is an upper bound on the exact point objective, or on the upper end of its enclosure (minimization). Where I checked, it is the minimal upward rounding at the shown precision.
  - Every dual display is at or below the certificate.
  - Every changed gap is at least the exact gap and is rounded up.
- **Old displays.** The replaced primal displays (lnts100, dtoc5, ex6_2_5, powerflow0039p/0039r, eg_int_s, eg_disc_s, waterno2_06/12/24, ann_cumene_tanh) are indeed below the point objective.
- **Objectives recomputed independently.** I recomputed the dtoc5 objective and all five waterno2 objectives from the OSIL models and the stored exact points. They equal the stored exact rationals.
- **Prose and audit edits.** The facts in the prose and audit replacements match the track reports and saved logs:
  - eg_disc2_s: 1,114,361 leaves under A1/A2, and the 10,404-leaf interval sample in parts 0 and 2–7;
  - ann_cumene_tanh: the identical exp twin was closed in floating point;
  - the 13 formerly tolerance-only instances;
  - the audit counts 35/38/46 with 18 distinct strings, the slack floor affecting 0 of 158 screened pairs, and 17 tie pairs on three instances;
  - the five spring (i-r) pairs.

**The 22 round-1 issues.**
- 15 are fully resolved, and 3 more are resolved apart from optional notes.
- 4 are only partly resolved. The round-2 text for issues 10, 17 and 18 introduces new errors, and one sentence for issue 21 still lacks the new count definition.
- **Issue 22 disagreement: the author is right.** The saved MINOTAUR logs print `gap percentage = 5.9096`, `13.3380` and `20.8425`. These values are the absolute gap divided by |incumbent|.

**Collateral damage.** None of substance.
- All 58 round-2 hunks were classified. 57 are explained by an issue or a response note; the remaining one is a harmless trailing-space removal.
- The recorded round-2 patch reproduces the current files byte for byte.
- The two protected files are unchanged: their hashes match `protected-r2.json` and git HEAD.
- No tracked log was truncated.
- One rewritten log is missing from `FILES-r2.json`.

**Summary scan.** There are no invalid primal or dual displays outside the list. The problems are a mixed gap-rounding convention, which the list makes visible, and three small display or wording problems that predate this work.

There are no blockers, 1 major issue and 10 minor issues.

## Issues

### Major

1. **scip-bug: the new sentence for issue 18 overstates the five examined solutions** (major)
   - **Location:** `scip-bug/report.md:173`.
   - **Evidence:**
     - The sentence reads: "For these five examined solutions, the wrong claims are refuted for the exact decimal model and under SCIP's tolerance-based feasibility checks".
     - The five solutions (`:169`) are pumps_default, p0 seed 0, tiny2, and pair2236 seeds 0 and 7. Two of them do not fit:
       - `logs/binary64_scip_solution.log:5` shows tiny2 "claimed -1.337". That is the correct optimum (`:118`, `:529`), not a wrong claim.
       - `logs/pair_semantics.log:1` shows pair2236 seed 0 "claimed optimum 55.68977300185796". Section 6 (`:313`) and the round-2 fix for issue 3 say this low claim is not refuted.
     - Only three of the five are refuted wrong claims. The sentence contradicts Section 6 of the same report, in a document meant to support an upstream bug report.
   - **Fix:** replace the sentence with:
     > Of these five examined solutions, three are refuted wrong claims: pumps_default (1.198), p0 seed 0 (169.9503) and pair2236 seed shift 7 (65.124) lie above exactly feasible witnesses that SCIP itself accepts. tiny2 with default settings returns the correct decimal optimum −1.337, and pair2236 seed 0 returns the low claim 55.689773, which is not refuted (Section 6). All five returned vectors fail exact binary64 feasibility; this was not checked for the other scanned claims.

### Minor

2. **Integration list: the waterno2_06 gap now disagrees with the text, and gap rounding is mixed** (minor)
   - **Location:**
     - `open-instances-summary.md:82` ("278.230573774 (gap 1.67%)") and `:186` ("1.67%), and a finite dual …");
     - replacement items 16, 18, 20, 22, 24 and 28 in `minor-fixes/summary.md`.
   - **Evidence:**
     - The list changes the table cell to "1.68%" (exact gap 1.6739582%) but leaves the two prose mentions at 1.67%.
     - The same cell keeps "7.26%" for the wave-2 dual. Its exact value is 7.26219%, so this display is rounded to nearest, while 1.68% next to it is rounded up.
     - Other cells that the list leaves alone are also rounded to nearest:

       | cell | display | exact value |
       |---|---|---|
       | lukvle10 | 1.4e-9 | 1.41717e-9 |
       | ex6_2_7 | 4.8e-14 | 4.81819e-14 |
       | powerflow0030p | 2.0e-9 rel. | 2.03083e-9 |
       | powerflow0039p | 6.3e-10 rel. | 6.32211e-10 |
       | pricing050 | 1.0e-17 | 1.041e-17 (verifier's log) |
       | ann_cumene_tanh, under its stated /\|primal\| convention | 0.194% | 0.19402% |
       | ann_cumene_tanh, wave-3 gap | 19% | 19.07% |
       | ann_cumene_tanh, wave-3 gap under the waterno2 convention | 16.0% | 16.015% |

     - The new display-convention sentence (item 28) covers dual and primal displays but not gaps. After integration the table will mix upward-rounded gaps (lnts, chain, waterno2) and nearest-rounded gaps without saying so.
     - No gap cell is false as an approximate size.
   - **Fix:**
     - Add two exact edits:
       - "refined further: 278.230573774 (gap 1.67%)." → "refined further: 278.230573774 (gap 1.68%)."
       - "1.67%), and a finite dual for ann_cumene_tanh" → "1.68%), and a finite dual for ann_cumene_tanh".
     - Change "1.68% (3.78%; 7.26%)" to "1.68% (3.78%; 7.27%)".
     - Append to the item-28 new text: "Gap cells marked ≤ and the lnts, chain and waterno2 gaps are rounded up; other gap cells are rounded to nearest."
     - Alternatively, round all of the cells in the table above upward: 1.5e-9, 4.9e-14, 2.1e-9, 6.4e-10, 1.1e-17, 0.195%, 20% and 16.1%.

3. **Integration list: edits to older documents leave stale numbers, and the matching lnts displays are not corrected** (minor)
   - **Location:**
     - `research-20260929/open-instances-wave2/cops/report.md:19, :21`;
     - `research-20260929/reviews/cops-verification/verification-report.md:18–20, :209–210`;
     - `research-20260929/reviews/closing-audit-a.md:138`.
   - **Evidence:**
     - **Stale gap cells (items 34 and 35).** The chain50 and chain200 rows of the cops summary table will read primal 5.0722614939828724, dual 5.0722614939828627, gap 9.4e-15 (and 5.0689173417931710, 5.0689173417931616, 9.0e-15). The gaps were computed against the old displays. Against the new displays they are 9.7e-15 and 9.4e-15.
     - **Stale sentence.** `verification-report.md:209–210` ("The resulting gaps are 9.4e-15, 9.9e-15, 9.0e-15 and 1.0e-14, as claimed") depends on the old displays.
     - **lnts displays not corrected.** The list corrects every older chain display but not the analogous lnts displays (round-1 issue 8):
       - `verification-report.md:18–19` and `closing-audit-a.md:138` still call 0.5545954011663566 and 0.5545770161025291 certified. They lie 3.44e-17 and 4.96e-18 above N·h2.
       - In the same table, the 1e-10-margin values 0.554577016047626 (lnts200) and 0.5545724136452299 (lnts400) lie 2.96e-17 and 3.26e-17 above their N·h2.
   - **Fix:**
     - Extend items 34 and 35 so that the cops-table gap cells read 9.7e-15 (chain50) and 9.4e-15 (chain200).
     - Add "(against the original binary64 displays)" after "as claimed" at `verification-report.md:210`.
     - Add exact edits:
       - 0.5545954011663566 → 0.5545954011663565 in `verification-report.md` and `closing-audit-a.md`;
       - 0.5545770161025291 → 0.5545770161025290 and 0.554577016047626 → 0.5545770160476259 in `verification-report.md`;
       - 0.5545724136452299 → 0.5545724136452298 in `verification-report.md`.
     - Alternatively, state in the paper that only the main summary displays are authoritative.

4. **Integration list: "A1/A2" is undefined in the summary and qualifies only eg_disc2_s** (minor)
   - **Location:** items 14 and 29 (`open-instances-summary.md:41, :180`).
   - **Evidence:**
     - The summary never defines A1/A2. They are the certifier's hand-checked float-padding analysis and its sampled exp-accuracy assumption (`eg-recheck/report.md:119–120`).
     - `eg-recheck/report.md:225` and `research-20260929/reviews/eg-retry-review.md:21–23` say the eg_int_s and eg_disc_s certificates rest on the same assumptions. Yet their rows will read "verified (all leaves …)" with no qualifier, which suggests they need no such assumptions.
   - **Fix:**
     - In item 14, write "verified on all 1,114,361 leaves under the certifier's floating-point assumptions A1/A2 ([eg recheck](publication/eg-recheck/report.md)); …".
     - Add an edit that appends ", under the same assumptions" to the eg_int_s and eg_disc_s verification cells.

5. **Integration list: the added spring sentence has no antecedent in the audit report** (minor)
   - **Location:** item 33 (`research-20260929/bound-audit/audit-report.md`, after line 652).
   - **Evidence:**
     - "The spring SCIP objective difference of about 1e-9" refers to the audit-ir track's SCIP 10 re-evaluation of the spring proof point (`audit-ir/report.md:125`). The audit report contains no such evaluation.
     - Placed under the bullet about MINLPLib's listed SCIP entries, the sentence reads as if a listed SCIP value differed by 1e-9.
   - **Fix:** in the item-33 new text, replace the last sentence with: "In the separate audit-ir recheck, SCIP 10's evaluation of the spring proof point's objective differs by 1.0e-9 from the exact value; this comes from bisection at SCIP's 1e-9 feasibility tolerance and is not an objective disagreement." Alternatively, drop the sentence.

6. **Summary scan: three small display and wording problems that predate this work** (minor)
   - **Location and evidence:**
     - **`open-instances-summary.md:52`, the KAN row "(listed 0.3606 → 0.0693 for n8)".** The kan_r5_h1_n8 point objective is 0.0693278606…, so 0.0693 is rounded down. After item 28 states that "Numeric primal bounds are rounded upward for minimization", this display contradicts the stated convention.
     - **`:27`, "293.87607509587509 (exact value of the certificate)".** The certificate value is 293.87607509587509237940 (`research-20260929/reviews/bangbang-verification/logs/qcal_exact.json`). The display is a valid rounded-down bound, but it is not the exact value.
     - **`:119`, "at least 1.42e-5 absolute, 1.4e-6 relative".** The proven lower bound on the relative difference is 1.4201e-5/10.40175 = 1.365e-6, so "at least 1.4e-6" overstates it.
   - **Fix:** add exact edits:
     - "0.0693 for n8" → "0.0694 for n8";
     - "(exact value of the certificate)" → "(certificate value rounded down)";
     - "1.4e-6 relative" → "1.36e-6 relative".

7. **primal/lnts: wrong constant in the new rational-point proof, and the file list is incomplete** (minor; issue 10)
   - **Location:** `primal/lnts/report.md:57` and `:94`.
   - **Evidence:**
     - The proof says Σ w_j cos θ_j = 45/(50h). With the weights (1/2, 1, …, 1, 1/2) (`lnts_primal.py:162`) and the constant A = 100 (`:44`), the terminal row is 100·h·Σ w_j cos θ_j = 45, so the value is 45/(100h). That matches the cited r1 review (`reviews/primal-lnts-review-r1.md:42`).
     - The weights are not defined in the sentence. The argument's structure is otherwise correct.
     - The Files list omits the new `logs/review_r2_check.log`.
   - **Fix:** write "Σ w_j cos θ_j = 45/(100h), with trapezoid weights w = (1/2, 1, …, 1, 1/2)". List `logs/review_r2_check.log`.

8. **scip-bug: wrong scope in the restricted mechanism sentence, and the fm336 witness evidence is no longer cited** (minor; issues 17 and 19)
   - **Location:** `scip-bug/report.md:243` and `:119`.
   - **Evidence:**
     - **Line 243** reads "All instrumented cutoffs in Section 5.3 (seeds 8 and 14)". The Section 5.3 table (`:210–224`) has 14 instrumented runs on eight models with seed shifts 0, 2, 3, 8 and 14; seeds 8 and 14 are only the two pair2236 runs. Line 38 is correct.
     - **The fm336 witness evidence.** Removing internal paths from the draft (issue 19) was correct. But the report body now cites no evidence that the fm336 witness is accepted on 10.0.2 and 10.0.3. That evidence is only in `reviews/scip-bug-r1/rv_runs.log:55–57, 155–157`.
   - **Fix:**
     - Delete "(seeds 8 and 14)" at `:243`.
     - In the body remark at `:119` (not in the draft), add "(10.0.2/10.0.3 acceptance: `../reviews/scip-bug-r1/rv_runs.log`)".

9. **audit-ir: two sentences still lack the round-2 wording** (minor; issues 6 and 21)
   - **Location:** `audit-ir/report.md:13` and `:202`.
   - **Evidence:**
     - Line 13 says the 10th-digit display unit "is the coarsest rounding the page display could have applied". Line 60 and the new round-2 text say that no 10-significant-digit display limit exists.
     - Line 202 gives "35 … 38 … or 46" without "displayed entries".
   - **Fix:**
     - At `:13`, replace the second sentence with "The 10th-digit floor is a conservative choice; it changes no screened pair (Section 1)."
     - At `:202`, write "define the counts as displayed entries (35 …)".

10. **primal/water-ann-kan and primal/chain: wording** (minor)
    - **Location:** `primal/water-ann-kan/report.md:5, :27` and `primal/chain/report.md:26`.
    - **Evidence:**
      - **Water, line 5:** comma splice ("…by the same author, independent review r1 later verified…").
      - **Water, line 27:** ends with a dangling clause ("…display, now measured against an exactly feasible point.").
      - **Chain, line 26:** implies that both rounded values occur in all five documents. `closing-audit-a.md`, `solver-campaign-review-r1.md` and `solver-runs/report.prev.md` contain only the chain50 value. The integration list itself is correct.
    - **Fix:**
      - Line 5: "…by the same author. Independent review r1 later verified…".
      - Line 27: "Use 1.68% for an upward two-decimal display; the gap is measured against an exactly feasible point."
      - Chain line 26: add "(chain200's value only in the first two)".

11. **Record keeping** (minor)
    - **Evidence:**
      - `FILES-r2.json` omits `primal/water-ann-kan/logs/minor_review_check.log`, which round 2 rewrote at 22:49:56. Its content matches the round-1 review's values.
      - Two round-2 edits are missing from both the track response tables and `response-r2.md`: `literature/control/report.md:36, :272` (5.5e-13 → ≤ 5.55e-13) and `primal/water-ann-kan/report.md:27` (1.67% → 1.68%). Both edits are numerically correct.
      - `commands-r2.json` omits the final `check_r2.py` rerun at 22:54, and `commands.md` was edited after the recorded patch.
      - The round-1 patch `minor-fixes/report_changes.patch:801–827` is malformed: the last hunk's line count is off by one, and GNU `patch` rejects it.
      - From round 1, unescaped `|` characters break the table rows at `primal/lnts/report.md:129` (`|control|`) and `primal/powerflow/report.md:158` (`||I − C J(X)||∞`).
      - `literature/control/checks/dtoc5_reference_check.py` prints the 99,997/99,983/14 conclusion as fixed text instead of computing it. I confirmed the values independently.
    - **Fix:**
      - Add the log to `FILES-r2.json`.
      - Add the two edits to the response tables.
      - Record the rerun in `commands-r2.json`.
      - Regenerate `report_changes.patch`.
      - Escape the pipes as `\|`.
      - Compute and print the counts in the checker.

## The 22 round-1 issues

| # | result | evidence (current files) |
|---|---|---|
| 1 | resolved | `primal/lnts/report.md:83` is restricted correctly. lnts100: 0.5545954011670 ≥ f_hi = 0.55459540116691116100178 (+8.9e-14), the minimal 13-decimal upward rounding (item 2). |
| 2 | resolved | dtoc5 primal 5.389672119181141 ≥ f = 5.3896721191811404674239664991… (own recomputation from the OSIL and the point equals the stored rational). The dual 5.38967211918114 ≤ the verifier's lower end …1140467423964723… |
| 3 | resolved | water `:28` gives 6.90%; the exact value is 6.8939570%. The water checker now tests every percentage display. |
| 4 | resolved | Chain gap ≤ 1.01e-14. Exact gaps against L: 9.571e-15, 1.0028e-14, 9.332e-15 and 9.772e-15. Against the safe displays: 9.616e-15, 1.0057e-14, 9.400e-15 and 1.0014e-14. |
| 5 | resolved | The name is eg_disc2_s, and 1,152,830 is described as processed boxes. |
| 6 | resolved; residual in #9 | The floor wording and "0 of 158" are added to the integration list and the audit-ir report. |
| 7 | resolved | `literature/control/report.md:184, :715`. |
| 8 | resolved | The safe displays lie 2.98e-17 to 9.50e-17 below N·h2. h2 is printed to 20 digits (`v_lnts.py:209`), an uncertainty of at most 5e-20. Relative gaps are 1.00005–1.00017e-12, so 1.01e-12 is correct. Older documents: #3. |
| 9 | resolved | 5.55e-13 (exact maximum 5.5467e-13 against N·h2, allowing one unit of h2 printing error); 5.79, 6.12, 5.84 and 5.88e-13 are upward roundings of 5.789, 6.112, 5.837 and 5.871e-13; the distance range is labelled approximate. |
| 10 | partly | The linear-independence argument is now used, but its constant is wrong and the file list is incomplete (#7). The rerun point files are byte-identical. |
| 11 | resolved | Two documents added; "a bullet list and a table". Small imprecision in #10. |
| 12 | resolved | dtoc5 local-minimizer claim removed; "p5's maximum row violation"; powerflow slacks e215, e346 and e306 assigned one per instance. |
| 13 | resolved | `sources/QuadHandler_master_r2.cpp:184–236` matches the rule text; `QPLIB_8585.mnt:27–28` gives 99983 and 99997; the reference point lies in [0, 8.057243524908399]. |
| 14 | resolved | The refreshed log gives 4.708e-10 overall and 2.497e-10 for QPLIB_3177, consistent with the README and the report. |
| 15 | resolved | The qualifier "for this MINLPLib model" is added. |
| 16 | resolved | Table 5 is on PDF pp. 69 and 72; Göß is the single author. Optional: add the printed page numbers 67 and 70. |
| 17 | partly | Line 38 is correct; the scope at line 243 is wrong (#8). |
| 18 | partly | Line 36 is correct; line 173 is wrong (#1). |
| 19 | resolved; residual in #8 | The draft is cleaned and `sources/` is listed. |
| 20 | resolved | Review status acknowledged; the code comment now says {lo, hi}. Comma splice: #10. |
| 21 | partly | Lines 60–62 are correct; line 202 lacks "displayed entries" (#9). |
| 22 | resolved; **disagreement adjudicated for the author** | `literature/control/sources/mittelmann_cnconv/logs/QPLIB_2738.mnt:2197`, `QPLIB_2480.mnt:2195` and `QPLIB_2703.mnt:2183` print "mntr-glob: gap percentage = 5.9096 / 13.3380 / 20.8425". These equal the absolute gap divided by \|best solution value\|, for example 0.2532/4.2842. The round-1 statement that the percentages are not printed was wrong; `report.md:191` quotes them correctly. Optional: say the percentage is relative to the incumbent. The other cosmetic items are fixed. |

## The 40 integration replacements

Exact values: lower bounds use the certificate (or the verifier's exact decimal target); primal values use the upper end of the point's objective enclosure. "Old" is the replaced display.

| # | target | change | exact check | result |
|---|---|---|---|---|
| 1 | summary | lnts50 gap 5.5e-13 → 5.79e-13 | 0.5546687649386788986220923 − 0.5546687649381 = 5.789e-13 | valid, minimal upward |
| 2 | summary | lnts100 primal …669 → …670 | f_hi …6691116100178; old is 1.12e-14 below | valid |
| 3 | summary | lnts100 gap → 6.12e-13 | 6.1116e-13 | valid |
| 4 | summary | lnts200 gap → 5.84e-13 | 5.8367e-13 | valid |
| 5 | summary | lnts400 gap → 5.88e-13 | 5.8711e-13 | valid |
| 6 | summary | dtoc5 primal → 5.389672119181141 | +5.33e-16 above f; old 4.67e-16 below | valid |
| 7 | summary | chain column 4 wording | max f_hi − safe display 1.0057e-14 | valid |
| 8 | summary | chain gap → ≤ 1.01e-14 | as #7; dual range 5.06862 … 5.07226 ≤ all L | valid |
| 9 | summary | ex6_2_5 primal …706 → …705 | f = −70.75207783344770558 (20 digits); new +5.7e-16 above f, old 4.2e-16 below | valid |
| 10 | summary | powerflow0039p → 41869.0515113203 | f_hi …1132020380; old 3.8e-12 below | valid, minimal |
| 11 | summary | powerflow0039r → 41869.0515113210 | f_hi …1132098309; old 1.83e-10 below | valid, minimal |
| 12 | summary | eg_int_s → …2275 | objvar 6.4531031593842274088 | valid |
| 13 | summary | eg_disc_s → …5107 | objvar 5.7605396164535106058 | valid |
| 14 | summary | eg_disc2_s verification cell | `eg-recheck/report.md:19–21`; `reviews/eg-recheck-review-r1.md:20` | facts correct; see #4 |
| 15 | summary | waterno2_06 → 282.888038 (exactly feasible) | f = 282.88803738690480797 (own recomputation) | valid, minimal |
| 16 | summary | waterno2_06 gap → 1.68% | 1.67396% against the exact dual 278.2305737746 | valid; see #2 |
| 17 | summary | waterno2_09 label | f = 914.0119752371 ≤ 914.012 | valid |
| 18 | summary | waterno2_09 gap → 10.82% | 10.8115% | valid |
| 19 | summary | waterno2_12 → 2233.821346 | f = 2233.8213456082; old 3.46e-4 below | valid, minimal |
| 20 | summary | waterno2_12 gap → 6.90% | 6.89396% | valid |
| 21 | summary | waterno2_18 label | f = 5023.9827604607 ≤ 5023.983 | valid |
| 22 | summary | waterno2_18 gap → 4.87% | 4.86685% | valid |
| 23 | summary | waterno2_24 → 6963.795181 | f = 6963.7951801564; old 1.80e-4 below | valid, minimal |
| 24 | summary | waterno2_24 gap → 5.90% | 5.89469% | valid |
| 25 | summary | ann_cumene_tanh dual wording | `literature/network/report.md:45–47` (twin proved identical; SCIP and LINDO closed it in floating point) | correct |
| 26 | summary | ann_cumene_tanh → −3379.9823940 | f = −3379.98239407177155; old 5.93e-6 below; dual −3386.5403 ≤ −3386.54022914 | valid, minimal |
| 27 | summary | tolerance-only note | 13 instances; lnts ≤ 5.55e-13 against N·h2 (5.5467e-13); lukvle10 caveat | correct |
| 28 | summary | display-direction sentence | all numeric primal cells comply, except the pre-existing KAN "0.0693" (#6); gaps not covered (#2) | correct as far as it goes |
| 29 | summary | eg coverage parenthetical | as #14 | correct; see #4 |
| 30 | summary | "13 formerly tolerance-only" | 4 + 1 + 1 + 4 + 3 = 13 | correct |
| 31 | audit | display precision and counts | 35/38/46 and 18 strings (r1 group C; author's independent parser) | correct |
| 32 | audit | slack floor | 0/158; 17 tie pairs on fac1, fac2 and waternd_fosspoly0 | correct |
| 33 | audit | spring wording | 5 pairs (`audit-ir/report.md:19–22`); the 1e-9 sentence lacks context | see #5 |
| 34–35 | cops report | chain50 → 5.0722614939828627; chain200 → 5.0689173417931616 | truncations of L = 5.07226149398286274561…, 5.06891734179316166830…; old displays 2.54e-16 and 3.32e-16 above L | valid; stale gap cells (#3) |
| 36–37 | cops verification report | same | same; 2 occurrences each, plus one already-correct occurrence | valid; see #3 |
| 38–40 | closing-audit-a, solver-campaign-review-r1, solver-runs/report.prev.md | chain50 only | same. The differences quoted at `solver-campaign-review-r1.md:43` (1.893e-12, 1.697e-12) are unchanged at 4 digits against the new display | valid |

**Other displays in the summary (scan), all valid:**
- **Duals:** lnts, dtoc5, camshape100–800, lukvle10, optcdeg2, ex6_2_5, ex6_2_7, etamac, pricing050 (upper bound ≥ the exact bound −1813.82907845197305775), powerflow, pindyck, catmix range, waterno2 (all three bounds for 06), ann_cumene_tanh.
- **Primals:** lukvle10, optcdeg2, ex6_2_7, pricing050 (maximization, rounded down), pindyck, eg_disc2_s.

The only remaining problems are #2 and #6.

## Commands run

All commands were run from `research-20260929` or the review directory, single-threaded (`OMP_NUM_THREADS=1`), at most 3 processes at a time. No scientific script was imported or run in the main tree. No main computation, solver run, project-wide verification or CI inspection was done, and no track or author file was edited.

Lead (`minor-fixes-review-r2/scratch/`):

```sh
cat minor-fixes-review-r1.md minor-fixes/{response-r2.md,summary.md,PROGRESS.json,FILES-r2.json,check_r2.log,protected-r2.json}
sed -n 1,200p minor-fixes/check_r2.py
python3 scratch/apply_check.py > scratch/apply_check.log      # 40 old strings: counts, sequential application, summary.md == JSON
python3 scratch/recompute_objs.py | tee scratch/recompute_objs.log   # dtoc5 + waterno2_* objectives from OSIL (1.5 s)
python3 scratch/check_displays.py | tee scratch/check_displays.log   # all displays and gaps, exact Fractions
python3 - (in-memory application of the 40 edits to scratch/applied/*, then diff against the current files)
git log/status -- open-instances-summary.md bound-audit/audit-report.md
grep/sed reads: open-instances-summary.md; bound-audit/audit-report.md:236-296,640-670,1005-1012;
  open-instances-wave2/cops/report.md:10-30,165-180; reviews/cops-verification/verification-report.md:12-40,185-215;
  reviews/closing-audit-a.md:125-140; reviews/catmix-recheck.md:1-40; reviews/eg-retry-review.md;
  reviews/closing-confirm-r3-checks/logs/lukvle10_display.log; eg-recheck/report.md; audit-ir/report.md;
  literature/network/report.md (twin); literature/control/sources/mittelmann_cnconv/logs/QPLIB_{2738,2480,2703}.mnt;
  scip-bug/report.md:119,167-173,243; scip-bug/logs/{binary64_scip_solution,pair_semantics}.log;
  primal/lnts/{report.md:57,lnts_primal.py:44,150-175}; solver-runs/smoke2/basic/results.json (chain50)
python3 -c (lnts 1e-12/1e-10 displays vs N*h2; emfl050_3_3 relative margin; KAN point objectives)
```

The sub-agents' exact command lists are in `minor-fixes-review-r2/agent-issues.md` (issues 1–22; scripts in `scratch-issues/`) and `minor-fixes-review-r2/agent-collateral.md` (hunk classification, patch re-application, before-r2 reconstruction, hashes, log sizes and mtimes; scripts in `scratch-collateral/`). These are local targeted checks, separate from CI.
