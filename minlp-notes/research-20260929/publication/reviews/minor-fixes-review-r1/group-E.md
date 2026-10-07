# Verifier group E: literature/control and literature/network

Date: 2026-10-03. P = research-20260929/publication. The track files were read only. My scratch script and logs are in `scratch-E/`.

Overall: all 16 issues are fixed in substance. I found no blocker or major problem. There are 2 minor problems in literature/control (2.1 stale log/README; 2.5 default-bound inference) and 3 minor problems in literature/network (stale unqualified novelty phrase, Müller page attribution, Göß "et al."). The rest are nits.

## literature/control (review: reviews/lit-control-review-r2.md, Section 2)

### 2.1 Missed upper bounds: fix in report OK; minor problem with stale artifacts

- **Script change: minimal and correct.** No pre-fix copy exists on disk, because `literature/` is gitignored and nothing exists in reviews/lit-control-r2. I recovered the old text from the author's session log (`~/.codex/sessions/2026/10/03/rollout-...01a10487....jsonl`). The edit was exactly `('r"^(\w+)\.(lo|up|fx)', 'r"(\w+)\.(lo|up|fx)')`, applied once. The quoted old body matches the current file everywhere else, including the 3 blank lines before `parse_gms`.
  - Without the anchor, the pattern still requires `name.(lo|up|fx) = number;`. It therefore cannot match equation text (`=E=`) or `.l` level lines, and it now captures the second statement on each `x1.lo = 1; x1.up = ...;` line.
- **Independent recomputation.** I wrote `scratch-E/camshape_bounds.py`, my own statement-level parser that splits on `;`, evaluates rows exactly with Fraction, and applies the same QPLIB x_k to x_{k-1} shift. Output is in `scratch-E/camshape_bounds.log`. Bound counts per pair are 396/796/1596/3196, all finite, and the bounded-variable sets match.
  - Maximum relative bound difference (|a−b|/max(|a|,1)):
    - camshape100/2738: 1.741e-10 (x100.lo);
    - camshape200/2480: 2.420e-10;
    - camshape400/2703: **4.7078e-10 (x1.up, 1.00000982052922 vs 1.000009821)**;
    - camshape800/3177: **2.4970e-10 (x1.up)**.
  - The overall maximum is 4.7e-10 and QPLIB_3177 alone is about 2.5e-10. Both match the report and the summary.md integration cell. The reviewer's pure-relative metric gives the same maxima (`lit-control-r2/bound_rel.log`).
  - QPLIB points against MINLPLib's r1 upper bound: 2480 violates it by 2.481e-11 and 2703 by 4.7078e-10. This matches report line 192.
- **Problem (minor): stale log and README.**
  - `literature/control/checks/qplib_camshape_compare.log` (mtime Oct 2 19:28) was not regenerated after the regex fix (script mtime Oct 3 21:32). It still shows the pre-fix lower-bound-only output:
    - maxima 1.741e-10, 2.420e-10, 1.939e-10 and 3.802e-11;
    - the 2703 QPLIB point "max violation in MINLPLib model = 8.921e-11 (e658)", which with upper bounds is 4.7078e-10 at x1.up.
  - `checks/README.md` (revision-1 block) still says "(all <= 2.5e-10)".
  - report.md:172 cites `checks/qplib_camshape_compare.py` for 4.7e-10. The corrected numbers are logged only in `checks/minor_review_check.log`.
  - Fix: rerun `qplib_camshape_compare.py` for the four pairs to refresh its log, and change the README to "≤ 4.7e-10 (QPLIB_3177 ≈ 2.5e-10)".

### 2.2 Waki Table 12: OK

`pdftotext -f 33 -l 33 sources/papers_rev1/waki2004_oo988.pdf` shows Table 12 on PDF p. 33, printed p. 31 (the page footer reads 31; problem (39) is on printed p. 30, PDF p. 32).
- Rows M = 600–1000.
- ε_feas values: −2.2e-10, −8.1e-10, −1.6e-10, −6.8e-10, −2.7e-10.
- CPU 3.3–5.0.

No "M ≤ 1000", "up to 1000" or "<= 1000" remains, except the quotation of the issue in the response row.

### 2.3 Müller camshape100 page: OK

In arXiv 1912.00356v1, PDF p. 40 (footer 38) carries the Table 4 camshape100 row: −4.28415 / −5.0295 / −4.92812 / −4.90792. PDF p. 41 has camshape200–800, and lnts50 is on p. 46. The body (line 238) and the bibliography ("pp. 40–41, 46, 58") are both corrected, and no other "p. 41" remains.

### 2.4 Spurious camshape800 closure: OK

The four MINOTAUR logs, all `v0.4-50-g456fd8cc`:
- **3177:** nodes processed = 1; best bound estimate from remaining nodes = inf; time used = 2.89; "Optimal solution found".
- **2738, 2480 and 2703:** "Reached time limit" at 10800.02, 10800.08 and 10800.11 s; bounds −4.5374, −4.8494 and −5.1678.

The definition of "false under exact feasibility" and the QPLIB-copy caveat are present (lines 189–191). COPT 3177 "quadratics 2.98281e-08" is confirmed in QPLIB_3177.cop.
- Nit: the gaps 5.9%/13.3%/20.8% are not printed. The logs give absolute gaps 0.2532/0.5707/0.8913, and I recomputed the relative values as 5.91/13.34/20.84%. The report could say "relative gaps computed from the logged absolute gaps".
- Nit: the bottom line (line 28, "so the claim is false") does not repeat the exact-feasibility qualifier, though line 29 points to Section 3.

### 2.5 MINOTAUR dtoc5 default bounds: fix present; minor problem with the inference

Checked:
- `sources/QuadHandler_master_r2.cpp` equals `reviews/lit-control-r2/web/minotaur/QuadHandler.cpp` (cmp).
- The reference point `sources/qplib/QPLIB_8585.sol` has sha256 9d9f5c4f…, which equals the r2 SHA256SUMS. My own read gives 99998 entries; max |x| is x2 = 8.057243524908399; all entries are positive (min 1.46e-5).

Problem (minor):
- **(a) The rule is misdescribed.** `addDefaultBounds` (lines 184–237) does not use "the largest applicable finite bound magnitude":
  - the lower default comes from the **smallest finite lower bound** m: 100·m if m < −aTol, −100·m if m > aTol, otherwise −1000;
  - the upper default comes from the **largest finite upper bound**, with the mirror-image rule.
  - The wording came from the r2 review. For a sole bound of 1 both readings give [−100, 100].
- **(b) "Sole finite bound x50001 = 1" is not what the rule saw.**
  - In dtoc5.gms (`solver-runs/gms/dtoc5.gms`, textually identical to QPLIB_8585), 99998 variables occur in sqr terms (all except x100000), and the only bound in the model is `x50001.fx = 1`. Without presolve changes, both warnings should therefore count 99997.
  - The log has 99997 upper, which is consistent, but **99983 lower**. So 14 more quadratic variables had finite lower bounds, presumably presolve-derived, when the rule ran. Their values, and hence the lower default, are unknown even for master.
  - The containment conclusion still holds. The rule always yields a negative lower default (m > aTol gives −100m; otherwise 100m < 0 or −1000), and every reference coordinate is positive. The upper default is ≥ 100·1 provided x50001's bound is still present.
- **Locations:** report.md:296 ("scales the largest applicable finite bound magnitude… sole finite bound … this gives [−100, 100]"), :531, :698 and response row 2.5. In summary.md row 2.5 the integration cell should also mention this caveat.
- **Fix:** describe the rule as above. State that the upper default is consistent with 100, that the lower default is not determined (the log shows 14 extra finite lower bounds at that point), and that the reference point lies in any box the rule can produce, because the lower default is always negative and the point is positive with max 8.06.

### 2.6 "MINLPLib optimizer" wording: OK

My own evaluation gives MINLPLib p1 (`open-instances/minlplib_sol/camshape800.p1.sol`) a max row violation of **3.9132e-10 at e1562** in MINLPLib camshape800, and 5.0613e-10 (e1314) in QPLIB_3177. This matches lines 191–192. "MINLPLib optimizer" no longer occurs.

### 2.7 CONOPT 8.7e-6: OK

QPLIB_2738.ant line 248 reads `0   0   8.7007237331E-06 (Input point)` under the column header "Infeasibility". All four mentions are reworded as an aggregate Infeasibility for the input point, with the incumbent identity stated as inference: report lines 54, 180, 370 and 586. No "infeasible by 8.7e-6" remains.

### Collateral (diff before/literature__control.txt against report.md)

Every hunk matches an issue; no numbers changed without an explanation, and no deletions were lost. Other observations:
- report.md:704–705: no blank line before `## Response to review` (it renders, but it is cosmetic).
- Lines 190 and 697 still say QPLIB_3177 is rounded "at the 2e-10 relative level" or "about 2e-10". The true figures are 1.2e-10 for coefficients and 2.5e-10 for bounds. This is acceptable as an order of magnitude; nit.
- `report.prev.md` is the original round-0 partial report (mtime Oct 3 21:27, before the author's session). It is untouched by the fixes and nothing links to it. It is stale, so it should not be mistaken for current text.
- `sources/MANIFEST.md` has a new "Minor-review revision (2026-10-03)" block with correct hashes for `QuadHandler_master_r2.cpp` and `qplib/QPLIB_8585.sol`.
- summary.md rows 2.1–2.4, 2.6 and 2.7 are correct. For row 2.5, see above.

## literature/network (review: reviews/lit-network-review-r2.md, Section 2)

### 1. Cumene source versions: OK

The saved dissertation equals the r2 copy (`cmp` of `schweidtmann2021_dissertation.pdf` against `rwth820314_wayback20260128.pdf`).
- **Dissertation:** Table 2.8 is on PDF p. 43, page footer 29. It gives F3 4,671,260 / 2930; envelope 6,329,810 / 444; envelope* 10,033,800 / 328; BARON 1·10^20.
- **arXiv v2:** Table 4 is on PDF p. 21 and gives 4,772,133 / 1·10^11, 5,683,103 / 8·10^10 and 12,939,508 / 1·10^5. Fig. 6 is on p. 22.
- **Front matter:** "Chapter 2 is based on parts of [1]" and "Reprinted from … JOTA" are present.

The body (lines 48 and 300–305), Section 8 (line 358), Section 9 (line 384) and the bibliography all keep the two versions distinct and leave the JOTA table unchecked.
- Nit: summary table line 74 still says "Schweidtmann & Mitsos 2019 … their Table 4" and "In the source paper no method converged". This is harmless, because both versions agree on non-convergence.

### 2. Nonclosing benchmarks: OK, with a minor citation imprecision

- **SCIP Suite 8.0** (`literature/control/sources/scip80_suite_arXiv2112.08872v1.pdf`):
  - PDF p. 105 has powerflow0030r ∞ / 0.54% and powerflow0039r >1000% / 0.23%;
  - PDF p. 112 (footer 112) has waterno2 06 326%/128%, 09 >1000%/321%, 12 >1000%/571%, 18 >1000%/638% and 24 >1000%/750%.
  - These match lines 114 and 268.
- **Göß** (arXiv 2603.16505v1, PDF p. 32): Table 4 row "powerflow0039p min PARA 10−4 limit 4.0e2 4.0e2 9.90 9.90". This matches.
- **Müller–Serrano–Gleixner** (arXiv 1903.05521v2):
  - **Problem (minor):** only Table 5 (PDF pp. 69 and 72) shows t = 1800.0 in all three settings, for powerflow0030r/0039r and waterno2_04–24 (waterno2_03 is solved).
  - pp. 42 and 48 are Table 3 (separation statistics) and pp. 56 and 59 are Table 4 (root gap closed). Neither shows a time limit.
  - Lines 114 and 268 cite "pp. 42,48,56,59,69,72" for the time-limit statement. Fix: cite Table 5, pp. 69 and 72, for the time limit; the other pages only list the instances. The reviewer's text has the same imprecision.
- **Problem (minor/nit):** line 61 (summary table) says "Göß et al. 2026". The paper has a single author, Adrian Göß; the bibliography and line 114 correctly say "Göß".
- The JOGO SCIP 8 qualification is present (lines 268 and 347).

### 3. Oustry et al.: OK, with one stale sentence

The paper and table were checked in the saved sources (`oustry2022_pscc22.txt`, `oustry_table_of_results.txt`):
- PGLib-OPF v21.07, "typical operating conditions (TYP)";
- certified LB 803.127 (case30_as), 7896.87 (case30_ieee) and 137254 (case39_epri);
- Crossref (saved JSON) gives Electr. Power Syst. Res. 212:108278 and the four authors;
- the HAL id hal-03613385 is confirmed.

The report cites it in Sections 1, 8 and 9 and in the bibliography.
- **Problem (minor, stale text):** report.md:135 (Section 3.2 consequence) still says 'Present ours as "the first rigorous certificate"' without "for this MINLPLib model". Lines 30, 60 and 368 carry the qualifier, and the response row says first-rigorous claims were restricted. Fix: add the qualifier at line 135.

### 4. 0030p/0030r rounding: OK

I grepped the whole report for transport claims ("same data", "any dual", "maps to a feasible", "transfer", "transport", 576.8934126255):
- lines 28, 60, 121–123, 369 and 428 (the r1 history row) are all corrected;
- line 132 ("ANTIGONE established the optimum … in floating point, on the twin 0030r") is an FP statement, not exact transport. A nit: it could add "at solver tolerance".

Coefficients, counted in the r2-saved GAMS files:
- 0030p stores 1.86832740213523 (6 occurrences);
- 0030r stores 1.86832740213523 (20 occurrences) and 0.934163701067616 (16 occurrences).
- 2 × 0.934163701067616 = 1.868327402135232, which differs from 525/281 at the 16th significant digit.

The attribution to r2 is correct.

### 5. Huang Table 5.2: OK

The table is in `huang2019_dissertation_wayback20240414.txt` lines 6844–6874 (printed p. 126). The source is the TU Darmstadt dissertation, Wayback copy 2024-04-14.
- Extended column: P[0,5] gap 0.000470589 (gap limit 1e-5 per p. 125); P[0,6] 0.178792 is the minimum and P[0,23] 1.14263 the maximum over 6–24, giving 0.18–1.14.
- Original column: 3-period 215/215 against MINLPLib 115.0045. Extended 1- and 2-period values: 19.38 and 39.5.

The 343.41 argument is withdrawn (line 265), the summary-table gaps are labelled "extended-model", and line 39 is correct.

### 6. Bibliography: OK

I checked titles and authors against the saved PDF headers for Bingane, D'Ambrosio, Geißler, Ghaddar, Josz, Kocuk, Lavaei, Li, Molzahn, Vigerske, Wilhelm, Izquierdo González, both Karia entries, Müller–Serrano–Gleixner, SCIP 8 JOGO, the SCIP Suite 8.0 report and Oustry.
- Li et al.: the six authors match (Owen Li, Daniel Ovalle, Barnabas Poczos, Carl D. Laird, Ignacio E. Grossmann, Javier Peña), and so does the title.
- Carrasco–Muñoz: no saved source, so I read the public arXiv API. The title matches, and v2 was updated 2026-03-30, so "v2 (2026; first version 2024)" is correct.
- VSDP: the optimization-online 1047 preprint title and authors (Jansson, Chaykin, Keil) are correct, and both tuhh URLs return 200. Nit: the body (line 362) links `/vsdp/` while the bibliography links `vsdp_cj.html`.
- The saved Crossref JSON has errors for 7 of the 15 DOIs (6 × 429, 1 × 404), as commands.md states.

### 7. KAN tolerance: OK

- Karia arXiv PDF p. 16 (footer 16) says only "default gap tolerance of zero" and "time limit of 2 hours".
- `sources/zenodo_kan/ex/kan_effect_neurons/Default/R3_H1_N4.log` shows "reading user parameter file <scip.set>" followed only by `limits/time = 7200`, with SCIP 9.0.1.
- The report says the tolerance is inferred (line 169). Nit: it says "Default logs" in the plural, but only the R3_H1_N4 log is cited and checked.

### 8. Stale text and duplicate commands: OK

- The introduction and the first open-issue bullet are updated.
- The deleted list "Commands run (from the agent's structured return)" is fully covered item by item by Section 12, "Revision (2026-10-02)". The only items lost are two sha256 prefixes (5998d8bc…, 33fa04a3…), which are immaterial. Section 12 is retained.

### 9. Unobtained sources: OK

- Line 14 says "Three sources remain unobtained": Huang 2011, the Sept 2013 Hijazi report and the AIChE abstract, all listed in Section 8 (lines 355–359).
- The Schweidtmann dissertation is marked obtained.

### Collateral (diff before/literature__network.txt against report.md)

Every hunk maps to an issue, with no unexplained number changes and no lost content. Other observations:
- The header comment changed from "Status: partial" to "Status: complete". This is OK.
- Section 7 ("Checks run by this track") does not list the new `checks/minor_review_check.py`, although the response section does (nit).
- MANIFEST: all 103 hashed rows match (own script), including the new 2026-10-03 block. The origin column contains absolute /home paths, which are path-only and ignored.
- summary.md rows 1–9 for network: the integration cells are correct. Row 3 could add that line 135 still needs the qualifier.

## Commands (all run by me; single process, seconds each)

```sh
cd P/reviews/minor-fixes-review-r1 && cat BRIEF.md && ls
cd P && cat reviews/minor-fixes-review-r1/PROGRESS.json; ls reviews/minor-fixes/; grep -n -i "literature/control\|literature/network\|lit-control\|lit-network" reviews/minor-fixes/summary.md; ls literature/control literature/network literature/control/checks literature/network/checks
wc -l reviews/lit-control-review-r2.md reviews/lit-network-review-r2.md literature/*/report.md literature/control/report.prev.md reviews/minor-fixes/before/literature__*.txt
diff -u reviews/minor-fixes/before/literature__control.txt literature/control/report.md
grep -n "8\.7e-6\|8\.7007\|M ≤\|2\.4e-10\|2\.5e-10\|2e-10\|4\.7e-10\|optimizer\|p\. 41\|default bound\|Table 12\|1\.6e-10\|2\.2e-10" literature/control/report.md
git status --short literature/; git check-ignore -v literature/control/report.md literature/control/checks/qplib_camshape_compare.py
find . -name "qplib_camshape_compare*"; grep -rl "def parse_gms" --include=*.py research-20260929
cat literature/control/checks/{qplib_camshape_compare.py,qplib_camshape_compare.log,minor_review_check.py,minor_review_check.log,dtoc5_reference_check.py,dtoc5_reference_check.log,README.md}
grep -rl "qplib_camshape_compare" ~/.codex/sessions/2026/10 ~/.claude/projects
python3 - (scan of ~/.codex/sessions/2026/10/03/rollout-...01a10487....jsonl for 'lo|up|fx' to recover the pre-edit script text and the edit command)
grep -n ... camshape_copies/*.gms (bounds layout, e1562, e1314, e801 rows); head of camshape800.p1.sol and QPLIB_2703.sol
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 300 python3 scratch-E/camshape_bounds.py | tee scratch-E/camshape_bounds.log
cat reviews/lit-control-r2/bound_rel.log
pdftotext -layout -f 32/33 -l 32/33 literature/control/sources/papers_rev1/waki2004_oo988.pdf - | grep ...
pdftotext -layout -f 40/41/46 mueller2019_arXiv1912.00356.pdf - | grep camshape/lnts50
grep -n -i "nodes processed|best bound|best solution value|gap =|time used|status of|Default|Minotaur version" literature/control/sources/mittelmann_cnconv/logs/QPLIB_{3177,2738,2480,2703,8585}.mnt
sed -n 170,190p QPLIB_3177.cop; sed -n 200,260p QPLIB_2738.ant
sed -n 184,237p literature/control/sources/QuadHandler_master_r2.cpp; cmp it with reviews/lit-control-r2/web/minotaur/QuadHandler.cpp
grep -n "\.lo\|\.up\|\.fx" solver-runs/gms/dtoc5.gms; python3 -c (count variables inside sqr() in dtoc5.gms: 99998 of 99999; only x100000 absent)
python3 -c (sha256, count, max/min of literature/control/sources/qplib/QPLIB_8585.sol)
grep MANIFEST.md entries (control and network); python3 manifest sha256 check of literature/network/sources/MANIFEST.md (103 rows, 0 bad)
diff -u reviews/minor-fixes/before/literature__network.txt literature/network/report.md > scratch-E/network.diff
grep -n (transport, first rigorous, Göß, Schweidtmann, JOTA, Carrasco) literature/network/report.md; sed of lines 30-40, 124-136, 314-336, 370-380, 440-490
grep -o coefficient counts in reviews/lit-network-r2/powerflow0030{p,r}.gms
pdftotext loops over scip80_suite (pp. 90-114), mueller2020_arxiv1903.05521.pdf (all pages), goss2026 p. 32 and p. 1
head/grep of oustry_table_of_results.txt and oustry2022_pscc22.txt; python3 summary of bibliography_metadata_20261003.json
head of the saved source texts (titles and authors); grep 2410.23362 in the Karia text
curl -s https://export.arxiv.org/abs/2410.23362; curl -s "https://export.arxiv.org/api/query?id_list=2410.23362"   # read-only
curl -s -o /dev/null -w '%{http_code}' for the two tuhh VSDP URLs and the optimization-online 1047 PDF; pdftotext of p. 1 (temp file deleted)
pdftotext -f 43 schweidtmann2021_dissertation.pdf; -f 21/22 schweidtmann2019_arxiv1801.07114.pdf; cmp with r2 copy
sed -n 6815,6880p huang2019_dissertation_wayback20240414.txt
grep of zenodo_kan/ex/kan_effect_neurons/Default/R3_H1_N4.log; pdftotext -f 16 karia2025_arxiv2503.02807.pdf
sed -n 79,121p reviews/minor-fixes/commands.md; cat literature/network/checks/minor_review_check.{py,log}
```

No solver, no main construction, no edits to track or author files, no git mutation, and nothing was submitted.
