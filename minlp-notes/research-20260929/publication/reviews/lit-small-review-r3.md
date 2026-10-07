Verdict: issues

# Review of track lit-small (round 3)

- **Reviewer:** independent verifier, review round 3. An earlier round-3 attempt was interrupted. I reused its verified results after a sanity check (see "Commands"), and did not repeat its work.
- **Date:** 2026-10-03.
- **Text reviewed:** `literature/small/report.md`, "Revised 2026-10-02 after review rounds 1 and 2" (fix round 2; Sections 16 and 17).
- **My files:** `publication/reviews/lit-small-r3/`. This folder holds my check code (`manifest_check.py`, `eg_mod_point_check.py`, `camino_gurobi_scan.py`), the logs in `logs/`, OpenAlex results in `openalex/`, new sources with a sha256 manifest in `sources/`, and `PROGRESS.json`.

## Summary

All round-2 issues are fixed, and the fixes are correct. I found no blocker and no major issue, and no consequence label changes.

- **R2-M1 (CAMINO / Gurobi 13.0.0) is fully fixed.** The report now describes Gurobi's bound = objective, reported before the time limit, as wrong optimality claims on eg_disc2_s, eg_disc_s and eg_int_s. It no longer calls CAMINO "primal values only". My own code (`eg_mod_point_check.py`) uses my own `.mod` parser, exact rational bound and integrality checks, and its own interval enclosure of `exp`. It confirms that the project's recorded points satisfy all 28 rows of each MINLPLib `.mod` model, with objectives 5.64210057997…, 5.76053961645… and 6.45310315938…. Gurobi's bounds exceed these objectives by 0.244594416, 0.431290231 and 5.201055875. All SCIP 9.2.2 bounds are valid. The author's added refinement is correct: `create_plot.py` counts a "success" without looking at the bound. The caveats are stated: the termination status is not recorded, the `.mod` copies are assumed current, and the cause is unknown.
- **All four round-2 minor issues are fixed.** Two of the new sentences contain small factual slips (issues 1 and 2 below).
- **My own searches found one source the report misses:** Cuesta et al. (arXiv 2026), which ran Gurobi 12.0.1, BARON 24.5.8 and COUENNE 0.5.8 on ex6_2_5 and ex6_2_7 (issue 3). It supports the existing labels.

## Status of the round-2 items

| item | status | my check |
|---|---|---|
| R2-M1 CAMINO / Gurobi | **fixed** | Paper pages (p. 26 setup; pp. 28–29 heuristic remark, time-limit rule, Table 3 caption; Table 8 pp. 49–51) confirmed by the earlier round-3 attempt. I re-read `using_amplpy.py` lines 105–136: options `bestbound=1 feastol=1e-8 mipgap=1e-2 threads=1 timelimit=…`; `obj` and `obj.bestbound` are recorded only if `solve_result` ∈ {solved, limit}. The eg rows of `noncvx_gurobi.csv`, `noncvx_scip.csv` and `noncvx.csv` and the limits in `wall_time_noncvx_sbmiqp.json` (32.6315, 19.2360, 212.6604 s) match every number in Sections 1, 9.2, 10.1, 11.1 and 12. My point check: see Summary. S-B-MIQP's 5.642100351878204 on eg_disc2_s is 2.22e-7 below the certified bound 5.642100574331458, as the report says. |
| Minor 1: CAMINO limits and versions | fixed | Sections 9.2, 10.1 and 11.1 give the 300 s limit for Bonmin, SHOT and S-B-MIQP(-ee), and the per-instance S-B-MIQP times for SCIP 9.2.2 and Gurobi 13.0.0. |
| Minor 2: Kosolap (2019) | fixed, with a new slip | The ex6_2_5 row is quoted correctly (n = 10, m = 3, EQR −70.9586, best known −70.75, GL; −70.75207783… − (−70.9586) = 0.2065). The added sentence about the other rows of the table is wrong; see issue 1. |
| Minor 3: eg_int_s old point and history | fixed, with one point left open | My interval check: the GAMS World point violates e12 by 6.367788e-9; all other rows, bounds and integrality hold; the smallest objvar meeting e1–e24 at that x is 6.4531031590678 (report: 6.4531031591). 6.4531031529331155 − 6.4531031527 = 2.3e-10. BONMIN 2008 logs: "28 rows 8 columns 220 non-zeroes", 196 NL nonzeros. The 2008 BARON/LindoGlobal model size is still called "presumably"; see issue 2. |
| Minor 4(a) hvycrash summary cell | fixed | It now lists COCONUT, Smith, SOLTN(100/500/1000) and Omheni −0.18 to 1.1e-19. |
| Minor 4(b) "c_k" | fixed | Section 3.1 now reads U(1..50) = x51..x100 ∈ [0.08, 0.417]. |
| Minor 4(c) pricing bounds page | fixed | Formula (9) is on p. 15 and [l, u] = [0, 10] on p. 16. |
| Minor 4(d) paraboloids README and option files | fixed | Section 9.2 cites README line 38 and the contents of `scip.opt` and `gurobi.opt`. The copies are in `sources/eg/paraboloids_repo/`, and their hashes match the manifest. |

## Issues

### 1. minor — Kosolap (2019) Table 1: "every one of the nine EQR values lies below" is wrong

- **Location:** Section 5.2 (Kosolap bullet: "Every one of the nine EQR values in the same table lies below its listed 'best glob. min.'"). Section 12, item 8 ("Every EQR value in that table lies below its listed best known value"). Section 17, minor-issue table, row 2.
- **Evidence:** I rendered PDF p. 4 of `sources/kosolap/kosolap2019_acps_4-1_32.pdf` at 200 dpi and read the table image.
  - Table 1 has **15** rows: Egg Holder, Rana, Nie ×4, meanvar, G16, Charles_Audet, Ex7_3_5, Ex8_4_7, Ex6_2_5, Ex2_1_8, Haverly and Harker.
  - The G16 row prints EQR **1.914608** against a best known value of **−1.9046617**. As printed, this EQR value lies *above* the best known value.
  - The other 14 EQR values lie below their listed best known values.
- **Suggested fix:** "14 of the 15 EQR values in the table lie below the listed best known value. The exception is G16, printed as 1.914608 against −1.9046617, possibly with a lost minus sign." This does not affect the ex6_2_5 finding.

### 2. minor — The 2008 BARON and LindoGlobal model size is recorded in the saved trace files; "presumably" is unnecessary

- **Location:** Section 9.1, "Row count" ("The BARON and LindoGlobal runs of the same 2008 benchmark … presumably used the same model files. Their logs are not online"). Section 17, minor-issue table, row 3.
- **Evidence:** The trace files the report already saved, `sources/coinor_2008/BARON-2.trc.canall` and `LINDOGLOBAL-1.trc.canall`, contain one record per eg_* instance. Each record lists 28 equations, 8 variables, 220 nonzeros and 196 nonlinear nonzeros. Example: `eg_int_s,MINLP,BARON2,2,0,28,8,3,220,196,8,3,6.45310315899,-8.080703459,…`. The full logs are missing, but the model size is on record.
- **Suggested fix:** "The trace records of the BARON and LindoGlobal runs list the same size (28 equations, 8 variables, 220 nonzeros, 196 nonlinear nonzeros), so their values refer to the current model."

### 3. minor — Missed source: Cuesta et al. (2026) ran current global solvers on ex6_2_5 and ex6_2_7

- **Location:** Sections 4.2 and 5.2, and the references. Possibly also the "Search coverage" bullet in Section 13.
- **Source:** M. Cuesta, C. D'Ambrosio, M. Durbán, V. Guerrero and R. Spencer Trindade, "On leveraging constrained smooth additive regression models for global optimization", arXiv:2510.14122v3 (8 Sep 2026; v1 15 Oct 2025). Saved as `reviews/lit-small-r3/sources/cuesta_et_al_arxiv2510.14122v3.pdf` (sha256 b740fcc0…).
- **Setup (Section 6):** Gurobi 12.0.1, BARON 24.5.8 and COUENNE 0.5.8, with a 600 s limit and default settings. The gap is 100·|UB − LB|/|UB| (eq. (32)). The instances were taken from the Bertsimas & Margaritis test set because Gurobi 12.0.1 "cannot solve [them] in 600 seconds".
- **Results (Table 5, "MINLP solver" rows):**

  | instance | solver | value | time | gap |
  |---|---|---|---|---|
  | ex6_2_5 | Gurobi | −70.599 | 600.3 s | 345.257% |
  | ex6_2_5 | BARON | −70.752 | 603.0 s | 203.848% |
  | ex6_2_5 | COUENNE | −70.752 | 607.0 s | 1386.825% |
  | ex6_2_7 | Gurobi | −0.161 | 600.6 s | 2400.913% |
  | ex6_2_7 | BARON | −0.161 | 603.0 s | 1359.993% |
  | ex6_2_7 | COUENNE | −0.161 | 607.3 s | 10913.441% |

  The text notes that MINLPLib does not mark these instances as solved to global optimality.
- **Effect:**
  - No label changes. The implied dual bounds, for example about −215 (BARON, ex6_2_5) and about −2.35 (BARON, ex6_2_7), are far below the certified values, so nothing conflicts with them.
  - This is the most recent run of current commercial and open-source global solvers on these two instances. It strengthens "no rigorous certificate was found; current solvers do not close the instance". It also contrasts with the Bertsimas & Margaritis BARON "GOpt" label, although the time limits differ (600 s here, 1500 s there).
- **Why it was missed:** OpenAlex full-text search does not index this arXiv paper; my OpenAlex `search=ex6_2_7` (from 2024) returned 0 hits. A WebSearch for "ex6_2_7" with arXiv found it.
- **Suggested fix:**
  - Add one bullet each to Sections 4.2 and 5.2 and an entry in the references.
  - Optionally, add a sentence in Section 13 that recent arXiv preprints are not covered by OpenAlex full-text search.

### 4. minor — "61 other instances" with a genuine bound ≠ objective includes two placeholder bounds

- **Location:** Section 9.2 (Gurobi data bullet: "on 61 other instances that stopped early, it differs from the objective"), Section 14.3 (CAMINO scan) and Section 17 (R2-M1, "Data re-fetched").
- **Evidence:** My scan (`camino_gurobi_scan.py`; "early" means time < 0.99 × the per-instance limit) gives:
  - 32 early runs with bound = objective, among them the three eg_* runs;
  - **59** early runs with a finite bound ≠ objective;
  - 2 early runs with bound ≥ 1e99 (eg_all_s and hadamard_9, the AMPL placeholder for "no bound");
  - 4 failed runs and 165 runs at the limit.
  
  The total matches the report's 61, but two of those runs carry no real bound.
- **Effect:** None on the conclusion. 59 runs still show that the column holds a genuine bound.
- **Suggested fix:** "on 59 other instances that stopped early, it is a finite value different from the objective (two more report the placeholder 1e100)".

## Spot checks of other claims (all confirmed)

- **Manifest:** re-run on 2026-10-03: 128 rows, 128 distinct paths, 0 bad hashes, 0 missing, 0 unlisted.
- **Percentages:** 0.2446/5.6421 = 4.3%; 0.4313/5.7605 = 7.5%; 5.2011/6.4531 = 80.6%, which the report gives as 81%.
- **Göß et al. Table 17 and the paraboloids repository:** confirmed in rounds 1–2 and unchanged.
- **COIN-OR 2008 values in Sections 9.2, 10.1 and 11.1:** BARON 6.45310315899 / −8.0807, 5.76053961645 / −8.0807 and 5.93701554196 / −8.0807; LindoGlobal 7.4631 / −3.1577, 5.76053961646 / −7.3125 and 5.64210057997 / −9.9793. These match the saved trace files.
- **Section 1 side findings 6–8 and Section 12 items 7–9:** the numbers agree with Sections 9–11 and with my own computations.

## My own literature searches

No source found changes a consequence label. Besides issue 3:

- **WebSearch (10 queries):**
  - "ex6_2_5" OR "ex6_2_7" rigorous interval 2023–2026;
  - "eg_int_s" OR "eg_disc_s" OR "eg_disc2_s" global optimum (extended);
  - Kiaghadi dissertation and decision diagrams for pricing (two variants);
  - exact or verified MINLP in SCIP;
  - "pindyck" OR "etamac" global optimality 2024–2026;
  - ethylene glycol – lauryl alcohol – nitromethane UNIQUAC global Gibbs;
  - Gurobi 13 wrong optimum, AMPL, exp;
  - arXiv "ex6_2_7" OR "ex6_2_5" BARON Gurobi 2026 (extended; found Cuesta et al.);
  - "hvycrash" OR "pricing050" OR "eg_disc2_s" 2025–2026 (extended; no relevant hits).
- **OpenAlex** (`search=`, publication date ≥ 2024): "minlplib open instances closed", "rigorous dual bound minlplib", "verified global optimization minlplib", "certified global optimum mixed-integer nonlinear interval arithmetic benchmark", "ex6_2_7" (0 hits), "eg_int_s" (SHOT thesis, CAMINO). The earlier round-3 attempt ran full-text queries for all nine names; every relevant hit is already in the report.
- **Read and found not relevant** (none mentions the nine instances, or the instances appear only as unsolved):
  - Liberti, Nannicini & Mladenović, "A good recipe for solving MINLPs": eg_disc_s, eg_int_s and eg_disc2_s are in Table 3, "Instances unsolved by RECIPE".
  - Bertsimas & Öztürk, arXiv 2202.06017.
  - Göß, arXiv 2603.16505 (confirms the report: no eg_* entry).
  - Davarnia, Kiaghadi & Qiu, GlobalDD arXiv v1 and v2 and optimization-online R1: no pricing instance in any version. The optimization-online v1 file returned "Page not found".
  - Kosolap, JNAM 2025.
  - Zhu, He & Tawarmalani, arXiv 2603.18458.
  - Araya, Messine, Ninin & Trombettoni, J. Glob. Optim. 91 (2025) 437–456: COCONUT series 1–2, aggregate results only, no instance names.
  - RAPOSa MINLP, arXiv 2410.17949.
  - Szeider, CP 2026: VIPR certificates for ILP only.
  - Earlier round-3 attempt: Vanaret thesis and CP 2015 (Charibde; 11 COCONUT problems, not ex6_2_5/7), Neveu, Trombettoni & Araya JFPC 2015 (ex6_2_6/8/9/10/11/12 only), Lundell 2020 SHOT benchmark data (none of the nine).
- **Not used:**
  - Gurobi community thread 41172002380433 (Najman, staff, June 2026): Gurobi 13 returned different "globally optimal" values on a user's nonconvex model; tightening the tolerances fixed it. This is context only. It is not evidence about the CAMINO eg_* runs, and the report is right not to guess the cause.
  - A UdeC (Chile) study of ethylene glycol + 1-dodecanol + nitromethane at 295.15 K (snippet only; NRTL and UNIFAC, not the handbook UNIQUAC model).

## Cross-track notes (not issues for this track)

- **eg_all_s:** in the same CAMINO data, Gurobi 13.0.0 recorded objective 0 and bound 1e100 after 1.63 s, against a limit of 40.58 s. If another track covers eg_all_s, this anomalous record is worth a look.
- **Kosolap:** the same author has a 2025 JNAM paper and a 2026 Springer chapter on "difficult multimodal problems". The 2025 paper does not mention any of the nine instances. The 2026 chapter was not read; it has no open-access copy.

## Commands I ran

All runs used one process (at most one core), with no background jobs. No project-wide checks were run and CI was not inspected. Nothing was committed, posted or sent.

**Earlier round-3 attempt (2026-10-02; reused after a sanity check, logs in `lit-small-r3/logs/`):**
- `python3 manifest_check.py ../../literature/small/sources` → 128 rows, 0 bad, 0 missing, 0 unlisted.
- `python3 eg_mod_point_check.py`: own `.mod` parser, exact bound and integrality checks, interval rows. Results are in the Summary and under minor 3 above.
- A Python scan of `noncvx_gurobi.csv`; `sed` of `create_plot.py` lines 631–658; `pdftotext` of CAMINO v2 pp. 26, 28, 29, 49 and 51; Kosolap Table 1 text; `grep` of the 2008 trace files.
- OpenAlex full-text queries for the nine names (`openalex/ft_*.json`, `logs/openalex_fulltext.log`); `curl` of the four saved sources in `sources/manifest.tsv` and `pdftotext`/`grep` of them.

**This session (2026-10-03):**
- `cat` of `PROGRESS.json` and logs; `cat` of `reviews/lit-small-review-r2.md` and `literature/small/report.md`. `diff report.prev.md report.md` (`report.prev.md` is the round-0 text) and `ls --time-style=full-iso`.
- `python3 manifest_check.py ../../literature/small/sources` → 128 rows, 0 bad, 0 missing, 0 unlisted (`logs/manifest_check_rerun_20261003.log`).
- `pdftotext -layout -f 4 -l 4` and `pdftoppm -f 4 -l 4 -r 200` of the Kosolap PDF; cropped with PIL and viewed the image (issue 1).
- `grep` of `sources/coinor_2008/*` for the eg_* records (issue 2).
- `head`, `grep` and `sed -n 115,160p` of the CAMINO files (`noncvx.csv`, `noncvx_gurobi.csv`, `noncvx_scip.csv`, `using_amplpy.py`, `wall_time_noncvx_sbmiqp.json`).
- `python3 camino_gurobi_scan.py` (`logs/camino_gurobi_scan.log`; issue 4).
- `grep -n` of `report.md` for the old wording ("c_k", "near-zero", "primal only", "presumably", "every one of the nine").
- `grep` of the Blomqvist thesis text extract for eg_* (test-set list only, line 3721).
- `curl` (sequential, about 1 s apart), then `pdftotext`/`grep` for the nine names:
  - recipemh.pdf (LIX);
  - arXiv 2202.06017, 2603.16505, 2409.19794 (v2 and v1), 2510.14122 (v3, saved), 2608.22815, 2410.17949 and 2603.18458;
  - optimization-online Global_DD.pdf (404 page) and Global_DD_R1.pdf;
  - the CP 2026 LIPIcs PDF;
  - jnam.knu.ua article 206;
  - the Araya et al. 2024 PDF: HAL and Springer served HTML pages to a browser user agent, the PDF to `curl/8.5.0`. HAL API metadata query; Wayback availability API (no snapshot).
- arXiv abs page of 2510.14122 (versions).
- OpenAlex: 6 `search=` queries with `from_publication_date:2024-01-01` (`openalex/search_*.json`, `logs/openalex_search_2024plus.log`) and 4 DOI look-ups.
- WebSearch: the 10 queries above. WebFetch: two Gurobi community threads and one HAL page (access denied).
