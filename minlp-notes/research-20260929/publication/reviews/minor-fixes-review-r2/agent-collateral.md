# Collateral-damage check of the round-2 minor fixes (sub-agent B)

Date: 2026-10-03. Scope: tasks 1–6 of the brief. P = `research-20260929/publication`, M = `P/reviews/minor-fixes`. All paths below are relative to P unless they start with `research-20260929/`. Scratch files are in `P/reviews/minor-fixes-review-r2/scratch-collateral/`.

No file outside `reviews/minor-fixes-review-r2/` was edited. No scientific script from the main tree was imported or run. Only read-only shell tools and my own small read-only Python scripts were used, serially on one core.

## Verdict

No accidental deletions, no broken links, no new broken tables and no unexplained number changes were found in the round-2 diffs. The recorded round-2 patch exactly reproduces the current files. The two protected files are unchanged. No tracked or untracked log in the ten tracks was truncated. The new check logs postdate their scripts and match the current code.

There is one new numerical slip (finding 1), one omitted file in `FILES-r2.json` (finding 2), two round-2 edits missing from the track response tables (finding 3) and some small wording or record-keeping points.

## Findings

### 1. lnts: wrong constant in the new rational-point proof (minor, new in round 2)

- **Location:** `primal/lnts/report.md:57`: "vx_N = 45 would require Σ w_j cos θ_j = 45/(50h)".
- **Evidence:**
  - The rows (report lines 33–34 and 40) give v_{i+1} = v_i + 50h(cos θ_i + cos θ_{i+1}). Summing them gives vx_N = 100h Σ w_j cos θ_j with the trapezoid weights w = (1/2, 1, …, 1, 1/2).
  - Those are the weights in `primal/lnts/lnts_primal.py:162` (`w = [Fraction(1, 2)] + [Fraction(1)] * (N - 1) + [Fraction(1, 2)]`). The report uses the same w_j in the tangent law at line 38.
  - The cited r1 review (`reviews/primal-lnts-review-r1.md:42`, item 8) correctly writes 45/(100h).
  - 45/(50h) is right only for the weights (1, 2, …, 2, 1). The proof still holds, because any positive rational multiple works, but the stated constant is wrong for the weights the report uses.
- **Fix:** Write 45/(100h), or define w_j explicitly as (1, 2, …, 2, 1).

### 2. FILES-r2.json omits a file that round 2 rewrote (minor, record-keeping)

- **Location:** `reviews/minor-fixes/FILES-r2.json`. `run_checks_r2.py:33` rewrote `primal/water-ann-kan/logs/minor_review_check.log` at 22:49:56 (with `>`).
- **Evidence:**
  - The file is listed in the cumulative `FILES.json`, but not in `FILES-r2.json`, and it has no `before-r2/` copy. Its round-2 diff therefore cannot be audited directly.
  - The current content agrees with the values group C recorded in round 1 (`reviews/minor-fixes-review-r1/group-C.md:36–37`: 1.6739582e-2, 1.0811534e-1, 6.8939570e-2, …). The new asserts in the script print nothing, so no change in output is expected. No damage is evident.
- **Fix:** Add the log to `FILES-r2.json`.

### 3. Two round-2 edits are not listed in their track's round-2 response table (minor, disclosure)

- **literature/control:**
  - Locations: `literature/control/report.md:36` ("Our rigorous closure to ≤ 5.55e-13") and `:272` ("Our rigorous ≤ 5.55e-13 closure").
  - Both lines previously said 5.5e-13. The change propagates issue 9 and is correct (it matches `primal/lnts/report.md:19`).
  - The control round-2 table (lines 722–731) lists only issues 7, 13, 14 and 22. `response-r2.md` issue 9 mentions only the lnts report and the integration list.
- **primal/water-ann-kan:**
  - Location: `primal/water-ann-kan/report.md:27` now says "The old summary 1.67% is rounded to nearest. Use 1.68% …".
  - The number is correct: the exact gap/dual is 1.67395824% (my check; the log gives 0.016739582387).
  - The change matches integration item `integration-r2.json:95–96`. However, the water round-2 table (line 195 onward, issue 3) and `response-r2.md` issue 3 mention only waterno2_12.
- **Fix:** Add a row "9 — propagated ≤ 5.55e-13" to the control round-2 table. Mention waterno2_06 1.67% → 1.68% under issue 3 in the water table and in `response-r2.md`.

### 4. Water report wording (cosmetic, new in round 2)

- `primal/water-ann-kan/report.md:5` contains a comma splice: "…by the same author, independent review r1 later verified…". Use "…by the same author; independent review r1 later verified…".
- `primal/water-ann-kan/report.md:27` ends with a dangling clause: "Use 1.68% for an upward two-decimal percentage display, now measured against an exactly feasible point." Suggested wording: "The gap 1.674% is now measured against an exactly feasible point; for a two-decimal upward display use 1.68%."

### 5. Chain report: three of the five documents contain only the chain50 decimal (minor, imprecise)

- **Location:** `primal/chain/report.md:26` says that both 5.072261493982863 (chain50) and 5.068917341793162 (chain200) occur in all five listed documents.
- **Evidence (grep counts, chain50 / chain200):**

  | document | chain50 | chain200 |
  |---|---|---|
  | `open-instances-wave2/cops/report.md` | 2 | 2 |
  | `reviews/cops-verification/verification-report.md` | 2 | 2 |
  | `reviews/closing-audit-a.md` | 1 | 0 |
  | `publication/reviews/solver-campaign-review-r1.md` | 1 | 0 |
  | `publication/solver-runs/report.prev.md` | 1 | 0 |

  The integration list in `summary.md` correctly gives only the chain50 edit for the last three.
- **Fix:** Mark the last three documents "(chain50 value only)".

### 6. Unescaped pipes break two response-table rows (minor, pre-existing from round 1)

- **Locations:**
  - `primal/lnts/report.md:129`: `|control| < 1e-110` gives 4 cells instead of 2.
  - `primal/powerflow/report.md:158`: `||I − C J(X)||∞` gives 6 cells instead of 2.
- **Evidence:** The before-r2 copies have the same defect, so round 2 did not cause it. The `summary.md` copies of these rows escape the pipes (`\|`).
- **Fix:** Escape the pipes as in `summary.md`.

### 7. Recorded round-1 patch is malformed (record-keeping, round 1)

- **Location:** `reviews/minor-fixes/report_changes.patch:801–827`, the last hunk of `literature/control/report.md`.
- **Evidence:**
  - The header says `+695,25`, but the hunk has 24 new lines.
  - `before/literature__control.txt` has no final newline, and the patch lacks a "\ No newline at end of file" marker. As a result, the last `-` line and the first `+` line are joined on one line ("…eg_disc2_s.+- **For other tracks…").
  - GNU `patch` stops with "malformed patch at line 828". `git apply --recount` also fails on this patch.
- **Fix:** Regenerate the patch with `diff -u`. (After splitting that one line, the round-1 patch applied to `before/` reproduces `before-r2/`; see task 3.)

### 8. Small observations (no fix required unless noted)

- **dtoc5 title (cosmetic, unexplained):** hunk 28 removes a trailing space from the title at `primal/dtoc5-lukvle10/report.md:3`. This is harmless and not listed anywhere.
- **lnts command record:** `primal/lnts/report.md:108` edits a historical command-output record ("-> max diff approximately 3.25e-15..3.54e-15"). This applies issue 9 inside a transcript. It is harmless, but a transcript ideally stays verbatim; consider a note instead.
- **dtoc5 reference checker:**
  - `literature/control/checks/dtoc5_reference_check.py` prints the 99,997/99,983/14 conclusions as fixed strings rather than computing them.
  - Its first log line still says "URL … matches saved r2 hash", although the script now only hashes the saved file.
  - The report's lower endpoint 1.460728991e-5 (`literature/control/report.md:296`) is asserted (> 0) but not printed. I confirmed it independently: min = x49999 = 1460728991/10^14, max = x2 = 8057243524908399/10^15, 99,998 entries.
  - Optional fix: print min/max, and write "saved file sha256".
- **report.prev.md snapshot:**
  - `before-r2/literature__control__report.prev.md` (22:54:21) was not saved before the edit. `finish_r2.py:54–57` reconstructed it by removing the one-paragraph note that `edit_r2.py:103–104` prepended.
  - Because the current file has exactly one such header, the reconstruction is exact. No independent copy exists (searched by size and sha256).
- **check_r2.log rerun:** `check_r2.log` (22:54:24) was regenerated after `check_r2.py` was last modified (22:52:57), so it is current. However, `commands-r2.json` (22:49:59) records only the earlier run. The rerun is described only in prose at `commands.md:152`.
- **commands.md timing:** `commands.md` was modified at 22:57:36, after `validation_r2.log` (22:57:25) and the patch (22:57:06). It has no before-r2 copy, so the patch does not cover it.
- **README line length (cosmetic):** `literature/control/checks/README.md:30` is now an over-long line in an otherwise wrapped paragraph.

## Task results

### Task 1: per-hunk classification (58 hunks, current diff before-r2 → now)

Class: **a** = explained by review issue n (per `response-r2.md`); **b** = response/round-2 note; **c** = unexplained.

| # | file | hunk (old → new) | class | content / check |
|---|---|---|---|---|
| 1 | audit-ir/report.md | -57,9 +57,10 | a 21, 6 | displayed entries (18 distinct strings), trailing zeros, 17 tie pairs on 3 instances; slack-floor note (0 of 158). Numbers match r1 review. |
| 2 | audit-ir/report.md | -215,3 +216,14 | b | round-2 table (6, 21); links resolve |
| 3 | eg-recheck/report.md | -20,7 +20,7 | a 22 | tree-free proof citation; paths exist |
| 4 | eg-recheck/report.md | -258,3 +258,14 | b | round-2 table (5, 22) |
| 5 | lit/control/checks/README.md | -27,7 +27,7 | a 14 | 4.7e-10 / 2.5e-10 match the refreshed log (4.708e-10, 2.497e-10) |
| 6 | lit/control/checks/dtoc5_reference_check.log | -1,3 +1,6 | a 13 | matches the current script's 6 print statements |
| 7 | lit/control/checks/dtoc5_reference_check.py | -1,17 +1,20 | a 13 | fetch removed; signed values; min > 0 assert |
| 8 | lit/control/checks/qplib_camshape_compare.log | -1,28 +1,24 | a 14 | rerun from repository root (paths now repository-relative; no blank separators, which the script never prints); 4.708e-10 and 2.497e-10 at x1.up; 2.481e-11 at x1.up for 2480 matches report line 192 |
| 9 | lit/control/report.md | -33,7 +33,7 | a 9 (propagated; not in control table, finding 3) | 5.5e-13 → ≤ 5.55e-13 |
| 10 | lit/control/report.md | -181,14 +181,14 | a 7/13, 22 | 8585 cell; 1.2e-10/2.5e-10 (log: 1.218e-10, 2.497e-10); printed gaps 5.9096/13.3380/20.8425 confirmed at .mnt lines 2197/2195/2183 |
| 11 | lit/control/report.md | -269,7 +269,7 | a 9 (propagated; finding 3) | lnts50 ≤ 5.55e-13 |
| 12 | lit/control/report.md | -293,7 +293,7 | a 13 | rule matches `QuadHandler_master_r2.cpp:184–229`; range [1.460728991e-5, 8.057243524908399] confirmed |
| 13 | lit/control/report.md | -528,7 +528,7 | a 13 | open-issue bullet |
| 14 | lit/control/report.md | -694,14 +694,15 | a 22, 13 | QPLIB scale wording; dtoc5 caveat; blank line before `## Response to review` |
| 15 | lit/control/report.md | -712,8 +713,21 | a 13 (round-1 row 2.5 rewritten) + b | round-2 table (7, 13, 14, 22) |
| 16 | lit/control/report.prev.md | -1,3 +1,5 | a 22 | superseded note only (snapshot reconstructed; §8) |
| 17 | lit/network/report.md | -58,7 +58,7 | a 16 | Göß 2026 single author |
| 18 | lit/network/report.md | -71,7 +71,7 | a 22 | arXiv v2 Table 4 |
| 19 | lit/network/report.md | -111,7 +111,7 | a 16 | Table 5, pp. 69 and 72 |
| 20 | lit/network/report.md | -132,7 +132,7 | a 15 | "found for this MINLPLib model" |
| 21 | lit/network/report.md | -166,7 +166,7 | a 22 | checked Default R3_H1_N4.log |
| 22 | lit/network/report.md | -265,7 +265,7 | a 16 | Table 5, pp. 69 and 72 |
| 23 | lit/network/report.md | -313,7 +313,7 | a 22 | checker listed |
| 24 | lit/network/report.md | -359,7 +359,7 | a 22 | VSDP URL unified |
| 25 | lit/network/report.md | -511,8 +511,20 | a 22 (round-1 row 7) + b | round-2 table (15, 16, 22) |
| 26 | primal/chain/report.md | -23,7 +23,7 | a 11, 4 | five documents; ≤ 1.01e-14 (finding 5: chain200 absent from 3 documents) |
| 27 | primal/chain/report.md | -187,3 +187,14 | b | round-2 table (4, 11) |
| 28 | primal/dtoc5-lukvle10/report.md | -1,6 +1,6 | **c** (cosmetic) | trailing space removed from title |
| 29 | primal/dtoc5-lukvle10/report.md | -16,8 +16,8 | a 2, 12 | 5.389672119181141 ≥ exact enclosure 5.38967211918114046…; "maximum row violation of p5" |
| 30 | primal/dtoc5-lukvle10/report.md | -124,7 +124,7 | a 12 | local-minimizer claim removed |
| 31 | primal/dtoc5-lukvle10/report.md | -138,3 +138,14 | b | round-2 table (2, 12) |
| 32 | primal/lnts/report.md | -8,15 +8,15 | a 8, 9 | 1.00e-12 → 1.01e-12 (exact rel. ≈ 1.00012e-12, upward 1.01e-12); duals …565/…290 rounded down; 5.79/6.12/5.84/5.88 match table |
| 33 | primal/lnts/report.md | -54,7 +54,7 | a 10 | **finding 1: 45/(50h) should be 45/(100h)** |
| 34 | primal/lnts/report.md | -80,8 +80,8 | a 1, 9 | lnts100 0.5545954011670 |
| 35 | primal/lnts/report.md | -89,9 +89,12 | a 10 | checker listed; obsolete-log note; reviewer rerun path exists |
| 36 | primal/lnts/report.md | -102,7 +105,7 | a 9 | "approximately" inserted into a command record (§8) |
| 37 | primal/lnts/report.md | -110,8 +113,8 | a 9 | ≤ 5.55e-13; summary-dual upper gaps |
| 38 | primal/lnts/report.md | -121,8 +124,21 | a 9 (round-1 row 3) + b | round-2 table (1, 8, 9, 10) |
| 39 | primal/powerflow/report.md | -41,7 +41,7 | a 12 | e215/e346/e306 split per instance |
| 40 | primal/powerflow/report.md | -158,3 +158,13 | b | round-2 table (12) |
| 41 | primal/water-ann-kan/code/minor_review_check.py | -19,6 +19,11 | a 3 | assert display ≥ exact ratio; no new output |
| 42 | primal/water-ann-kan/code/nn_exact.py | -140,7 +140,7 | a 20 | comment only |
| 43 | primal/water-ann-kan/report.md | -2,7 +2,7 | a 20 | review status (finding 4: comma splice) |
| 44 | primal/water-ann-kan/report.md | -24,8 +24,8 | a 3 | 6.90% (exact 6.8939570%); waterno2_06 1.68% (exact 1.6739582%; finding 3) |
| 45 | primal/water-ann-kan/report.md | -191,3 +191,14 | b | round-2 table (3, 20) |
| 46 | reviews/minor-fixes/summary.md | -1,8 +1,8 | b | completion text, r2 patch link |
| 47 | reviews/minor-fixes/summary.md | -10,30 +10,529 | a 1, 2, 4, 5, 6, 9, 11, 21, sweep + b | integration bullets and 40 exact edits; 14 removed lines are all replaced versions; no inventory row lost (57 → 57) |
| 48 | reviews/minor-fixes/summary.md | -42,12 +541,12 | a 3 | water row 2 cell |
| 49 | reviews/minor-fixes/summary.md | -67,7 +566,7 | a 7, 13 | control row 2.5 cell |
| 50 | reviews/minor-fixes/summary.md | -76,7 +575,7 | a 22 | network row 7 cell |
| 51 | scip-bug/report.md | -33,9 +33,9 | a 18, 17 | 56.492/65.12 refuted, 55.69 not (matches §6, lines 309–313); seeds 8 and 14 |
| 52 | scip-bug/report.md | -170,7 +170,7 | a 18 | five examined solutions (the list at line 169 has five) |
| 53 | scip-bug/report.md | -240,7 +240,7 | a 17 | instrumented cutoffs in §5.3 |
| 54 | scip-bug/report.md | -357,6 +357,8 | a 19 | files table rows |
| 55 | scip-bug/report.md | -499,7 +501,7 | a 19 | draft: internal log/review path removed |
| 56 | scip-bug/report.md | -524,7 +526,7 | a 19 | tiny2 inequality: 0.8 < (1.537/1.6)² = 0.9228004 (exact check true) |
| 57 | scip-bug/report.md | -552,7 +554,7 | a 19 | "Review r1 proposed" removed |
| 58 | scip-bug/report.md | -575,3 +577,15 | b | round-2 table (17, 18, 19) |

Additional checks on these diffs:

- **Changed numbers:** every changed number is explained by an issue number above.
- **Deletions:** removed lines in the reports are replaced versions of the same sentences. No section, row or link was lost.
- **Duplicated text:** repeated lines in `summary.md` are the expected old/new pairs of sequential edits.
- **Links:** every Markdown link and backticked relative path on an added line resolves. The only exceptions are links inside the quoted old/new code blocks of `summary.md`, which are relative to `research-20260929/` and do not render as links.
- **Tables:** no new table defect was found; see finding 6 for the pre-existing ones.
- **SCIP draft:** it no longer contains `logs/`, `../`, `review` or `/home/` (scratch `scip_draft.txt`).
- **Stale phrases:** a grep for the phrases the review flagged ("full value", "6.89%", "local minimizer", "Göß et al", "pp. 42", "vsdp/", "eg_all", "processed-leaf", "three are in display", "All traced", "consistent reading", "Review r1", "rv_runs", "centre and radius", "all <= 2.5e-10", "[−100") found no stale occurrence in the ten tracks.

### Task 2: recorded round-2 patch versus current files

- The current diffs and `report_changes_r2.patch` have the same 58 hunks.
- The only differences are the hunk-header layout and the position of the inserted blank line around one moved paragraph (lnts lines 89–92 and the `summary.md` header). These come from difflib versus GNU diff alignment.
- Applying the recorded patch with GNU `patch -p1` to fresh copies of all 18 `before-r2/` files succeeds without fuzz or offset. All 18 results are byte-identical (`cmp`) to the current files.
- No edits were made after the recorded patch. Exception: `commands.md` (22:57:36), which the patch does not cover (§8).

### Task 3: before-r2 copies versus the post-round-1 state

- **Reports:** I applied `report_changes.patch` to `before/<track>.txt` with a lenient applier (`scratch-collateral/apply_lenient.py`).
  - All ten reconstructed reports equal the `before-r2/*__report.md` copies.
  - For `literature/control/report.md`, this required splitting the malformed joined line (finding 7). The result then differs only by the final newline.
  - The seven tracked `before/` copies equal git HEAD. scip-bug and literature are untracked.
- **Non-report copies:** these are consistent with the round-1 review evidence:
  - the README says "all <= 2.5e-10" (line 30);
  - the qplib log has 8.921e-11 for the QPLIB_2703 point and lower-bound-only maxima;
  - the `nn_exact.py` comment says "centre and radius" (line 143), and the only differences from HEAD are the round-1 description string and path-only `_REPRO_ROOT` edits;
  - the `summary.md` lines 12–16 match the line references in the r1 review (eg_all, "processed-leaf");
  - the water checker had no gap assertions, as noted in `group-C.md:41`.
- **Timing:** the copies were taken at 22:29:26, after the round-1 review was written (22:20:45) and before the first round-2 edit (22:35:08). The exception is `report.prev.md` (§8).

### Task 4: protected files and modified-file inventory

- **Protected files:** the sha256 of `research-20260929/open-instances-summary.md` is 09da6cae…cdb3d, and that of `research-20260929/bound-audit/audit-report.md` is c116b7d7…8f63. Both equal `protected-r2.json` and git HEAD. The mtimes are 2026-10-01 and 2026-09-30, and git status is clean for both.
- **Repository state:** `git status` for `research-20260929` shows 202 modified (M) and 212 untracked (??) files. `git diff --stat` reports 202 files changed, +10,305/−759.
- **Track files outside FILES.json ∪ FILES-r2.json:** 17 modified track files fall outside both lists:
  - chain: build_points, scip_crosscheck, verify_points;
  - dtoc5-lukvle10: 7 scripts;
  - lnts: crosscheck;
  - powerflow: pfmodel;
  - water-ann-kan: 5 code files.

  All have mtimes of 21:31–21:33, before round 2. `git diff -U0` shows only path-portability edits (`_REPO`/`_REPRO_ROOT`/`expanduser`), which belong to the parallel reproduction work.
- **Files modified since 22:29:26** (`find -newer before-r2/audit-ir__report.md`):
  - inside the ten tracks: exactly the files in FILES-r2, plus `primal/water-ann-kan/logs/minor_review_check.log` (finding 2);
  - outside: `reproduction/*` and the path-only edits to `open-instances-scout/{hvycrash_check,structure}.py` and `treewidth-census/census.py` (22:33:50), which are reproduction work, not round 2.

### Task 5: logs not truncated

- No tracked log under `primal/`, `audit-ir/` or `eg-recheck/` differs in size from HEAD.
- The only empty log in the ten tracks is `eg-recheck/logs/run_record.out`, dated 2026-10-01 and the same size as at HEAD (0).
- In `scip-bug/logs`, `literature/control/checks` and the `primal/*/logs` directories, the only files modified after 22:29 are those listed in FILES-r2, plus the water log (finding 2).

### Task 6: new files and check logs

- All 37 FILES-r2 entries exist. 18 have `before-r2/` copies; the others are new or are review-process files.
- **Logs postdate their scripts:**

  | log | log mtime | script | script mtime |
  |---|---|---|---|
  | `primal/lnts/logs/review_r2_check.log` | 22:49:58 | `primal/lnts/minor_review_check.py` | 21:34:06 |
  | `scip-bug/logs/review_r2_check.log` | 22:49:58 | `scip-bug/minor_review_check.py` | 21:56:55 |
  | `literature/control/checks/dtoc5_reference_check.log` | 22:49:58 | `dtoc5_reference_check.py` | 22:35:08 |
  | `literature/control/checks/qplib_camshape_compare.log` | 22:49:59 | `qplib_camshape_compare.py` | 21:32:59 |
  | water `minor_review_check.log` | 22:49:56 | water `minor_review_check.py` | 22:35:08 |
  | `check_r2.log` | 22:54:24 | `check_r2.py` | 22:52:57 |

- The two `review_r2_check.log` files are byte-identical to the round-1 `minor_review_check.log` from the unchanged scripts. The lnts widths are < 2.1e-106, objective widths < 3e-109, and old-vector distances 3.2546e-15–3.5437e-15, all matching the report.
- The qplib log format matches the script's print statements exactly. The script prints no blank separators, and a run from the repository root explains the repository-relative paths. Bound violations now include `.up`/`.lo`. Its maxima (1.741e-10, 2.420e-10, 4.708e-10, 2.497e-10) equal the r1 reviewer's independent values.
- The dtoc5 reference log matches the six print statements of the current script. `float('8.057243524908399')` prints as 8.0572435249084 (same double). The saved `.sol` sha256 is 9d9f5c4f…455cd, as asserted.
- **Result:** no stale outputs.

## Commands run

All commands were run from `/workspace/minlp-notes` or `P`, serially. "S" = `P/reviews/minor-fixes-review-r2/scratch-collateral`.

```sh
ls -la $M $M/before-r2 $M/before; cat $M/FILES-r2.json $M/protected-r2.json; ls -la P/reviews/minor-fixes-review-r2/
mkdir -p S; cat $M/response-r2.md; cat P/reviews/minor-fixes-review-r2/PROGRESS.json
cat P/reviews/minor-fixes-review-r1.md; ls P/reviews/minor-fixes-review-r1/
python3 - (own: diff -u --label before/<f> --label after/<f> for every FILES-r2 entry with a before-r2 copy) > S/r2_now.patch; python3 - (own: list FILES-r2 entries, before-r2 copy present / file exists)
wc -l S/r2_now.patch; head -30 $M/report_changes_r2.patch; grep -c '^@@' S/r2_now.patch $M/report_changes_r2.patch; grep '^+++\|^---' $M/report_changes_r2.patch
diff <(grep -v '^@@\|^---\|^+++' S/r2_now.patch) <(grep -v '^@@\|^---\|^+++' $M/report_changes_r2.patch); diff <(grep '^@@' S/r2_now.patch) <(grep '^@@' $M/report_changes_r2.patch)
python3 - (own: copy before-r2 files into S/apply/before-r2/<path>); cd S/apply/before-r2 && patch -p1 --dry-run < $M/report_changes_r2.patch; patch -p1 -s < $M/report_changes_r2.patch; for f in ...; do cmp -s $f P/$f; done; find . -name '*.orig' -o -name '*.rej'
cd S/apply2/x && patch -p1 -R --dry-run < $M/report_changes_r2.patch; python3 - (own: fresh copies into S/apply/x2); cd S/apply/x2 && patch -p1 --dry-run < $M/report_changes_r2.patch | grep -v '^checking'
grep '^---\|^+++' $M/report_changes.patch; head -80 $M/FILES.json
cd S/r1apply; cp $M/before/<t>.txt <t>/report.md (10 tracks); patch -p1 < $M/report_changes.patch   # -> "malformed patch at line 828"
for t in ...; cmp <t>/report.md $M/before-r2/<t>__report.md; git show HEAD:research-20260929/publication/<t>/report.md | cmp - $M/before/<t>.txt
grep -n '^@@\|^---\|^+++' $M/report_changes.patch | awk -F: '$1>700 && $1<840'; sed -n 815,830p $M/report_changes.patch | cat -A
sed -n 801,827p $M/report_changes.patch | python3 -c '<own hunk line counter>'; tail -c 200 $M/before/literature__control.txt | cat -A; tail -c 100 P/literature/control/report.md | cat -A
git apply --recount -p1 -v $M/report_changes.patch   # in S/r1apply; failed (chain hunk), nothing applied
python3 S/apply_lenient.py   # own lenient applier; then the same with the joined line split (python3 - exec of the modified source)
tail -c 300 $M/before-r2/literature__control__report.md | cat -A; diff S/r1lenient/literature/control/report.md $M/before-r2/literature__control__report.md
(failed: bash syntax error, missing "do") for f in <8 non-report files>; ... git show HEAD:... | cmp - before-r2 copy
for f in <8 non-report files>; do git cat-file -e HEAD:...; git show HEAD:... | cmp -s - $M/before-r2/<f>; done; git log -1 --format='%H %ci'
git status --short research-20260929/publication | head -50; ... | wc -l; git ls-files research-20260929/publication | awk -F/ '{print $3"/"$4}' | sort | uniq -c
diff $M/before-r2/literature__control__report.prev.md P/literature/control/report.prev.md; ls -l --time-style=full-iso ...; grep -n 'report.prev' $M/*.py $M/commands.md $M/commands-r2.json $M/summary.md $M/PROGRESS.json
sed -n 40,75p $M/finish_r2.py; sed -n 95,115p $M/edit_r2.py
sha256sum $M/before-r2/literature__control__report.prev.md; find research-20260929 -type f -size 34327c | xargs sha256sum; git log --all --oneline -- research-20260929/publication/literature/control/report.prev.md
sed -n 1,30p $M/edit_r2.py; grep -n 'before-r2\|snapshot\|copy' $M/edit_r2.py $M/check_r2.py $M/run_checks_r2.py $M/build_integration_r2.py $M/validate_r2.py
grep -n '2.5e-10' before-r2 README; grep -n '8.921e-11\|2026-10-0' before-r2 qplib log; sed -n 141,145p before-r2 nn_exact.py; sed -n 12,16p before-r2 summary.md; ls -l --time-style=full-iso P/reviews/minor-fixes-review-r1.md P/reviews/minor-fixes-review-r1/*.md
sed -n 1,200p S/r2_now.patch; sed -n 200,420p S/r2_now.patch; sed -n 420,640p S/r2_now.patch > S/part3.txt; sed -n 640,1273p S/r2_now.patch > S/part4.txt; grep -n '^---\|^+++\|^@@' S/part4.txt   (and Read of these files)
grep -n <stale phrases> primal/lnts/report.md primal/water-ann-kan/report.md primal/water-ann-kan/code/*.py primal/dtoc5-lukvle10/report.md primal/chain/report.md literature/control/report.md literature/network/report.md scip-bug/report.md audit-ir/report.md eg-recheck/report.md literature/control/checks/README.md
sed -n 155,175p scip-bug/report.md; sed -n 280,295p scip-bug/report.md; grep -n '^## \|^### ' scip-bug/report.md
python3 S/linkcheck.py    # own: links/backticked paths on added lines
python3 S/tablecheck.py   # own: table cell counts before-r2 vs now
python3 - (own Fractions: waterno2_06 gap %, tiny2 inequality); sha256sum literature/control/sources/qplib/QPLIB_8585.sol; python3 -c '<own: min/max of x in QPLIB_8585.sol>'; ls literature/control/sources ...
find literature/control -name 'QPLIB_27xx/2480.mnt'; sed -n 2197p/2195p/2183p of the three .mnt logs
cat $M/run_checks_r2.py; python3 -c '<print commands-r2.json>'
ls -l --time-style=+%H:%M:%S literature/control/checks/ primal/lnts/logs/ primal/lnts/*.py scip-bug/logs/ scip-bug/*.py primal/water-ann-kan/logs/ primal/water-ann-kan/code/minor_review_check.py
find research-20260929 -newer $M/before-r2/audit-ir__report.md -type f (excluding minor-fixes-review-r2, __pycache__) -printf ... | sort
python3 - (own: git status --short --untracked-files=all research-20260929, filter ten tracks not in FILES ∪ FILES-r2, with mtimes)
git diff -U0 -- <17 unlisted track scripts> | grep '^[-+]'
sha256sum research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md; cat protected-r2.json; git status --short / git diff --stat on both; ls -l --time-style=full-iso both; git show HEAD:<both> | sha256sum
git diff --stat -- research-20260929 | tail -3; git status --short research-20260929 | awk '{print $1}' | sort | uniq -c; git diff -U0 -- open-instances-scout/{hvycrash_check,structure}.py treewidth-census/census.py
find primal audit-ir eg-recheck scip-bug literature/control literature/network -type f -size 0 (logs/checks); for tracked logs in primal/audit-ir/eg-recheck: compare git cat-file -s HEAD:<f> with stat -c %s
cmp primal/lnts/logs/review_r2_check.log primal/lnts/logs/minor_review_check.log; cmp scip-bug/logs/review_r2_check.log scip-bug/logs/minor_review_check.log; cat the three logs
cat literature/control/checks/qplib_camshape_compare.py; python3 -c "print(float('8.057243524908399')==float('8.0572435249084'), repr(8057243524908399/10**15))"
cat literature/control/checks/README.md; grep -rn 'review_r2_check' --include=*.md P
cat $M/validation_r2.log; sed -n 1,80p $M/validate_r2.py
awk '<scip draft section>' scip-bug/report.md > S/scip_draft.txt; grep -n -i 'logs/\|\.\./\|review\|scratch\|publication/\|/home/\|PROGRESS\|witness' S/scip_draft.txt
grep -n 'addDefaultBounds' -A45 literature/control/sources/QuadHandler_master_r2.cpp
git show HEAD:.../nn_exact.py | diff - $M/before-r2/primal__water-ann-kan__code__nn_exact.py; grep -n 'minor_review_check.py\|nn_exact' P/reviews/minor-fixes-review-r1/group-C.md
grep -rl 'gap/abs(dual)' P/reviews/minor-fixes-review-r1/; grep -n ... $M/validation.log $M/PROGRESS.json; grep -n 'gap/abs(dual)' -B2 -A3 group-C.md
ls P/reviews | grep -i lnts; grep -n -i 'linear.independen\|Lindemann' P/reviews/primal-lnts-review-r1.md; sed -n 38,46p of it
grep -n 'w_j\|vx_N\|...' primal/lnts/report.md; sed -n 36,42p primal/lnts/report.md; grep -n 'w\[\|w_j\|weights\| w =' primal/lnts/lnts_primal.py
sed -n 9,20p primal/water-ann-kan/report.md
for f in <5 chain documents>; grep -c 5.072261493982863 / 5.068917341793162; grep -rln '<both decimals>' --include=*.md research-20260929
python3 - (own: summary.md before/after row and heading counts, removed lines, duplicate lines)
sed -n 300,324p scip-bug/report.md
grep -n 'Round 2' -A3 $M/commands.md; grep -n 'rerun\|strengthened' $M/commands.md; tail -3 $M/check_r2.log; misc grep -n for line numbers (water/lnts/powerflow/dtoc5 head)
grep -n '^### Round 2' literature/control/report.md primal/water-ann-kan/report.md primal/lnts/report.md; wc -l literature/control/report.md
awk '/^\+\+\+ /{f=$2} /^@@/{print f" "$2" "$3}' S/r2_now.patch | nl
```

All of these are local, targeted, read-only checks. They are separate from CI, and no project-wide verification was run.
