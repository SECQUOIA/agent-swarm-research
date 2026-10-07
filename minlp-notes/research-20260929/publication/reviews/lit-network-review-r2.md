<!-- Written to disk by the root from the structured return value of verifier round 2 of track lit-network in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review of track lit-network (round 2)

Reviewer: independent verifier, round 2. Date: 2026-10-02.

Two agents worked in this role. The first was cut off by a usage limit while writing its review. I read its transcript, checked its code and logs, reran its scripts (each output is identical to its log), and then continued the work. Files for this round are in `publication/reviews/lit-network-r2/` (scripts, logs, `PROGRESS.json`, and newly found sources in `sources_r2/`). Cores used: at most 1 at a time.

**Verdict: verified, with 9 minor issues.**

- All 3 major and 6 minor issues of round 1 are resolved.
- I found no error that changes any instance's status ("partly known" for powerflow0030p and ann_cumene_tanh; "new as far as found" for powerflow0039p/r, waterno2_06–24 and kan_r3_h1_n9/kan_r5_*; "prior FP claim contradicted" for kan_r3_h1_n4/n5).
- New searches found five sources the report does not cite. None closes a gap on our 15 instances.
- One of them, Schweidtmann's 2021 dissertation, says it reprints the cumene source paper (JOTA). It gives MAiNGO results that differ from the arXiv preprint numbers the report quotes (minor issue 1).

## 1. Round-1 issues

| # | round-1 issue | status in the revised report | how I checked |
|---|---|---|---|
| M1 | ann_cumene_tanh: missed the identical twin ann_cumene_exp, which is closed in FP | Resolved. Status is "partly known" in Sections 1, 2, 6 and 9. The note to correct "the first finite dual" in `open-instances-summary.md` is passed on for integration (that file still says it; it is outside this track). | Reran `cumene_twin_r2.py` (own OSIL comparison): 250 nonlinear rows are −tanh(v) versus 2/(exp(2v)+1) with the same v and both bounds raised by exactly 1; the other 540 rows, the variables, the objective, and the linear and quadratic coefficients are identical. Re-parsed the MINLPLib pages: duals for ann_cumene_exp are SCIP −3379.982394, LINDO −3379.982394, BARON −3379.985774 and ANTIGONE −73920.54157; primal −3379.982394; the tanh page lists no dual. |
| M2 | powerflow0030p: shunts dropped; loads and shunts not checked | Resolved. Provenance is corrected, and an exact loads/shunts check was added. | `pf_loads_shunts_r2.py` (own parser, exact rationals, MATPOWER case30 fetched separately): the 60 balance-row right-hand sides equal the multiset of −Pd/100 and −Qd/100; no balance row is nonlinear; all 150 sqr(V) coefficients are pure branch quantities; 0.0019 and 0.0004 do not occur. `pf_taps_r2.py` on 0039r/0039p (GAMS files fetched separately): for 11 tapped branches only the untapped admittances occur; branch 23–36 has τ = 1; case39 has no bus shunts. |
| M3 | report.md missing or truncated | Resolved. `report.md` is on disk: 507 lines, with Sections 1–12, the per-instance sections, the search log and the commands. | Read in full. |
| m1 | Cite the June 2014 Hijazi et al. revision | Resolved: Section 3.1, pp. 16–18. | grep of the source text: Table 3 has rows 5/6 "576 … 0.57% … 0.00%" and row 8 "41864 … −0.06%"; the "non valid lower bound" sentence is on p. 18. |
| m2 | NESTA and Bingane for case39 | Resolved (Section 3.3). | The first r2 agent's grep of the source texts confirmed the values. |
| m3 | BARON/MAiNGO wording for cumene | Resolved against arXiv v2. But see minor issue 1. | arXiv v2 Table 4, p. 21: BARON 1·10^20 for F1–F4; MAiNGO F3 1·10^11, envelope 8·10^10, envelope* 1·10^5. |
| m4 | KAN check not independent | Resolved: labelled as such, and the r1 reproduction is cited. | — |
| m5 | Huang 2019 unread | Resolved: read from the Internet Archive copy; the network is identified. | Own counts: the four Example 5.41 coefficients occur 2, 4, 6, 8, 12, 18, 24, 36, 48 times in waterno2_01, 02, 03, 04, 06, 09, 12, 18, 24, i.e. 2 × T. Table 5.2 values re-read (Section 3.3 below). |
| m6 | "first bound … as listed" ambiguous | Resolved. | — |

## 2. Minor issues

1. **The cumene source-paper numbers may not be the published ones.**
   - **What the report quotes.** Sections 1, 2 and 6 cite Schweidtmann & Mitsos, JOTA 180(3):925–948 (2019), but quote arXiv:1801.07114v2. Table 4 there (p. 21) gives MAiNGO results after 1e5 s:

     | MAiNGO run | iterations | absolute gap |
     |---|---|---|
     | F3 | 4,772,133 | 1·10^11 |
     | envelope | 5,683,103 | 8·10^10 |
     | envelope* | 12,939,508 | 1·10^5 |

   - **What the dissertation says.** Schweidtmann, "Global Optimization of Processes through Machine Learning", Dissertation, RWTH Aachen, 2021, DOI 10.18154/RWTH-2021-05536. I read the Internet Archive copy (2026-01-28) of `publications.rwth-aachen.de/record/820314/files/820314.pdf`. Its front matter says that Chapter 2 "is based on parts of" the JOTA paper and lists it as "Reprinted … with permission". Section 2.4.4, Table 2.8 (printed p. 29, PDF p. 43) gives:

     | MAiNGO run | iterations | absolute gap |
     |---|---|---|
     | F3 | 4,671,260 | 2930 |
     | envelope | 6,329,810 | 444 |
     | envelope* | 10,033,800 | 328 |

     The BARON rows are unchanged (1·10^20).
   - **Unresolved.** I could not open the JOTA full text: the Springer page and its 2024-07-07 Internet Archive copy show only a preview. So which numbers the journal prints is unresolved.
   - **Effect on status: none.** In both versions no method converged, and MINLPLib's floating-point closure of the exp twin still stands. If the upper bound is near −3380, an absolute gap of 328 means an FP lower bound of about −3.7e3, still far weaker than our rigorous −3386.5403.
   - **Fix.** Attribute the 1e11/8e10/1e5 figures and the "Fig. 6, lower bound about −10^5" reading to arXiv v2. Add the dissertation's Table 2.8 values. Do not quote either set as "the JOTA result" until the publisher version is checked.

2. **Missed per-instance benchmark results (no closures).** Section 5.1 says the SCIP 8 paper's test set contains only waterno2_02 and waterno2_03, and Section 8 says "the SCIP 8 test set: none of our 15". That is true for the JOGO SCIP 8 paper (its test-set table lists waterno2_02/03). The following documents do report results on our instances, all FP and all at the time limit:
   - **SCIP Optimization Suite 8.0.** Bestuzheva et al., "The SCIP Optimization Suite 8.0", ZIB-Report 21-41, arXiv:2112.08872v1 (2021), Appendix A, "Detailed Computational Results to Section 4.14", pp. 93–112. Gaps for SCIP 7 / SCIP 8:
     - waterno2_06: 326% / 128%;
     - waterno2_09, _12, _18, _24: >1000% / 321%, 571%, 638% and 750% (p. 112);
     - powerflow0030r: ∞ / 0.54%;
     - powerflow0039r: >1000% / 0.23% (p. 105).

     (A copy is already in `literature/control/sources/`.)
   - **Müller, Serrano, Gleixner**, "Using Two-Dimensional Projections for Stronger Separation and Propagation of Bilinear Terms", SIAM J. Optim. 30(2):1339–1365 (2020), DOI 10.1137/19M1249825; arXiv:1903.05521v2. Its per-instance tables (arXiv pp. 42, 48, 56, 59, 69 and 72) show waterno2_04–24 and powerflow0030r/0039r hitting the 1800 s limit in all settings.
   - **Göß 2026**, "Clash of MINLP Relaxations: Piecewise Linear vs. Global Parabolic", arXiv:2603.16505v1 (17 Mar 2026), Appendix B, Table 4, p. 32. It has a powerflow0039p row: "PARA, ε 10^-4, time limit, dual 4.0e2, rep. dual 4.0e2, gap 9.90%, rep. gap 9.90%". The row is not consistent with MINLPLib's values for 0039p (primal 41869.05, best dual 41818.28), and it closes nothing. The lit-control track cites this paper for lnts, but this track does not mention the 0039p row.

   Fix: add these sources to Section 8 and the relevant instance sections as "checked; time-limit FP results, no closure". Qualify the "SCIP 8 test set" sentences.

3. **Prior work on certified OPF bounds is not cited.**
   - **The paper.** Oustry, D'Ambrosio, Liberti, Ruiz, "Certified and accurate SDP bounds for the ACOPF problem", PSCC 2022 / Electr. Power Syst. Res. 212:108278 (2022), DOI 10.1016/j.epsr.2022.108278; HAL hal-03613385. It computes certified SDP lower bounds for PGLib-OPF v21.07 TYP cases.
   - **Its results table** (github.com/aoustry/dualACOPFsolver, "Table of results") includes:
     - pglib_opf_case30_as: certified LB 803.127, equal to the IPOPT value;
     - pglib_opf_case30_ieee: 7896.87;
     - pglib_opf_case39_epri: 137254.
   - **Effect on status: none.** These PGLib cases have different data from the MINLPLib models (optimal values 803.13 and 137254, against 576.89 and 41869.05). I did not check whether their computation controls rounding errors.
   - **Fix.** This is the closest prior work to our rigorous power-flow certificates. Cite it in Section 8 next to VSDP, and in the paper. State "first rigorous certificate" as "for these MINLPLib models".

4. **The 0030p/0030r twin is exact only up to coefficient rounding, and round 1 did not check it.**
   - **What the report says.** Section 3.2: "The rectangular twin 0030r has the same data as 0030p: the reviewer checked this … Every feasible point of 0030p maps to a feasible point of 0030r with the same cost." Round 1 checked only that 0030r has no shunt terms and has the listed bounds.
   - **What I found.** `pf_twin_exact_r2.py` compares the two models in exact rational arithmetic, under u_i = V_i cos θ_i, w_i = −V_i sin θ_i, at two random rational points:
     - the objective is equal;
     - 214 of the 391 rectangular rows equal polar rows exactly;
     - 60 voltage rows match through V² (0.9025 = 0.95², 1.1025 = 1.05², 1.21 = 1.1²);
     - the reference row w_1 = 0 corresponds to θ_1 = 0;
     - the other 116 rows differ from their polar counterparts by at most 1.03e-13, because the two files round coefficients differently.
   - **Example.** Branch 27–29 has b = 525/281 = 1.8683274021352314…. 0030p stores 1.86832740213523. 0030r stores 1.868327402135232 (8 times) and 1.86832740213523 (4 times).
   - **Effect.** The map holds only up to relative perturbations of about 1e-15. This does not matter for the FP closure through ANTIGONE. But it means, for example, that wave 3's rigorous 0030r bound (576.8934126255, higher than the 0030p certificate 576.8934122988) cannot be carried over to 0030p without a perturbation argument. Agreement at random points is strong evidence, not a symbolic proof.
   - **Fix.** Write "same data up to rounding in the 15th–16th significant digit (checked by reviewer r2)", and do not attribute the check to round 1.

5. **Huang Table 5.2: the extended-cut column is a different model, and one gap range is off.**
   - (a) **Extended-cut column.** With gap 0, the "with ext. pump cost rel. cons." column gives 19.38 (1 period) and 39.5 (2 periods), against 19.46 and 39.57 in the "original" column. So the extended model is not equivalent to Huang's original model. The sentence "Huang's 6-period dual, 343.41, exceeds waterno2_06's primal, 282.888. This confirms that they are different models" uses that column. It holds only if the extended model is a relaxation of the original, which the report does not establish. The 3-period mismatch (215 against 115.0045) already proves the point. Drop or qualify the 343.41 argument. Also mark the gaps in the summary table rows (0.18–1.03) as extended-model values (the note under the table already does).
   - (b) **Gap range.** Section 1, item 4: "None of the runs with 5 or more periods closed the gap; with the author's extra cuts, the relative gaps are 0.18 to 1.14." The 5-period extended run has gap 0.000470589, just above the 1e-5 limit. The range 0.18–1.14 holds for 6–24 periods.

6. **The bibliography is incomplete.**
   - **Missing titles.** Most Section 10 entries have no title: Bingane, D'Ambrosio, Geißler, Ghaddar, Gleixner, Gopalakrishnan, Izquierdo González, both Karia entries, Kocuk, Lavaei, Li et al., Molzahn, Schweidtmann, Vigerske and Wilhelm. Li et al. (arXiv:2604.03871) also has no authors.
   - **Missing entries.** Works cited in the body but absent from Section 10: Josz et al. 2015, Carrasco & Muñoz 2026, Mittelmann's benchmark page, the SCIP 8 paper, and VSDP (Jansson et al.).
   - **What is correct.** The DOIs, volumes and pages given are right. Crossref matches 13 of the 15 DOIs; the NACO and Vigerske DOIs resolve through doi.org. For Izquierdo González, Crossref says volume 6, but the PDF header and the DOI landing page say volume 5, as the report does.

7. **The KAN feasibility tolerance is inferred, not stated in the paper.** Section 4.1 attributes "SCIP's default 1e-6 feasibility tolerance" to p. 16 of the paper, which states only "gap tolerance of zero" and the 2 h limit. The Zenodo log `Default/R3_H1_N4.log` shows SCIP 9.0.1 reading only `limits/time = 7200` from `scip.set`, so the 1e-6 default applies. Say "inferred from the logs".

8. **Stale text.** The introduction (line 11) and the first "Open issues" bullet say report.md is not on disk; it now is. The appended section "Commands run (from the agent's structured return)" duplicates Section 12.

9. **Update the list of sources not obtained.**
   - The Schweidtmann dissertation can be obtained (issue 1).
   - Not obtained: the AIChE 2025 Annual Meeting abstract "Multi-layer perceptrons or Kolmogorov–Arnold networks…" from the KAN source group (proceedings.aiche.org; Cloudflare check; no Internet Archive copy). It may report further runs on Rosenbrock KAN surrogates. List it in Section 8 as not obtained.

## 3. What was verified

All of these are independent of the author's code. Scripts marked "r2" were written in this review role (most by the first r2 agent) and reran today with outputs identical to their logs.

### 3.1 Power flow

- **Loads, shunts and taps.** See M2 above.
- **Twin structure.** See minor issue 4.
- **Mapping search.** A floating-point mapping search (`pf_twin_check.py`) shows that only the phase-shifted and swapped map matches all rows.
- **Angle rows.** 82 `=L= 0.26` plus 82 `=G= -0.26` rows in 0030p (4 × 41 branches), 92 + 92 in 0039p (4 × 46), none in 0039r or 0030r. The report says the same.
- **Mittelmann's benchmark** (plato.asu.edu, 26 Feb 2026) contains only waterno2_02/03 and powerflow0014r/0057r from these families.
- **QPLIB.** `qplib.solu` has no value near 576.89 or 41869.05. This closes the report's open QPLIB caveat as far as objective values can show.

### 3.2 KAN

- **Zenodo supplement.** An own xlsx reader (`zenodo_read_r2.py`; logs `zenodo_r3.log`, `zenodo_r5.log`) confirms all numbers in Sections 4.2–4.7, for example:
  - Default R3_H1_N4: PB = DB = 1.08116412047821e-3 at 3459 s;
  - R3_H1_N5: −1.30809958982354e-2 at 5038 s;
  - the other configurations: 7.98e-4, 9.10e-4, 1.006e-3, 1.049e-3 and 1.064e-3 (n4); −1.3104e-2, −1.3334e-2, −1.2561e-2 and −1.3476e-2, with Redundant at the time limit (PB −1.2882e-2, DB −2.6465e-2) (n5);
  - best duals −11.376, −1587.43, 0.18669 and −122.67; ConvexHull r5_n5 PB 0.272518774.
- **Objective scale.** The objective-defining row has A = 970.2191877107767 (r3) and 1439.6298856740555 (r5).
- **Other formulations.** MINLPLib holds no other formulation of the six networks; the other KAN instances are kan_r3_h1_n3 and kan_peaks_*.
- **arXiv versions.** arXiv 2503.02807 still has only v1.

### 3.3 Water networks

- **Huang 2019, Table 5.2.** Re-read: the values match the report's table. The gap columns are (primal − dual)/dual, e.g. (404.81 − 343.41)/343.41 = 0.1788. The no-cut gaps are 1.79, 3.67, 4.64, 10.72 and 17.43.
- **Other parts of the dissertation.** Table 4.3 concerns n25p22a18, not waterno2. The conclusion (p. 129) confirms "very early computational results for instance n9p3a11".
- **Geißler et al.** Appendix B Table 2 gives 442.50, 1422.16, 3119.55, 7359.11 and 9711.81.
- **D'Ambrosio et al.** The quotes are present.

### 3.4 MINLPLib pages and our claims

- **Pages.** An own parser over the 17 pages the author saved, and over 8 pages re-fetched today, confirms every listed primal and dual bound in the report and the dates added (18 Aug 2014, 07 May 2025, 12 Aug 2014, 29 Nov 2021).
- **Our values** match `open-instances-summary.md` and the wave-3 report:
  - 576.8934122988, 41869.05148485 and 41869.05148327;
  - the KAN bounds of R;
  - the waterno2 duals and primals;
  - −3386.5403 for cumene;
  - 576.8934126255 for 0030r.

### 3.5 Sources

- **Manifest.** All 93 `MANIFEST.md` entries match their sha256, and no file is unlisted (own script).
- **Key facts at the stated locations.** Hijazi 2014 pp. 16–18; Karia et al. Tables 2, 5 and 9; Schweidtmann arXiv v2 Table 4, p. 21; Izquierdo González pp. 1796–1797; Huang 2019 pp. v, 122–126. All confirmed by grep/sed.

## 4. Searches (both r2 agents)

**Web searches:**

- KAN global optimization: journal version, AIChE 2025, KAN MILP/MINLP formulations, 2025–2026 work. Results: only arXiv 2503.02807 v1 and the ESCAPE paper; unrelated KAN papers 2602.06737, 2501.17411 and 2512.12448.
- `"waterno2" MINLP benchmark dual bound`: led to arXiv 1903.05521, 2603.16505 and 2409.19794 (the last has no instance names).
- n9p3a11 and Huang water-network papers.
- `powerflow0039r OR powerflow0039p OR powerflow0030p`.
- QPLIB powerflow.
- Octeract claims about MINLPLib.
- Rigorous or verified ACOPF lower bounds: led to Oustry et al. 2022.
- Cumene ANN, MAiNGO, follow-ups: led to the RWTH record 820314.
- MINLPLib open instances with rigorous certificates: nothing beyond MINLPLib pages and a TRR154 optimality-certificate preprint not specific to these instances.

**Full-text checks of related papers:**

- Grep of other tracks' PDFs for our instance names: SCIP 8 JOGO paper, SCIP Optimization Suite 8.0, Göß–Burlacu–Martín (JOGO 2026), Mattick 2023 (gaps only, unrelated), Neumaier 2005, and Gabrys–Sremac 2025.
- Tasseff et al., arXiv 2208.03551: no waterno2 or MINLPLib mention.

**Archives:**

- Internet Archive availability/CDX checks for RWTH 820314 (found), the AIChE abstract (none) and the Springer JOTA page (preview only).

An unsuccessful search does not prove that nothing exists.

## 5. Items in the generic checklist that do not apply

This literature track ran no solver campaign, clean reproduction or background job, so there was nothing of that kind to check. Neither r2 agent started a long job; no stray processes remain (`ps` check).

## 6. Commands run

| who | command | outcome |
|---|---|---|
| r2 agent 1 | curl of minlplib.org GAMS files powerflow0030p/0030r/0039p/0039r and of MATPOWER case30.m/case39.m (GitHub master) | saved in `lit-network-r2/` |
| r2 agent 1 | `python3 pf_twin_check.py` → `pf_twin_check.log` | only the swapped/phase-shifted map matches |
| r2 agent 1, rerun by me | `python3 pf_twin_exact_r2.py` → `pf_twin_exact_r2.log` | objective equal; 214 exact + 60 via V² + reference row; 116 rows within 1.03e-13 |
| r2 agent 1, rerun by me | `python3 pf_loads_shunts_r2.py` → `pf_loads_shunts_r2.log` | loads match; no shunt terms |
| r2 agent 1, rerun by me | `python3 pf_taps_r2.py powerflow0039r.gms powerflow0039p.gms` → `pf_taps_r2.log` | 11 tapped branches untapped only, in both files |
| r2 agent 1, rerun by me | `python3 cumene_twin_r2.py` → `cumene_twin_r2.log` | 250 shifted rows, 540 identical, 0 bad |
| r2 agent 1 | `python3 zenodo_read_r2.py <xlsx> R3_…/R5_…` → `zenodo_r3.log`, `zenodo_r5.log` | values as in the report |
| r2 agent 1 | curl of 8 MINLPLib pages (1 s spacing) → `pages_20261002/summary.txt` | unchanged |
| r2 agent 1 | Crossref API for 15 DOIs; doi.org for 2 → `doi_check_r2.log` | as in minor issue 6 |
| r2 agent 1 | curl of Mittelmann minlp.html, nontrivial.txt, compare.txt; QPLIB instances.html and qplib.solu | Section 3.1 |
| r2 agent 1 | reran the author's `checks/*.py` with outputs to /tmp, then diff | identical apart from timing lines |
| r2 agent 1 | WebSearch (about 15 queries); WebFetch/curl of the AIChE abstract (403/Cloudflare) and the RWTH record (bot check); OpenAlex; arXiv abs page | Section 4 |
| me | python extraction of the predecessor transcript | context recovered |
| me | python parse of the 17 saved MINLPLib pages; grep of claim values in `open-instances-summary.md` and the wave-3 report | Section 3.4 |
| me | grep -o counts of the Example 5.41 coefficients in 9 waterno2 OSIL files | 2 × T |
| me | sed of Huang Table 5.2, Table 4.3 and the conclusion | Section 3.3; minor issue 5 |
| me | python: exact b of branch 27–29 versus the stored coefficients | minor issue 4 |
| me | python: KAN objective rows; grep of Zenodo log parameters | Section 3.2; minor issue 7 |
| me | python: sha256 of all `MANIFEST.md` rows | 93/93 match |
| me | WebSearch × 7; curl of arXiv PDFs 2603.16505, 1903.05521, 2409.19794, 2512.12448 and 2208.03551, with pdftotext and grep | minor issue 2 |
| me | pdftotext and grep on `literature/control/sources` PDFs (SCIP 8 papers, Göß JOGO, Mattick, Gabrys, Neumaier) | minor issue 2 |
| me | curl of the Oustry et al. PDF (lix.polytechnique.fr) and the GitHub results table | minor issue 3 |
| me | curl of the Wayback availability/CDX API and of the RWTH 820314 PDF (id_ URL); pdfinfo; pdftotext | minor issue 1 |
| me | curl of the Springer JOTA page (direct, and Wayback 2024-07-07, gunzip) | preview only |
| me | curl of doi.org/10.69997/sct.139045; Crossref query for Müller et al.; export.arxiv.org abs pages | minor issues 2 and 6 |
| me | `ps` check | no stray processes |

## 7. Sources saved by this round (`lit-network-r2/sources_r2/`, fetched 2026-10-02, sha256)

- `arxiv2603.16505.pdf` (Göß 2026) `c98b3f7a1f740d6bb6d21a109425770c952bf4bc31c491d27d7970132bd07c3b`
- `arxiv1903.05521.pdf` (Müller–Serrano–Gleixner) `3ce4981232e943ae6805f97e1e2528df45fd68daa1cbd8a0386545ecbfff5362`
- `oustry2022_pscc22.pdf` (HAL preprint) `75412dc265bad0f67db8359378b97c1e8cad83eb40095765f0e972d5f2e80d7e`
- `oustry_table_of_results.txt` (GitHub) `0fdca4d54703af8fa6beb80df44e63641da3fc38e4951afd644717c2e689fd8b`
- `rwth820314_wayback20260128.pdf` (Schweidtmann dissertation) `0ce49fca3cbf474ef42456d4ee5448a719dd96de3202b9aef283c8bc4b7bf44c`
- `arxiv2208.03551.pdf` `336f37404bcae8e455226bc24d1ed3b493d4d49aa32488da76df89b80e32f5fe`
- `arxiv2409.19794.pdf` `7f59f53f59fd72e345c3cd3ad2452622f295276f7cddb74daea492fbb2445ed5`
- `arxiv2512.12448.pdf` `8c217616705eddfea4e8473d7e0db52fb6c875bdb3bbec67ee882e0b8ae12041`
- `jota_springer_wayback20240707.html` (preview only) `4adceb07015ca353ad46277a576e5e1e6666ffe7f69a175be21970e5838f5105`
- `*.txt` files: pdftotext -layout output of these PDFs.

The SCIP Optimization Suite 8.0 report is already in `literature/control/sources/scip80_suite_arXiv2112.08872v1.pdf`.

## 8. What kind of evidence each result is

- **Exact rational comparisons:** the cumene twin identity, the loads and shunts, the tap coefficients, the coefficient rounding of 0030p/0030r and the 2 × T counts.
- **Agreement at random rational points:** the 0030p/0030r row matching. This is strong evidence, not a symbolic proof.
- **Read from the sources:** all literature values.
- **Floating-point claims of their authors:** all solver results quoted from the literature and from MINLPLib.
