<!-- Written to disk by the root from the structured return value of verifier round 1 of track lit-small in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review of track lit-small (round 1)

Reviewer: independent verifier, third attempt in this role. The first two attempts were cut off by usage limits; I read their transcripts and reused or reran their reviewer-side checks where noted. Date: 2026-10-02.
Report reviewed: `research-20260929/publication/literature/small/report.md` (48 443 bytes, written 2026-10-02 13:43).
My files: `research-20260929/publication/reviews/lit-small-r1/` (code, logs, `sif/`, `sources/` with `manifest.tsv`, `crossref/`, `PROGRESS.json`).

## Verdict

**Issues: one major, eleven minor.** The literature work is careful and mostly correct. The searches are broad, the sources are saved with hashes, and the labels (rigorous, floating-point global, local, listing) are used consistently. I confirmed almost every quoted number at its stated location. The exception is the claim that the CUTE SIF version of HVYCRASH is infeasible and that MINLPLib's hvycrash is a modified version of it. That claim is wrong, and the report repeats it in five places, including a "side finding for the paper". It must be corrected before the paper uses it.

## Major issue

### M1. HVYCRASH: the SIF problem is not infeasible, and MINLPLib's hvycrash is not a modification of it

**What the report says.** Summary table: "Modified: … The SIF fixes both [θ_0 and θ_50] at 0, which makes the SIF version infeasible." Section 3.1: "The SIF version is infeasible. This is our own observation, exact and checked by hand." Section 3.2: "The SIF version has no feasible points." Also: "Our infeasibility observation explains these failures." Side finding 3: "The CUTE SIF version of HVYCRASH is infeasible for every N." Section 3.3: "note that the MINLPLib version differs from the infeasible SIF version."

**What the SIF file does.** The BOUNDS section of `sources/hvycrash/HVYCRASH.SIF` reads:

```
 XX HVYCRASH  X(1,0)    0.0
 XX HVYCRASH  X(2,0)    2.19905
 XX HVYCRASH  X(3,0)    0.0

 XX HVYCRASH  X(3,N)    0.0

 DO T         0                        N
 XL HVYCRASH  U(T)      0.08
 XU HVYCRASH  U(T)      0.417
 XL HVYCRASH  X(3,T)    0.0
 XU HVYCRASH  X(3,T)    6.2831854
 OD T
```

The loop runs over T = 0..N and comes after the XX cards. It therefore sets X(3,0) and X(3,N) to [0, 6.2831854] again.

- **SIFDecode applies individual bound cards in order, and the last card wins.** In the reference decoder (`sif/sifdecode.f90`, subroutine SBOUND, from ralna/SIFDecode master, sha256 06cfe6d7…), an individual card assigns `B_l( ncol, nbnd ) = value4` (line 5060) and `B_u( ncol, nbnd ) = value4` (line 5090) unconditionally. A later XL/XU card overwrites an earlier XX card.
- **The decoded problem.** X(1,0) = 0 and X(2,0) = 2.19905 are fixed; θ_T = X(3,T) ∈ [0, 2π] for all T = 0..N, including θ_0 and θ_N; U(T) ∈ [0.08, 0.417]; all other variables are free. This is exactly Yurttan's AMPL file `hvycrash.mod`, which has 51 variables `x3_k >= 0, <= 6.2831854`, only `x1_0` and `x2_0` fixed, and all `u_k` in [0.08, 0.417]. It is also MINLPLib's model. The AMPL translation is faithful, not modified.
- **The 2013 version is the same.** The first ralna/SIF commit of the file (a4c9117d7d, 2013, saved as `sif/HVYCRASH_2013_a4c9117d7d.SIF`) has the same BOUNDS order. So the May 2026 update did not change this.
- **Independent counts agree.** COCONUT Library 2 lists hvycrash with 202 variables (204 − 2 fixed). Omheni (2014, PDF p. 120) lists HVYCRASH at N = 1000 with n = 4002 (4004 − 2). Both fit two fixed variables, not four.

**Consequences.**
- MINLPLib hvycrash is the CUTE HVYCRASH problem at N = 50 ("original value"). The only difference is that the fixed X(1,0), X(2,0) and the unused U(0) are removed.
- The SIF value `*LO SOLTN -0.21850` (Toint, 1994) is therefore a value recorded for the same problem. This strengthens "partly known": the optimal value was on record, without proof, for the identical problem.
- The report's argument that SOLTN(100), SOLTN(500) and SOLTN(1000) cannot come from feasible points still holds, but only through the identity. The C2 element is cos θ/(A·C·r²), C(2,T) gives cos θ/(A·C·r²) = −1, so X(1,N) = X(1,0) − N·H = −TT at every feasible point for any N. The reason "the SIF version has no feasible points" must be deleted.
- The local-solver failures (Buchanan's "Feasible point is never found", Algencan's time and iteration limits, Gomes) are not explained by infeasibility. They concern a feasible, badly scaled problem. Delete "Our infeasibility observation explains these failures".
- Side finding 3 must go. It could be replaced by a neutral remark: the XX cards for X(3,0) and X(3,N) are dead code because the later loop overrides them. Whether the SIF author meant to fix them is unknown.

The algebra itself is correct: with θ_N = 0, row C(2,N) has no real solution. The error is only in reading which bounds the SIF file actually imposes.

## Minor issues

1. **PrincetonLib variant described inaccurately (Section 3.1).** The GAMS World file fixes x1_0 at 0.005 and x2_0 at 2.20405 (lines 716–717 and 770–771), and gives all 51 θ_k the bounds [0.005, 2π + 0.005], not only θ_0 and θ_50. The report says it "fixes x1_0 at epsi = 0.005 and bounds θ_0 and θ_50 below by 0.005".

2. **Missed source on ex6_2_5 and ex6_2_7.** Bertsimas & Margaritis, "Global optimization: a machine learning approach", J. Glob. Optim. 91 (2025) 1–37, doi:10.1007/s10898-024-01434-9 (arXiv:2311.01742v1, Table 1, PDF p. 27). BARON 2021.01.13 with a 1500 s limit is reported as "GOpt" for ex6_2_5 and ex6_2_7, both with time 1502.2 s. "GOpt" means "optimality gap below 0.1%". The paper does not say whether that gap is BARON's dual gap or the distance to the best known value, and BARON stopped at the time limit. This is not a certificate. The paper should cite it and explain it, because a reader could take it as "BARON solved ex6_2_5 and ex6_2_7". Saved as `sources/bertsimas_margaritis_arxiv2311.01742v1.pdf`.

3. **Publisher correction to Göß et al. not mentioned.** Crossref lists "Publisher Correction: Parabolic approximation & relaxation for MINLP", J. Glob. Optim. 95(4) (2026) 1095–1141, doi:10.1007/s10898-026-01614-9. It has 47 pages, so it apparently republishes the article; the original Crossref record spells the first author "Göss". I could not read it: there is no archived copy, and Springer and Econstor show bot pages. I did confirm Table 17 in an archived copy of the original JOGO PDF (`sources/goss_jogo_2026_archive.pdf`, PDF p. 38 = p. 988):
   - eg_int_s, SCIP, original model: 9085.1 s, 6.5 | 6.5.
   - eg_disc_s, SCIP\* (excluded for errors): limit, 3.6 | 5.8.
   - eg_disc2_s, SCIP: limit, −1.1 | 6.3. Gurobi: −5.2 | 7.0 (eg_disc2_s) and 2.0 | 7.5 (eg_disc_s).

   The paper should cite the correction and check that Table 17 did not change.

4. **The gap tolerance for "solved" can be pinned down.** The GAMS 32.1.0 release notes (July 2020, `docs/RN_32.html`) list optCR among the "new default values": 0.0001, previously 0.1. Göß et al. used GAMS 46.4.0 with "default settings". So "solved" means a relative gap ≤ 1e-4, unless they overrode it. The report says this was not checked for 46.4.

5. **Two dual bounds are rounded the wrong way.**
   - ex6_2_5: the report prints −70.75207783344770758. The proved bound is −70.7520778334477075803539…, so the printed value lies 3.5e-19 above it.
   - etamac: the report prints −15.294675643368092. The proved bound is −15.2946756433680921685…, so the printed value lies 1.7e-16 above it.
   - The summary already uses the outward-rounded −…759 and −…093 (`reviews/closing-confirm-r2.md`, `-r3.md`). Use those.

6. **Missed local-solver sources on HVYCRASH.** These are local results only and do not change any consequence. Both appear in the author's own OpenAlex hit list for "hvycrash" (8 hits), but neither is in the report.
   - Omheni, PhD thesis, Univ. Limoges, 2014, HAL tel-01136063. N = 1000, n = 4002 (PDF p. 120). Final objectives 1.1e-19, −1.8e-1, 9.3e-16 and −6.9e-2 in four result tables (PDF pp. 134, 146, 158, 170).
   - Prudente, thesis, Unicamp, 2012, doi:10.47749/t/unicamp.2012.862465. Not fetched: the DOI resolves to an HTML page.

7. **A likely primary source is not listed among the unread ones.** McDonald & Floudas, "Decomposition based and branch and bound global optimization approaches for the phase equilibrium problem", J. Glob. Optim. 5 (1994) 205–251, doi:10.1007/BF01096454. Floudas, *Deterministic Global Optimization* (Kluwer, 2000), doi:10.1007/978-1-4757-4949-6, is also relevant. I could not read either.

8. **pricing050: two caveats.**
   - The ORL formulation (9b) is printed as Σ a x e^{−x^k} with x ∈ [0, 10], without the 1/10 scaling that Davarnia & van Hoeve and pricing050 use. The values (UB 1813.3 next to the integer value 1825) suggest the scaled model was run. Still, this is a second possible source of the discrepancy, next to the report's "transcription error, or different data".
   - Both tables come from optimization-online preprints (7681 and 6512), not the published ORL and MP versions. The report gives preprint page numbers, but side finding 2 and Section 12 cite "Davarnia (2021, Table 1)" as if it were the journal version.

9. **`minlplib.solu` disagrees with the instance pages.** Its `=bestdual=` values differ from the best dual bounds on the pages for several instances:

   | instance | `minlplib.solu` | instance page |
   |---|---|---|
   | etamac | −16.399 | −15.40567 (SCIP) |
   | ex6_2_7 | −1.3547 | −1.0673 (BARON) |
   | pindyck | −1889.89 | −1437.94 (SCIP) |
   | pricing050 | −1153.0 | −1534.33 (SCIP, max form) |
   | eg_int_s | 0 | 6.3263 (SCIP) |
   | eg_disc_s | −0.2568 | 3.3660 (SCIP) |
   | eg_disc2_s | −5.2258 | 0 (SHOT) |

   The report uses the page values, which I confirmed. Since it lists `minlplib.solu` as a source, it should say that "MINLPLib best dual" means the instance page.

10. **Trombettoni et al. (2011): tolerance stated too broadly.** The report says the solvers ran with ε_obj = 1e-8. The Table 2 header shows Icos at 1e-3 and IbexOpt at both 1e-3 and 1e-8.

11. **Small additions that would help the paper.**
    - The COCONUT ex6_2_7 file for BARON 7.2 has model status 2 (locally optimal). This supports "primal value only".
    - The CAMINO paper (arXiv:2404.11786) calls its method a heuristic without global guarantees on nonconvex MINLPs, and its arXiv text has no eg_* entries. This supports the report's "probably primal only".

## Claims I confirmed

These checks used my own reading of the sources, Crossref, and the reviewer code listed below.

- **Source manifest.** 101 rows; all sha256 values match; no unlisted or missing files (`logs/manifest_check.log`).
- **Bibliographic data.** Correct for all 24 DOIs looked up on Crossref (`crossref/*.json`). The DOIs, volumes and pages of Göß et al., Davarnia ORL, Davarnia & van Hoeve, Davarnia–Kiaghadi–Qiu, Cristofari et al., Ninin et al., Trombettoni et al., Najman et al., Tessier et al., Stadtherr et al., Tawarmalani & Sahinidis, Gleixner et al., Müller et al., McDonald & Floudas (1995, 1997), Mitsos & Barton, Pindyck, Tyatushkin et al., D'Ambrosio et al., Gomes, Smith, Ahmadzadeh & Mahdavi-Amiri and the handbook are as stated.
- **MINLPLib.** All current and 2018/2024 best duals quoted in the report match the cached pages:
  - hvycrash: −2.185e8 SCIP; none in 2018.
  - ex6_2_7: −1.06726714 BARON. ex6_2_5: −111.4201713 BARON.
  - etamac: −15.83529486 ANTIGONE (2018); −15.40567054 SCIP (now).
  - pindyck: −1437.941134 SCIP.
  - pricing050: −1534.3281 SCIP; none in April 2024.
  - eg_int_s: −1.205 LINDO (2018); 6.32629896 SCIP (now).
  - eg_disc_s: −4.0246 LINDO; 3.36596129 SCIP.
  - eg_disc2_s: −7.5659 LINDO; 0 SHOT.

  Sources and "added" dates also match. Point histories match: COUENNE 2017–2018; CONOPT 15 Aug 2014; LaGO/CONOPT3 11 Jan 2007; SBB/CONOPT3 25 Jul 2002; KNITRO/Latifoğlu 26 Aug 2024.
- **Göß et al.** Setup: SCIP 8.1 and Gurobi 11.0.1 through GAMS 46.4.0, 8 threads, 4 h limit (arXiv v2, lines 817–820 and 1079). Table 17 values as above. The "reverse reading" of the primal | dual columns is right: only that reading is consistent for a minimization problem.
- **pricing050.**
  - My own .gms parser was cross-checked against the cached OSIL (row values agree to 7e-16). A HiGHS MILP with 550 binaries gives an integer-version optimum of **1825.0** with zero gap (`pricing050_integer_milp.py`, `logs/pricing050_integer_milp.log`). This is floating-point evidence.
  - Davarnia & van Hoeve, Table 6.1 (preprint p. 20), n = 50: UB = 1592, 1825, 1891, 2403, 1800. For #2: DD 1786.3, ANTIGONE 1063.3, BARON 1299.0, COUENNE 1452.5, SCIP 1367.2. Confirmed.
  - ORL Table 1 (preprint p. 18), n = 50 #2: 1813.3 / 1663.7 / 1037.4 / 1354.2 / 1437.6 / 1368.3. Confirmed.
  - Lagrangian check, rerun: λ ≈ (0, 0, 0, 3.0489, 2.1678), q(λ) = 1813.829078. Reaching 1813.3 needs a relative row relaxation ≥ 1.17e-4, about 0.10 absolute (`logs/pricing050_dual_check.log`). The inconsistency stands.
- **pindyck COCONUT value.**
  - Recomputation, rerun: J = 1612.17830322903321 with exponent factor 1, and 1057.2183755 with factor 1/7, where the minimum OPEC demand is −0.869 (`pindyck_coconut_check.py`, `logs/pindyck_coconut_check.log`).
  - The COCONUT .gms (dag2gams, 29/03/2004) uses exp(−0.0198026…·x) = 1.02^(−x). The COCONUT .mod has the correct `1.02**(-0.142857142857143*x52)`.
  - GAMS Model Library seq(t): `1.02**(-cs(t)/7)`. x51.fx = 0 in both the MINLPLib and GLOBALLib files.
- **Gibbs problems.**
  - The handbook start levels in `titan/ex6.2.7.gms` and `ex6.2.5.gms` match the report. Rerun of `handbook_start_vs_opt.py`: maximum distance 4.32e-4 and 2.98e-5; objective excess 8.15e-7 and 1.0e-10.
  - Handbook objective vs OSIL: earlier reviewer checks (GAMS evaluation; mpmath at 200 points) agree to 4e-14 relative (ex6_2_7) and 2.7e-13 (ex6_2_5, GAMS double).
  - Tessier et al. (2000), Table 10, is on preprint p. 28. Its feeds are (0.27078, 0.47302, 0.25620) and three (0.4/0.3/0.3)-type feeds, none of them (0.4, 0.1, 0.5).
  - Stadtherr et al. (2007): the α-BB quote is on PDF p. 2.
- **Interval solvers and MAiNGO.**
  - Ninin (2010): Table 3.1 on printed p. 63, "F" for both instances. Table 3.6 on printed p. 71: −66.227346367 after 4025.53 s and −7036.008545972 after 4036.35 s.
  - Trombettoni et al. (2011), p. 103: quote verbatim; BARON 9.0.7 on NEOS, 1000 s.
  - Najman et al. (2021), Table 7: ex6_2_7 at 28 800 s with ratios 14.77%–17.83%; tolerance 1e-4.
- **etamac and pindyck root-node studies.**
  - Tawarmalani & Sahinidis (2005): Table 1 on p. 242 has (8) etamac and (28) pindyck. Neither is among the 26 problems of Table 4 (p. 246).
  - Gleixner et al. (2017): both in Tables 4 and 6, absent from Table 8. The exclusion rules are as stated.
  - Müller et al. (2020): pindyck in Table 4 (−2239.98, −3972.57, −1170.49) and Table 5 (1800 s; 233.6K, 240.0K, 265.6K nodes); etamac only in Table 3.
  - Smith (2011): pindyck removed because of AMPL convalQ errors (PDF p. 71); hvycrash −1.905155235 in Table A.1. The τ ≈ 0.03 arithmetic is right.
- **eg_* instances.**
  - COIN-OR 2008 traces: BARON 8.1.5 bound −8.0807 for all three. LindoGlobal bounds −3.1577, −7.3125, −9.9793. Primal values as stated.
  - Cristofari et al. (2026), Table 1: 6.4531, 5.7605, 5.6421. Blomqvist (2025) lists the eg_* instances.
  - The GAMS World eg_int_s header says 26 equations; the file and the current model have 28.
- **HVYCRASH local studies.** Gomes (2007, p. 375), Buchanan (PDF pp. 115 and 124) and Andretta (PDF pp. 46–47) are quoted correctly. Their interpretation must change (M1).

## Own searches for missed prior results

- **WebSearch (10 queries):**
  - Kiaghadi dissertation and pricing.
  - "etamac" global optimum.
  - "pindyck" GLOBALLib global solvers.
  - "lauryl alcohol" "nitromethane" "ethylene glycol" Gibbs global UNIQUAC.
  - "ex6_2_7" OR "ex6_2_5" global optimization.
  - "eg_disc_s" OR "eg_int_s" OR "eg_disc2_s".
  - The CAMINO/SB-MIQP paper.
  - "hvycrash" test problem.
  - Davarnia pricing "1813".
- **Fetched and grepped for the nine names:**
  - Puranik & Sahinidis (arXiv 1706.08601).
  - GAMS present_cocos02.
  - SCIP 8 report (arXiv 2301.00587).
  - Bertsimas & Öztürk (arXiv 2202.06017).
  - Pintér (optimization-online 2002/523).
  - CAMINO (arXiv 2404.11786).
  - Davarnia & Kiaghadi (arXiv 2505.03899).
  - Neumaier et al., "A comparison of complete global optimization solvers" (2005 preprint) and the COCONUT solver-comparison index.

  Only Bertsimas & Margaritis matched (minor issue 2).
- **Other databases:**
  - The NSF PAR listing for Kiaghadi shows no pricing paper.
  - OpenAlex full text: 6 extra phrase queries, all with 0 hits ("ex6.2.5", "ex6.2.7", "ETA-MACRO global optimization", "etamac BARON", "pindyck BARON", "pindyck SCIP").
  - Semantic Scholar snippet search: HTTP 429.
- **Earlier reviewers in this role** also found McKinnon & Mongeau (1996; different ternary systems, no match) and confirmed that the GlobalDD v1 paper and Mittelmann's 200-instance set contain none of the nine instances.

No missed source changes any "consequence" label. The "new as far as found" labels for etamac, pindyck, pricing050, eg_disc_s and eg_disc2_s stand. So do "already solved globally in floating point" for eg_int_s and "partly known" for ex6_2_7, ex6_2_5 and hvycrash. For hvycrash, the reason becomes stronger after M1.

## Does the report state what is proved, numerical or unread?

Mostly yes. Model identity and the pricing050 instance identity are labelled numerical, and unread sources are listed. The one exception is the SIF infeasibility, which is labelled "exact and checked by hand" but rests on a misreading of the bounds (M1). The commands-run section is complete and specific.

## Commands I ran

All runs were single-process, using at most one core at a time. No project-wide checks were run, CI was not inspected, nothing was committed or posted, and no background jobs remain.

- **Predecessor transcripts:** read with Python (agent-a466d3d5d15e69f4d in wf_a89a60b6-d10; agent-a79644883f3179a88 in wf_6b4c8c17-543).
- **SIF checks:**
  - `curl` of `ralna/SIFDecode/master/src/decode/sifdecode.f90`, then `grep`/`sed` of SBOUND (lines 4935–5120).
  - GitHub API commit list for `HVYCRASH.SIF`, and `curl` of the 2013 version.
  - `sed` of the BOUNDS, ELEMENTS and GROUP USES sections of both SIF versions.
  - AMPL bound summary of `hvycrash.mod`.
  - PrincetonLib bound `grep`.
  - Reading of the archived SIF manual page 3.2.12.
- **Crossref:** `curl api.crossref.org/works/<doi>` for 27 DOIs (`crossref/`).
- **Göß et al.:** OpenAlex OA lookups; `curl` of the Wayback copy of the Springer PDF; `pdftotext` and Table 17 extraction. Econstor and the Springer correction failed (bot page; no archive copy).
- **pricing050:** `OMP_NUM_THREADS=1 python3 pricing050_integer_milp.py` → 1825.0. `OMP_NUM_THREADS=1 python3 pricing050_dual_check.py` → q = 1813.829078, δ ≥ 1.17e-4.
- **Handbook start points:** `OMP_NUM_THREADS=1 python3 handbook_start_vs_opt.py` → 4.32e-4 / 8.15e-7 and 2.98e-5 / 1.0e-10.
- **pindyck:** `python3 pindyck_coconut_check.py` → 1612.17830322903321 / 1057.2183755.
- **Manifest:** Python sha256 check of the track manifest → 101 rows, 0 bad.
- **MINLPLib pages:** page-to-text extraction of the current, 2018 and 2024 pages and the point pages; `grep` of `minlplib.solu`.
- **Saved sources:** `pdftotext`/`grep` on the saved PDFs (Göß arXiv and JOGO, ORL, Davarnia & van Hoeve, Ninin, Trombettoni, Najman, Smith, Gomes, Buchanan, Andretta, Müller, Tessier, Stadtherr, Omheni).
- **Local literature collection:** `grep` of `literature/papers/*/fulltext.md` for Tawarmalani & Sahinidis 2005, Gleixner et al. 2017 and Cristofari et al. 2026.
- **COIN-OR traces:** `awk` on the 2008 trace files.
- **GAMS docs:** `RN_32.html` and `optgams.def` for the optCR default.
- **Web:** the WebSearch, WebFetch-free `curl` fetches and OpenAlex/Semantic Scholar queries listed above, run sequentially about 1 s apart.

Results reused from earlier reviewers in this role, not rerun: `gibbs_gams_vs_osil.py` (GAMS evaluation, logs in `gams/`) and the `/tmp/lsr` mpmath Gibbs comparison. They agree with the author's figures to rounding.
