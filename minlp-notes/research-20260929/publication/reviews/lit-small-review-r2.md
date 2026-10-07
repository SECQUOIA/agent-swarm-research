<!-- Written to disk by the root from the structured return value of verifier round 2 of track lit-small in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review of track lit-small (round 2)

- **Reviewer:** independent verifier, review round 2. No earlier round-2 attempt had left files.
- **Date:** 2026-10-02.
- **Text reviewed:** the revised report given in the task text, "revised 2026-10-02 after review round 1". `literature/small/report.md` on disk is still the round-1 version (13:43); the root will overwrite it.
- **My files:** `research-20260929/publication/reviews/lit-small-r2/`. This folder holds my check code (`manifest_check.py`, `hvycrash_check.py`, `eg_int_s_oldpoint.py`, `eg_mod_check.py`), the logs in `logs/`, the new sources with a sha256 manifest in `sources/`, and `PROGRESS.json`.

## Verdict

**Issues: one major, four minor.**

The round-1 fixes are correct and well checked:
- M1 (HVYCRASH) is fully resolved. My own code confirms it and also closes one of the author's open points: the SIF rows now agree numerically with the OSIL rows, not only by inspection.
- All eleven round-1 minor items are handled. I confirmed each one at its stated location.

The new major issue concerns CAMINO. The report concludes "primal values only". In fact, CAMINO's own definitions and public data show Gurobi 13.0.0 claiming optimality at wrong values on eg_disc2_s, eg_disc_s and eg_int_s. No consequence label changes. The paper needs this fact, and the report's description of the source is wrong on exactly the point the track is about: claimed global optima.

## Status of the round-1 items

| item | status | my check |
|---|---|---|
| M1 HVYCRASH SIF bounds | **fixed** | Own bound decoder (`hvycrash_check.py`, applies the cards in file order): both SIF versions, N = 50 and 1000, fix only X(1,0) = 0 and X(2,0) = 2.19905, and all θ_T ∈ [0, 6.2831854]. SIF and AMPL bounds are identical for all 204 variables. New: the SIF rows C(1,T), C(2,T), C(3,T) at N = 50 (my hand transcription of GROUPS, ELEMENT USES and ELEMENTS) equal the rows of the cached OSIL. Max difference 2.1e-48 over 20 random points × 150 rows (mpmath, 50 digits), all with the same sign. The objective is X(1,50). Map: θ_T = x_T, θ_0 = x101, U(T) = x_{50+T}, r_T = x_{101+T}, X(1,T) = x_{202−T}. `diff` of the 2013 and 2026 files: only the "Updated … May 2026" line and the SOLTN spacing differ, as the report says. The identity algebra (C(2,T) ⇒ cos θ/(A·C·r²) = −1; C(1,T) ⇒ X(1,T) = X(1,T−1) − H) is correct. No infeasibility statement remains. |
| 1 PrincetonLib variant | fixed | Lines 714–822: `epsi = +0.005` (redefined; line 53 has epsi = 0.1, but the rows use a literal 0.1). x1_0 is fixed at 0.005, x2_0 at 2.20405, and all θ ∈ [0.005, 2π + 0.005]. The rows use 0.00437 and 1.62079 as in the SIF, and `Def_obj.. obj =e= x1_50`. So "−0.2135 at any feasible point" is right. |
| 2 Bertsimas & Margaritis | fixed | Confirmed: PDF p. 24 (1500 s limit, "GOpt" when the gap is below 0.1%, BARON 2021.01.13); p. 27 (ex6 2 5 and ex6 2 7, 9 variables, BARON GOpt at 1502.2 s); p. 25 ("BARON is able to solve 73 out of the 77"). arXiv has only v1. |
| 3 Göß correction | handled (unread) | Crossref: 95(4) 1095–1141, `update-to` 10.1007/s10898-026-01591-z. My own attempt: Springer still serves a 3 KB HTML bot page; Wayback has no snapshot; OpenAlex lists only the Springer URL. |
| 4 gap tolerance | fixed | arXiv v2, lines 817–821 ("If not stated otherwise, default settings are used") and 1078–1079 (60 GB memory, 4 h, eight threads). My own download of the paraboloids zip has the same sha256, 71ee269a…. No optcr anywhere. See minor 4(d) for two details. |
| 5 rounding | fixed | −70.75207783344770759 and −15.294675643368093 match `closing-confirm-r2.md`/`-r3.md` and the summary. Both are below the proved values. |
| 6 Omheni, Prudente | fixed | PDF p. 120 (n = 4002, m = 3000); p. 134 SPDOPT 1.1e−19; p. 146 IPOPT −1.8e−01; p. 158 ALGENCAN 9.3e−16; p. 170 LANCELOT −6.9e−02 with code 1 ("Nombre maximum d'itérations atteint"). |
| 7 unread primary sources | fixed | — |
| 8 pricing050 caveats | fixed | Formula (9) is on ORL preprint p. 15 without the 1/10 scaling; the bounds [0, 10] are on p. 16 (minor 4(c)). Table 1 (p. 18): n = 50, #2: 1813.3 / 1663.7 / 1037.4 / 1354.2 / 1437.6 / 1368.3. |
| 9 `minlplib.solu` | fixed | All nine `=bestdual=` values in the new table match `minlplib.solu`. All are weaker than the page values, and hvycrash has none. |
| 10 Trombettoni | fixed | Table 2 and 3 headers: Baron, GlobSol, IBBA+ at 1e-8; Icos at 1e-3; IbexOpt at 1e-3 and 1e-8. Limits: 1 h (IBBA+, GlobSol, IbexOpt), 10 min (Icos), 1000 s (Baron on NEOS). |
| 11 COCONUT, CAMINO | partly right | COCONUT `modelstatus = 2.00` is confirmed for ex6_2_7, ex6_2_5 and etamac. The author is right that CAMINO arXiv v2 (26 Mar 2026) has eg_* rows (Table 8, p. 51); the round-1 statement was wrong. The values quoted for all three instances are correct. But "primal only" is not right for Gurobi: see the major issue. |

## Major issue

### R2-M1. CAMINO: Gurobi 13.0.0 claimed optimality at wrong values on eg_disc2_s, eg_disc_s and eg_int_s, but the report says "primal values only"

**What the report says.**
- Section 9.2: Table 8 "lists only the objective values of returned solutions and wall times (300 s limit)".
- Sections 10.1 and 11.1: "primal values only, 300 s".
- Summary table: "CAMINO paper (2026): primal values only".
- Section 16, item 11: "the review's conclusion 'primal only' holds and is now confirmed from the text".

**What the source says.** CAMINO arXiv v2:
- Section 4.1 (p. 26): SCIP v9.2.2 and Gurobi v13.0.0 are "called using the AMPL Python interface which loads the MINLPLib as .mod file". The "MINLP gap for termination is set to 10−2".
- p. 28–29: "all algorithms except SCIP and Gurobi are only heuristics for nonconvex MINLPs". "On each instance we limit the available time of SCIP and Gurobi to the computation time achieved by S-B-MIQP".
- Table 3 caption: "For SCIP and Gurobi 'success' correspond to a global optimal solution".

**What the public data show.** The CAMINO-benchmark repository is cited in the paper as the reproducibility source (github.com/minlp-toolbox/CAMINO-benchmark; results last changed in commit 66a134daf8, 19 Mar 2026). Copies are in `sources/camino_benchmark/`.
- The driver `benchmark/using_amplpy.py` runs Gurobi with `bestbound=1 feastol=1e-8 mipgap=1e-2 threads=1 timelimit=<S-B-MIQP time>`. It records `obj` and `obj.bestbound` only when `solve_result` is "solved" or "limit".
- The per-instance limits are in `wall_time_noncvx_sbmiqp.json`.
- `results/26_03_10_results/noncvx_gurobi.csv` matches Table 8:

| instance | Gurobi objective | Gurobi best bound | time (s) | limit (s) | value of a known exactly feasible point |
|---|---|---|---|---|---|
| eg_disc2_s | 5.88669499573929 | 5.88669499573929 | 2.15 | 32.63 | 5.6421005799711068 |
| eg_disc_s | 6.191829847658548 | 6.191829847658548 | 0.99 | 19.24 | 5.7605396164535106 |
| eg_int_s | 11.65415903480683 | 11.65415903480683 | 70.80 | 212.66 | 6.4531031593842274 |

Gurobi stopped long before its limit, with the bound equal to the objective. By CAMINO's own definition, that is a claimed global optimum.

**Why the claims are wrong.**
- I fetched the three MINLPLib `.mod` files that CAMINO used. My `eg_mod_check.py` evaluated their rows and the cached OSIL rows at random points (mpmath, 40 digits): they are identical.
- On the `.mod` rows, the project's recorded exactly feasible points (`open-instances-wave3/eg/retry/sol/*.sol`, within the `.mod` bounds) need objective values of only 5.64210057997110676, 5.76053961645351061 and 6.45310315938422741.
- So Gurobi's bounds exceed the optimum by 0.2446, 0.4313 and 5.2011, which is 4%, 7% and 81%. This evaluation is numerical evidence; the exact feasibility of these points was proved and verified elsewhere in the project.
- By contrast, the SCIP 9.2.2 runs in the same data hit their limits with valid bounds −5.83, −6.74 and −4.26.

**Consequence.** The consequence labels stay the same, because a wrong optimality claim closes nothing:
- eg_disc_s and eg_disc2_s: "new as far as found";
- eg_int_s: "already solved in floating point" (Göß et al.).

But the report must stop calling CAMINO primal-only. It should say:
- for Gurobi, the paper's Table 3 semantics and its public data amount to claimed global optima at these wrong values;
- for SCIP, and for Gurobi elsewhere, the results are primal values at the S-B-MIQP time.

This belongs in Section 12 next to the COCONUT pindyck and Davarnia pricing050 items. For a paper about rigorous certificates, it is a strong motivating example: a 2026 commercial global solver reported wrong optimal values on three of these instances. The cause is not known; one possibility is how the AMPL driver passes `exp` terms to Gurobi. The report should say the cause is unknown, not guess.

## Minor issues

1. **CAMINO time limits.** The report gives "300 s limit" for all of Table 8. That limit applies to Bonmin, SHOT and S-B-MIQP. SCIP and Gurobi had the S-B-MIQP time of each instance: 32.6 s, 19.2 s and 212.7 s for eg_disc2_s, eg_disc_s and eg_int_s. State the versions (SCIP 9.2.2, Gurobi 13.0.0, through the AMPL Python interface).

2. **Missed source: Kosolap (2019).** A. Kosolap, "Finding the Global Minimum of the General Quadratic Problems During Deterministic Global Optimization in Cyber-Physical Systems", *Advances in Cyber-Physical Systems* 4(1) (2019) 32–36, doi:10.23939/acps2019.01.032. Saved as `sources/kosolap2019_acps_4-1_32.pdf`.
   - Table 1 (p. 34) lists **Ex6_2_5** (n = 10, m = 3) with "Method EQR −70.9586" against "best known glob. min. −70.75 (GL)".
   - The method ("exact quadratic regularization") uses local interior-point search.
   - −70.9586 lies 0.207 below the certified lower bound −70.75207783344770759, so no feasible point of the MINLPLib (= GLOBALLib) model has that value.
   - The paper should cite it among the published values that cannot be attained.
   - The same author's other open papers that I read (2013, 2014, 2018 ×2, 2020 (OCR), 2021 ×2, 2023) do not mention the nine instances; the 2021 ESAIM Proc. paper returned 403 and was not read.

3. **eg_int_s point and model history (Section 9.1).**
   - The GAMS World point `objvar.L = 6.4531031527` lies 2.3e-10 *below* the certified lower bound 6.4531031529331155. The report quotes it without comment.
   - My evaluation on the cached OSIL (`eg_int_s_oldpoint.py`) shows that the point violates row e12 by 6.4e-9, so the value is a tolerance artifact. Say so, or do not quote it as a solution value.
   - The COIN-OR 2008 BONMIN logs (2 Sep 2008) show all three eg_* models with "28 rows 8 columns 220 non-zeroes" and 196 NL nonzeros, the current size. So the two extra rows were added between Aug 2001 and Sep 2008, and the 2008 BARON and LindoGlobal values refer to the current model.

4. **Small inaccuracies.**
   - (a) The hvycrash summary cell says "near-zero local-solver values at N = 1000". Omheni's IPOPT gives −0.18 and LANCELOT −0.069, and the SIF SOLTN values are for N = 100, 500 and 1000. Use the wording of Section 12, item 4.
   - (b) Section 3.1 writes "c_k ∈ [0.08, 0.417]". The MINLPLib controls are x51..x100 (U(T)).
   - (c) Section 7.1 gives formula (9) "with x ∈ [0, 10] (preprint p. 15)". The formula is on p. 15, but [l, u] = [0, 10] is stated on p. 16 (line 314).
   - (d) Section 9.2. The repository README says the written GAMS files exclude "the `eg_...` ones due to their size", so the no-optCR finding is inferred from the other instances. Also, `para_relaxation/instances/scip.opt` (`limits/memory=61440`, matching the 60 GB limit) and `gurobi.opt` (`nonconvex=2`, `memlimit=60`) set no gap. Both points support the 1e-4 reading and are worth one sentence.

## Cross-track notes (not issues for this track)

- **chain50** (literature track for chain*): Kosolap, *J. Numer. Appl. Math.* 2(136) (2021) 53–63, doi:10.17721/2706-9699.2021.2.05, Table 1, claims chain50 = 0.09259 against the best known value 5.07226. That is far below the known optimum, so it cannot be the value of a feasible point. Saved in `sources/kosolap2021_jnam_136.pdf`.
- **KAN instances** (literature track for KAN): CAMINO's data report objective values for kan_r3_h1_n4/n5/n9 and kan_r5_h1_n3/n5/n8 from SCIP and Gurobi at feastol 1e-8. For example, Gurobi gives 0.0766 on kan_r3_h1_n4 and SCIP gives 89.17. Our work found these OSIL models exactly infeasible, so these points can satisfy the constraints only within the solvers' tolerances.
- **waterno2** (water track): the CAMINO Gurobi and SCIP primal values for waterno2_06–24 are all above our certified bounds, so there is no conflict.
- **Solver campaign / SCIP wrong-value track:** Gurobi 13.0.0 through AMPL claimed wrong optima on eg_* (R2-M1). The campaign runs Gurobi 13.0.2 through GAMS; its eg_* results deserve a careful validity check.

## Claims I confirmed (beyond the round-1 list)

- **Manifest** (`manifest_check.py`): 112 rows, 112 distinct paths, 0 bad hashes, 0 missing, 0 unlisted files.
- **hvycrash:**
  - The OSIL has 201 variables and 150 rows, with the objective on x152 = X(1,50). The gms has 201 variables plus objvar (row e151), so "201 variables plus objvar" is right for the gms.
  - The COCONUT Library 2 model is Vanderbei's `hvycrash.mod`, so the identity applies to the COCONUT and Smith values.
  - The SIF has an empty `SOLTN(3000)` line.
- **CAMINO v2:**
  - Table 8 (caption on p. 49, eg rows on p. 51): all quoted values are correct.
  - The abstract quote is verbatim.
  - arXiv history: v1 17 Apr 2024, v2 26 Mar 2026. Crossref: MPC article 10.1007/s12532-026-00331-4; correction 10.1007/s12532-026-00337-y (update-to the article).
- **Göß et al.:**
  - arXiv v1 8 Jul 2024, v2 21 Mar 2025.
  - JOGO PDF p. 38 (= p. 988), Table 17. eg_int_s: SCIP orig 9085.1 s, 6.5 | 6.5. eg_disc_s: SCIP\* orig 3.6 | 5.8; Gurobi 2.0 | 7.5. eg_disc2_s: SCIP −1.1 | 6.3; Gurobi −5.2 | 7.0. eg_int_s Gurobi orig: −1.9 | inf.
- **MINLPLib 2018 snapshots:** eg_int_s LINDO −1.20527282 (report: −1.21, correctly rounded); eg_disc_s −4.02463010; eg_disc2_s −7.56589692.
- **Najman et al. (2021), Table 7:** ex6_2_7 at 28 800 s with 14.77%–17.83%. ex6_2_5 is absent.
- **Published values compared with the certified bounds.** Every other published primal value in the report sits at or above our certified bounds once printing round-off is allowed for:
  - COCONUT BARON −0.1608476155 and MINOS −15.2946756434 (10-digit rounding);
  - MINLPLib CONOPT points;
  - BARON and LindoGlobal 2008 values;
  - Cristofari et al.
  
  The only exceptions are those the report already flags (pricing050 1813.3, COCONUT pindyck, the hvycrash values) and the new ones above (Kosolap, the GAMS World eg_int_s point).

## My own searches for missed prior results

- **WebSearch (6 queries):**
  - "ethylene glycol" "lauryl alcohol" "nitromethane" Gibbs global minimum stochastic;
  - ANTIGONE Misener–Floudas per-instance results for ex6_2_7;
  - Kiaghadi dissertation and decision diagrams for pricing;
  - "eg_disc2_s" OR "eg_int_s" OR "eg_disc_s";
  - "hvycrash" "−0.2185";
  - "ex6_2_7" OR "ex6_2_5" with EAGO, Octeract, Gurobi or SCIP.
- **OpenAlex:**
  - full-text queries for all nine names (hvycrash 8 hits, all in the report; ex6_2_7 4; ex6_2_5 4, which led to **Kosolap 2019**; etamac and pindyck only off-topic hits);
  - 2 title/abstract searches for the Gibbs systems, which found Stateva et al. 2000, Reddy & Rani 2012 and Sun & Seider 1995 (local or homotopy phase-equilibrium methods; not read; they would not change any label);
  - Kosolap's 26 works (all open ones read or OCRed);
  - the ANTIGONE paper (closed; per-instance data not public).
- **Other:**
  - GlobalDD arXiv v2 (4 Apr 2026): none of the nine instances.
  - arXiv 2607.02697 and 2407.07812 (S2MPJ): no HVYCRASH.
  - CAMINO-benchmark repository (R2-M1).
- **Not readable:** the Göß correction (bot page) and Kosolap's 2021 ESAIM Proc. paper (403).

No source changes a consequence label.

## Does the report say plainly what is proved, numerical or unread?

Yes, with one exception: the CAMINO characterization (R2-M1). The hvycrash bound decoding is correctly described as pure card bookkeeping. The model identity and the pricing050 instance identity are labelled numerical. Unread sources are listed with reasons, and the commands-run section is complete and specific. The open point "hvycrash rows compared by inspection, not numerically" can now cite my numerical row check (`logs/hvycrash_check.log`).

## Commands I ran

All runs were single-process (at most one core), with no background jobs; none of my processes remain. No project-wide checks were run, CI was not inspected, nothing was committed, and nothing was posted or sent.

- **Manifest:** `python3 manifest_check.py ../../literature/small/sources` → 112 rows, 0 bad, 0 missing, 0 unlisted (`logs/manifest_check.log`).
- **HVYCRASH:**
  - `diff` of `HVYCRASH.SIF` and `HVYCRASH_2013_a4c9117d7d.SIF`; `sed` of the BOUNDS, GROUPS, ELEMENT USES, GROUP USES and ELEMENTS sections.
  - `python3 hvycrash_check.py`: bounds for both versions at N = 50 and 1000; SIF vs AMPL bounds (0 differences); SIF vs OSIL rows (max difference 2.05e-48) (`logs/hvycrash_check.log`).
  - Python summary of the OSIL variable bounds; `sed`/`grep` of `hvycrash.gms`, the PrincetonLib indexed file (lines 1–160 and 700–1001), `hvycrash.mod`, and the COCONUT `lib2_hvycrash.htm`/`.res`.
- **PDF checks:** `pdftotext` with Python or `grep` for:
  - Bertsimas & Margaritis (pp. 24, 25, 27);
  - Omheni (pp. 120, 134, 146, 158, 170; code legend);
  - Trombettoni (Table 2/3 headers);
  - ORL preprint 7681 (pp. 2, 15, 16, 18);
  - CAMINO v2 (pp. 1, 26–29, 47–51; setup lines 1418–1445);
  - Göß arXiv v2 (lines 812–824, 1078–1079; table numbering) and JOGO p. 38;
  - Najman (Table 7).
- **Text files:**
  - `grep` of `minlplib.solu` for the nine instances; `grep` of `closing-confirm-r2.md`/`-r3.md` and of the summary;
  - text extraction of the 2018 snapshots for eg_*;
  - `grep` of the COCONUT `.res` model status;
  - `grep` of the GAMS World point files.
- **Web fetches** (curl, sequential, about 1 s apart):
  - arXiv abstract pages for 2404.11786, 2407.06143, 2311.01742 and 2409.19794;
  - Crossref for 10.1007/s12532-026-00331-4, 10.1007/s12532-026-00337-y, 10.1007/s10898-026-01614-9, 10.23939/acps2019.01.032 and 10.17721/2706-9699.2021.2.05;
  - Springer correction PDF (bot page), Wayback availability API, OpenAlex record;
  - GitHub paraboloids `main.zip` (sha256 71ee269a…), unzipped and `grep`ped for optcr, reslim, threads, gap and option files;
  - COIN-OR 2008 BONMIN logs for the three eg_* instances;
  - CAMINO-benchmark: GitHub API tree, the commit list for `noncvx_gurobi.csv`, raw `noncvx_gurobi.csv`, `noncvx_scip.csv`, the two `overview.json` files, `using_amplpy.py` and `wall_time_noncvx_sbmiqp.json`;
  - MINLPLib `.mod` files for eg_disc2_s, eg_disc_s and eg_int_s;
  - arXiv PDFs 2409.19794 (v2), 2607.02697 and 2407.07812;
  - Kosolap papers (9 URLs; one returned 403; one needed a second URL); `pdftoppm` with `tesseract` (eng, one thread) OCR of the scanned 2020 paper.
- **OpenAlex API:** 9 full-text queries, 2 search queries, 5 DOI lookups and 1 author works list.
- **WebSearch:** the 6 queries listed above.
- **eg_* numerical checks:**
  - `python3 eg_int_s_oldpoint.py` → objective 6.4531031527; max violation 6.37e-9 at row e12 (`logs/eg_int_s_oldpoint.log`).
  - `python3 eg_mod_check.py`, run twice after fixing a parsing bug in my row-sense regex. Result: `.mod` vs OSIL relative difference 0.0 for all three instances; feasible x8 = 5.64210057997…, 5.76053961645…, 6.45310315938…; Gurobi bounds exceed these by 0.2446, 0.4313 and 5.2011 (`logs/eg_mod_check.log`).
