<!-- Written to disk by the root from the structured return value of fixer round 2 of track lit-small in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Literature check: small process, economics and geometry models (track lit-small)

Date: 2026-10-01. Revised 2026-10-03 after review rounds 1–3 (Sections 16–18).

**Instances:** hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck, eg_int_s, eg_disc_s, eg_disc2_s.

**Claims checked:** those in `research-20260929/open-instances-summary.md` and the notes it links (`open-instances-wave2/small/report.md`, `open-instances-wave2/small/pindyck-extension.md`, `open-instances-wave3/eg/retry.md`).

**Status:** the planned searches are finished. Some key sources could not be read (Section 13). A search that finds nothing does not show that a result is new.

Labels used below:
- **rigorous**: a bound proved with exact or outward-rounded arithmetic.
- **floating-point global**: a deterministic global solver or an ε-global method reports optimality within its own tolerances.
- **local**: a value from a local or heuristic solver.
- **listing**: a value given in a test library.

**Files.**
- **Sources:** copies of fetched sources are in `publication/literature/small/sources/`. `sources/manifest.tsv` gives each file's URL, fetch date and sha256. It lists 129 files:
  - 101 fetched on 2026-10-01;
  - 11 added on 2026-10-02 in the first revision;
  - 16 added on 2026-10-02 in the second revision;
  - one added on 2026-10-03 in the third revision, copied from the round-3 review's saved source.
- **Checks:** the checks written for this track are in `checks/`, with logs in `checks/logs/`. Most give numerical evidence, not proofs. Three are exceptions:
  - `hvycrash_sif_bounds.py` only reads bound cards and does no floating-point arithmetic.
  - `eg_camino_gurobi.py` and `eg_int_s_oldpoint.py` evaluate the eg_* rows in outward-rounded interval arithmetic (mpmath `iv`). Their assumptions are stated in the scripts and in Section 9.2.

**"MINLPLib best dual"** means the best dual bound on the MINLPLib instance page. The file `minlplib.solu` lists different, weaker values (Section 2).

## 1. Summary

| instance | provenance (is the MINLPLib model the source model?) | strongest prior result found | consequence for our claim |
|---|---|---|---|
| hvycrash | CUTE problem HVYCRASH (SIF file by Ph. Toint, 1994) at N = 50, which the SIF file calls the "original value". **Same model.** SIFDecode applies the SIF bound cards in order; under that rule the SIF fixes only X(1,0) and X(2,0), and all θ_T lie in [0, 2π]. Yurttan's AMPL translation has exactly these bounds. MINLPLib's model is that translation, with the fixed X(1,0) and X(2,0) and the unused U(0) eliminated. | listing: the SIF file gives the solution value SOLTN = −0.21850 without a proof. No N is attached; it is presumably for N = 50. No global result or dual bound was found in the literature. These published values cannot come from feasible points: −0.0481 (COCONUT); −1.905 (Smith 2011); the SIF's SOLTN values for N = 100, 500 and 1000 (about 1e-8); and the local-solver objectives in Omheni (2014) at N = 1000 (−0.18 to 1.1e-19). | **partly known**. The optimal value is on record for the identical problem, at least since the 2013 repository version of the file. The identity (the objective is constant on the feasible set) and an exactly feasible point are new as far as found, but both are elementary. |
| ex6_2_7 | Floudas et al. handbook (1999), Ch. 6, Test Problem 7: ethylene glycol – lauryl alcohol – nitromethane, UNIQUAC, three liquid phases. **Same model**: the handbook GAMS model with constants rounded to double (relative difference ≤ 4.1e-14). | floating-point global, very likely but not read: MINLPLib cites McDonald & Floudas (1997, GLOPEQ), a deterministic ε-global method. The handbook GAMS start point is within 4.3e-4 of our optimum, with objective 8.2e-7 above it. Rigorous interval solvers and BARON failed (2010–2015). MAiNGO failed in 8 h (2021). Bertsimas & Margaritis (2025) label BARON "GOpt" (gap < 0.1%, gap not defined) after 1502 s with a 1500 s limit. That is not a certificate. | **partly known**. The optimal value was very likely reported as an ε-global solution in floating point. No rigorous certificate was found, so ours is new as far as found. |
| ex6_2_5 | Same handbook, Ch. 6, Test Problem 5: sec-butyl alcohol – di-sec-butyl ether – water, with UNIQUAC liquids and an ideal vapour. **Same model** up to rounding (≤ 9.4e-14). | As for ex6_2_7, including the BARON "GOpt" label at 1502 s (Bertsimas & Margaritis 2025). The handbook start point is within 3.0e-5 of our optimum, with objective 1.0e-10 above it. Interval solvers and BARON failed (2010–2015). Kosolap (2019) reports −70.9586, which is 0.2065 below our certified lower bound and so not attainable. | **partly known**, as for ex6_2_7. |
| etamac | GAMS Model Library model etamac (SEQ=80), A. Manne's ETA-MACRO (1977). **Same model** as the GLOBALLib scalar version (checked). Not checked against Manne's text. | local: MINOS −15.2947 (COCONUT) and CONOPT point p1 (MINLPLib). Global solvers: root-node studies only (BARON 2005, SCIP 2017). | **new as far as found**. No global claim or certificate was found. |
| pricing050 | Continuous version of the marketing pricing model of Davarnia & van Hoeve (2021), n = 50. There is strong evidence that it is their instance #2 (Section 7). Contributed to MINLPLib in 2024 by M. Kiaghadi. | Dual bounds only: decision-diagram bound 1663.7 and solver bounds ≤ 1437.6 (Davarnia 2021, 300 s; read in the preprint). MINLPLib best dual 1534.33 (SCIP). All values in min form. | **new as far as found**. The primal value 1813.3 that Davarnia (2021) reports for instance #2 is below our certified minimum 1813.829. |
| pindyck | GAMS Model Library model pindyck (SEQ=28), after Pindyck (1978). **Same model** as the GLOBALLib scalar version. | SCIP studies did not solve it: root bound −2239.98, and the 1800 s tree runs hit the limit (Müller et al. 2020). The COCONUT "best" value −1612.18 belongs to a mistranslated model. | **new as far as found**. |
| eg_int_s | "Bram Schoonen's Model Collection" (MINLPLib, 2002). We found no document on its origin. | floating-point global: SCIP 8.1 solved it (Göß, Burlacu, Martin 2026: 9085 s on 8 threads). The stopping gap is very likely GAMS's default optCR = 1e-4 (Section 9.2). A wrong claim also exists: in the CAMINO benchmark data (2026), Gurobi 13.0.0 reported best bound = objective = 11.654 before its time limit. The optimum is ≤ 6.4531 (Section 9.2). | **already solved globally in floating point**. As far as found, ours is the first rigorous certificate. |
| eg_disc_s | same collection | Best valid dual 3.6 (SCIP 8.1, 4 h; the authors flag this run for numerical or memory errors). MINLPLib best dual 3.366 (SCIP). In the CAMINO benchmark data (2026), Gurobi 13.0.0 claimed optimality at 6.1918 (bound = objective). This is wrong: the optimum is ≤ 5.7605 (Section 10.1). | **new as far as found** |
| eg_disc2_s | same collection | Best valid dual −1.1 (SCIP 8.1, 4 h). MINLPLib best dual 0 (SHOT). In the CAMINO benchmark data (2026), Gurobi 13.0.0 claimed optimality at 5.8867 (bound = objective). This is wrong: the optimum is ≤ 5.6421 (Section 11.1). | **new as far as found** |

Side findings the paper may need (details in Section 12):
1. **pindyck, COCONUT.** The COCONUT benchmark's best value for pindyck (−1612.1783) comes from a translation that drops the factor 1/7 in the exponent. It is not a value of the MINLPLib model.
2. **pricing050, Davarnia (2021).** Table 1 of Davarnia (2021, ORL), as printed in the optimization-online preprint, gives the primal value 1813.3 for the instance that is very likely pricing050. We did not read the journal version. Our certified minimum is 1813.8290784519…. Unless the data or the model differ, no feasible point of pricing050 has that value.
3. **HVYCRASH SIF file.** The XX cards that fix θ_0 and θ_N at 0 have no effect, because a later loop sets [0, 2π] for every θ_T. Whether the author meant to fix these two variables is unknown.
4. **hvycrash values that are not feasible.** Every feasible point has objective −0.2185, for every N. So the following values cannot come from feasible points:
   - −0.0481 (COCONUT) and −1.905155235 (Smith 2011);
   - the SIF's SOLTN(100), SOLTN(500) and SOLTN(1000), which are about 1e-8;
   - the local-solver objectives in Omheni (2014).
5. **ex6_2_5 and ex6_2_7, "GOpt".** Bertsimas & Margaritis (2025) label BARON's results on these instances "GOpt". This is not a proof of global optimality and should not be cited as one (Sections 4.2 and 5.2).
6. **eg_\*, Gurobi 13.0.0 in the CAMINO benchmark.** On eg_disc2_s, eg_disc_s and eg_int_s, Gurobi 13.0.0, run through AMPL, stopped well before its time limit. Its reported best bound equaled its objective: 5.8867, 6.1918 and 11.654. These are claims of global optimality, and all three are wrong. The project's recorded points are feasible for the same .mod models, which we proved in interval arithmetic. Their objectives are lower by 0.2446, 0.4313 and 5.2011 (4.3%, 7.5% and 81%). The cause is unknown.
7. **ex6_2_5, Kosolap (2019).** Table 1 gives −70.9586 for Ex6_2_5 (method EQR). This is 0.2065 below our certified lower bound, so no feasible point of the MINLPLib (= GLOBALLib) model has that value.
8. **Tolerance-level values below the eg_\* certified bounds.** Both are tolerance artifacts:
   - The old GAMS World point of eg_int_s has objvar 6.4531031527. It violates row e12 by 6.4e-9.
   - The CAMINO data give S-B-MIQP the value 5.642100351878204 on eg_disc2_s. That is 2.2e-7 below our certified lower bound.

## 2. How the search was done

- **MINLPLib.**
  - Current instance pages (cached in `bound-audit/pages/`), point pages (`sources/minlplib_points/`) and the file `minlplib.solu`.
  - The earliest Internet Archive snapshot of each instance page, saved in `sources/minlplib_history/`: 2018-09-22, or 2024-04-13 for pricing050.
  - The AMPL `.mod` files of eg_disc2_s, eg_disc_s and eg_int_s (`sources/eg/minlplib_mod/`; fetched in the second revision).
  - **"MINLPLib best dual" means the instance page.** The `=bestdual=` values in `minlplib.solu` differ from the pages. They are weaker for all nine instances (for pricing050, a maximization problem, weaker means larger), and hvycrash has no `=bestdual=` line. We do not know why they differ. This report uses the page values.

    | instance | `minlplib.solu` `=bestdual=` | instance page: best dual (solver) |
    |---|---|---|
    | hvycrash | none | −2.185e8 (SCIP) |
    | ex6_2_7 | −1.354737094 | −1.06726714 (BARON) |
    | ex6_2_5 | −364.1162233 | −111.4201713 (BARON) |
    | etamac | −16.3990195 | −15.40567054 (SCIP) |
    | pricing050 (max) | −1153.003281 | −1534.3281 (SCIP) |
    | pindyck | −1889.888367 | −1437.941134 (SCIP) |
    | eg_int_s | 0 | 6.32629896 (SCIP) |
    | eg_disc_s | −0.2567667014 | 3.36596129 (SCIP) |
    | eg_disc2_s | −5.225776378 | 0 (SHOT) |
- **Original sources:**
  - the GAMS World archive on GitHub (GLOBALLib and old MINLPLib scalar models, PrincetonLib CUTE translations);
  - the handbook's web supplement (titan.princeton.edu, archived copy);
  - the CUTE SIF file (two versions) and the SIFDecode source;
  - Vanderbei's AMPL file;
  - the GAMS Model Library pages and the COCONUT benchmark pages.
- **Literature**:
  - WebSearch, about 25 queries (listed in Section 14).
  - OpenAlex full-text search, 22 queries. This found most of the useful papers. One hit was not followed up in the first version: Kosolap (2019), returned by the query "ex6_2_5". The round-2 reviewer found and read it; it is now in Section 5.2.
  - Crossref for bibliographic data.
  - The project's local literature collection (`literature/papers/`), searched with grep for every instance name.
  - DuckDuckGo: one useful query before it was rate-limited.
  - In the second revision: the public data repository of the CAMINO paper (CAMINO-benchmark on GitHub).
- **Reading**: every fact below was read in the source itself (PDF text, HTML or data file), not taken from search snippets, unless it is marked "not read".

## 3. hvycrash

**Our claim.** The objective equals −0.2185 at every feasible point. This is an exact identity that follows from the rows alg_k. An exactly feasible point exists, so the optimum is −0.2185 (wave-2 small report, Section 3; verified).

### 3.1 Provenance
- **MINLPLib page**: source "CUTE model hvycrash", added 6 Feb 2017. References: Ivashkevich (1976) and Tyatushkin, Zholudev & Erinchek (1992).
- **SIF file** HVYCRASH (`sources/hvycrash/HVYCRASH.SIF`). It says "SIF input: Ph. Toint, February 1994" and "Updated to improve processing, Pim Heeman, May 2026".
  - The header calls the problem "freely inspired by" the heavy spacecraft landing problem. Because "No feasible point was found for the original formulation by any of the packages at hand", it drops the final-state constraint on the second variable and sets EPS = 0 in the second constraint. It also calls the problem "badly scaled degenerate".
  - Classification LOR2-AN-V-V. Objective X(1,N). Variables X(1,T), X(2,T) = r_T, X(3,T) = θ_T and U(T), for T = 0..N.
  - N = 50 is marked as the "original value"; the current default is N = 1000.
  - The first version of the file in the ralna/SIF repository (commit a4c9117d7d, 2013, imported from the CUTEst svn; `sources/hvycrash/HVYCRASH_2013_a4c9117d7d.SIF`) differs from the 2026 version only in the "Updated" header line and in the spacing of the SOLTN lines.
- **Bounds of the SIF problem.**
  - The BOUNDS section first makes all variables free (`FR HVYCRASH 'DEFAULT'`).
  - XX cards then fix X(1,0) = 0, X(2,0) = 2.19905, X(3,0) = 0 and X(3,N) = 0.
  - Finally, a loop `DO T 0 N` sets U(T) ∈ [0.08, 0.417] and X(3,T) ∈ [0, 6.2831854].
  - SIFDecode applies individual bound cards in file order, and a later card overwrites an earlier one. In subroutine SBOUND of `sifdecode.f90` (ralna/SIFDecode master, sha256 06cfe6d7…, saved in `sources/hvycrash/`), an individual card assigns `B_l( ncol, nbnd ) = value4` and `B_u( ncol, nbnd ) = value4` unconditionally (around lines 5060 and 5090).
  - So the loop overrides the XX cards for X(3,0) and X(3,N). In the decoded problem only X(1,0) and X(2,0) are fixed, and θ_0 and θ_N lie in [0, 2π] like every other θ_T. The 2013 version has the same BOUNDS section.
  - Our check `checks/hvycrash_sif_bounds.py` applies the cards in this order to both file versions:
    - N = 50: 204 variables, of which only X(1,0) and X(2,0) are fixed, and every θ_T ∈ [0, 6.2831854].
    - N = 1000: 4004 variables, with the same fixed variables and θ bounds.
    - At N = 50, all 204 variables have the same bounds as in the AMPL file.
    - The logs are `checks/logs/hvycrash_sif_bounds_N50.log` and `…_N1000.log`. The round-1 reviewer reached the same result independently from the SIFDecode source, and the round-2 reviewer with a separate bound decoder.
  - Two independent variable counts agree: COCONUT Library 2 lists hvycrash with 202 variables, and Omheni (2014, PDF p. 120) lists HVYCRASH at N = 1000 with n = 4002. Both are the total minus two fixed variables.
- **AMPL translation** by Hande Yurttan (Vanderbei's CUTE collection, `sources/hvycrash/hvycrash.mod`, N = 50):
  - x1_0 = 0 and x2_0 = 2.19905 are fixed;
  - all 51 x3_k ∈ [0, 6.2831854];
  - all u_k ∈ [0.08, 0.417].

  It is a faithful translation of the SIF problem at N = 50.
- **MINLPLib hvycrash is the SIF problem at N = 50.**
  - It has 201 variables plus objvar: the 204 minus x1_0, x2_0 (fixed) and u0 (in no row). x1_0 = 0 is substituted.
  - θ_0 = x101 and θ_1..θ_50 = x1..x50 lie in [0, 6.2831854]. The controls U(1..50) = x51..x100 lie in [0.08, 0.417].
  - Its rows have the form of the SIF rows C(1,T), C(2,T) and C(3,T), with H = TT/50 = 0.00437, 1.62079·0.01 = 0.0162079 and 1.62079·0.3 = 0.486237. I compared the rows by inspecting their form.
  - The round-2 reviewer's independent code also compared them numerically. It transcribed the SIF rows at N = 50 by hand and evaluated them against the rows of the cached OSIL at 20 random points × 150 rows in 50-digit arithmetic. The maximum difference was 2.1e-48, using the map θ_T = x_T, θ_0 = x101, U(T) = x_{50+T}, r_T = x_{101+T}, X(1,T) = x_{202−T}; the objective is X(1,50). Code and log: `reviews/lit-small-r2/hvycrash_check.py` and `reviews/lit-small-r2/logs/hvycrash_check.log`.
- **The GAMS World PrincetonLib translation is a variant** (indexed model file, lines 714–822), with epsi = 0.005:
  - it fixes x1_0 at 0 + epsi = 0.005 and x2_0 at 2.19905 + epsi = 2.20405;
  - it gives all 51 θ_k the bounds [0.005, 2π + 0.005];
  - u_k ∈ [0.08, 0.417].

  By the identity below, any feasible point of this variant has objective 0.005 − 0.2185 = −0.2135. We did not check that the variant has feasible points.
- **The identity holds for the SIF problem at every N** (exact algebra, checked by hand from the element definitions INV, C2 and C3):
  - Row C(2,T) reads −1/r_T − cos θ_T/(A·C_T·r_T³) = 0, with A = 1.62079 and C_T = 0.01 + 0.3 U(T)² > 0. Hence cos θ_T/(A·C_T·r_T²) = −1.
  - Row C(1,T) reads X(1,T−1) − X(1,T) + H·cos θ_T/(A·C_T·r_T²) = 0, so X(1,T) = X(1,T−1) − H.
  - Therefore X(1,N) = X(1,0) − N·H = −TT = −0.2185 at every feasible point.
  - Row C(2,T) also forces cos θ_T < 0. So θ_N = 0 is infeasible, but the SIF problem does not fix θ_N.

### 3.2 Prior results
- **SIF file, solution lines** (listing, no proof).
  - "`*LO SOLTN -0.21850`", with no N attached. The other lines are SOLTN(100) = 3.26705331D-8, SOLTN(500) = 2.36171208D-8, SOLTN(1000) = 8.48265630D-8 and an empty SOLTN(3000). The unlabelled value is therefore presumably for the original N = 50, the MINLPLib instance.
  - The lines are in the 2013 version. When they were added is not recorded.
  - −0.21850 equals −TT, the value the identity forces. The file gives no proof or explanation.
  - SOLTN(100), SOLTN(500) and SOLTN(1000) cannot be objective values of feasible points, because every feasible point has objective −0.2185 for every N. They presumably come from points that satisfy the rows only within a solver tolerance.
- **COCONUT benchmark, Library 2** (#2439; `sources/coconut/`): the table gives Fbest = −0.0481. The linked "best solution" (solver OQNLP) has objective −0.1573199996, model status 5 and "infeas = 14". Neither value comes from a feasible point. The COCONUT Library 2 model is Vanderbei's `hvycrash.mod` (round-2 reviewer), so the identity applies.
- **Smith (2011), PhD thesis, Carleton University**, Appendix A, Table A.1 ("Best Known Objective Function Values for Feasible Solution Vectors to Test Models from the COCONUT Benchmark"): hvycrash −1.905155235.
  - By the tolerance remark in our wave-2 report (Section 3), a point whose rows are violated by at most τ has objective ≥ −0.2185(1 + 7.86τ) − 50τ.
  - Reaching −1.905 needs τ ≈ 0.03, so this is not the value of a feasible point.
- **Local-solver studies of the CUTE HVYCRASH** (local results). The problem is feasible but badly scaled, and these reports concern local solvers that struggled with it:
  - Gomes (2007), p. 375: HVYCRASH (n = 4004, m = 3000, so N = 1000) is among the problems where the GMM code "has found a lower objective function" than Lancelot.
  - Buchanan (2008), MPhil thesis (Edinburgh), at N = 50 (201 variables, 150 constraints), PDF pp. 115 and 124: iteration limit; "Feasible point is never found".
  - Andretta (2008), USP thesis, PDF pp. 46–47: Algencan stops at the time or iteration limit.
  - Omheni (2014), PhD thesis, Univ. Limoges (HAL tel-01136063; archived copy in `sources/hvycrash/`): N = 1000, n = 4002, m = 3000 (PDF p. 120). Final objective values:
    - SPDOPT 1.1e−19 (PDF p. 134);
    - IPOPT −1.8e−1 (PDF p. 146);
    - ALGENCAN 9.3e−16 (PDF p. 158);
    - LANCELOT-B −6.9e−2, with failure code 1, "maximum number of iterations reached" (PDF p. 170).

    The first three carry no failure flag. None equals −0.2185, so none of the returned points is exactly feasible.
  - Ahmadzadeh & Mahdavi-Amiri (2026) include it in their test set at N = 50 (204 variables, 150 constraints).
  - Prudente (2012), Unicamp thesis "Inviabilidade em métodos de lagrangiano aumentado", is an OpenAlex hit for "hvycrash". **Not read**: the repository returned HTTP 503 three times.
  - None of the sources read states the identity or proves an optimal value.
- **MINLPLib**:
  - Points p1–p3 were found by COUENNE (2017–2018). p3 = −0.2185 (infeasibility 1e-12). p1 and p2 = −0.21413 are tolerance artifacts (our report).
  - The only dual bound is SCIP's −2.185e8. The 2018 snapshot lists no dual bound.

### 3.3 Consequence
**Partly known.**
- The SIF file records the optimal value −0.21850 for the identical problem (N = 50, the MINLPLib instance), without a proof. The value is present at least since the 2013 repository version.
- MINLPLib still lists the instance as open.
- We found no source that says the objective is constant on the feasible set, or that gives an exactly feasible point.

The closure is a short exact argument, not a computational result. The paper should present it that way and credit the SIF value.

## 4. ex6_2_7

**Our claim.** Rigorous dual bound −0.16084761546364905 (the verifier's value), with gap 4.8e-14 to an exactly feasible point. Method: a Lagrangian over the mass balances plus a tangent-plane test by interval branch and bound.

### 4.1 Provenance
- **MINLPLib**: "Test Problem ex6.2.7 of Chapter 6 of Floudas e.a. handbook". References: the handbook (Floudas et al. 1999) and McDonald & Floudas (1997, GLOPEQ). Added 31 Jul 2001.
- **Handbook web supplement** (archived copies in `sources/titan/`):
  - Chapter 6 is "Biconvex and Difference of Convex Functions (D.C.) Problems". In its D.C. part, Test Problem 7 is "Ethylene Glycol - Lauryl Alcohol - Nitromethane -- Gibbs energy minimization (UNIQUAC)" (ex6.2.7.gms).
  - The GAMS file sets:
    - T = 295 K, P = 1 atm, three liquid phases and feed (0.4, 0.1, 0.5);
    - UNIQUAC r = (2.4088, 8.8495, 2.0086) and q = q' = (2.248, 7.372, 1.868);
    - the interaction parameters;
    - bounds 1e-7 ≤ n ≤ ntot.
  - Test Problem 8 (ex6.2.8) is the tangent-plane distance problem for the same system, at a different composition (0.29672, 0.46950, 0.23378).
- Tessier, Brennecke & Stadtherr (2000), Table 10 (preprint p. 28), attribute the same UNIQUAC data to McDonald & Floudas (1995a, AIChE J.). Their feeds differ from (0.4, 0.1, 0.5).
- **The MINLPLib model is the handbook model up to rounding.**
  - The MINLPLib GAMS file equals the GLOBALLib scalar file (GAMS Convert, 2001) up to term order. Equation residuals agree to 1e-39 at 20 random points (`checks/compare_gms.py`).
  - We re-implemented the handbook objective from its GAMS source. It agrees with the MINLPLib objective to ≤ 4.1e-14 relative at 200 random points (`checks/gibbs_source_vs_minlplib.py`).
  - The difference comes from constants rounded to about 15 digits. This rounding also explains the 5e-14 non-cancellation R_p in our scaling analysis.

### 4.2 Prior results
- **Not read**: the handbook (1999), GLOPEQ (1997), McDonald & Floudas (1994, J. Glob. Optim. 5:205–251; GOP and branch and bound for the phase-equilibrium problem) and Floudas (2000, *Deterministic Global Optimization*). Publisher pages were blocked, and no open copy was found. The 1994 paper and the 2000 book are likely primary sources for the Gibbs problems.
  - Indirect evidence that they report our optimum: the handbook GAMS file starts from n.l = (0.00880, 0.33595, 0.05525; 0.00065, 0.00193, 0.09742; 0.30803, 0.14700, 0.04497).
  - This point satisfies the mass balances and lies within 4.3e-4 of our optimal point in every coordinate.
  - Its objective is −0.1608468, which is 8.2e-7 above our certified optimum −0.16084761546 (`checks/handbook_start_points.py`).
  - The start point is most likely the handbook's reported solution, rounded.
- **Status of the McDonald–Floudas methods** (floating-point global):
  - Stadtherr, Xu, Burgos-Solórzano & Haynes (2007, preprint p. 2) describe them as deterministic global optimization (GOP, and branch and bound with convex underestimators). They note that whether α-BB bounds are "rigorously valid bounds depends on the proper choice of a parameter (α)".
  - Tessier et al. (2000) call them methods "which provide a mathematical guarantee of reliability".
  - Neither source treats ex6.2.7 itself. These are ε-global methods in floating point, not outward-rounded certificates.
- **COCONUT, Library 1**: Fbest −0.1608, best point found by BARON 7.2. The .res file gives objective −0.1608476155 and `modelstatus = 2.00` (GAMS: locally optimal, not 1 = optimal). This is a primal value only.
- **Rigorous interval solvers failed**:
  - Ninin (2010), PhD thesis, INP Toulouse, Table 3.1 (p. 63): no IBBA variant solved ex6_2_7 within 1 h at precision 1e-8.
  - Same thesis, Table 3.6 (p. 71): started with the best known value −0.1608, IBBA+CP+rART reached only the lower bound −66.227346367 after 4025.5 s.
  - Ninin, Messine & Hansen (2015, 4OR; preprint 2012, Tables 1 and 3): the same outcome.
  - Trombettoni, Araya, Neveu & Chabert (AAAI 2011), p. 103: "Three systems (ex6_2_5, ex6_2_7 and ex7_2_3) are removed from this table because they are not solved by any solver, including Baron".
    - Precision ε_obj on the cost (Tables 2 and 3 headers): 1e-8 for BARON, GlobSol and IBBA+; 1e-3 for Icos; IbexOpt was run at both 1e-3 and 1e-8.
    - Time limits: 1 h for IBBA+, GlobSol and IbexOpt; 10 min for Icos; 1000 s for BARON 9.0.7 on NEOS.
- **MAiNGO** (floating-point global): Najman, Bongartz & Mitsos (2021), Table 7. ex6_2_7 was not solved within 8 h at tolerance 1e-4 with any of five linearization strategies. The final lower/upper bound ratio was 14.8%–17.8%.
- **BARON "GOpt" label**: Bertsimas & Margaritis (2025, J. Glob. Optim. 91:1–37; read in arXiv:2311.01742v1, saved in `sources/`).
  - What the paper reports: Table 1 (PDF p. 27) lists ex6_2_7 (9 variables) with BARON 2021.01.13 "GOpt" at 1502.2 s. The setup (PDF p. 24) uses a 1500 s limit and records "GOpt" "when the optimality gap is below 0.1%".
  - What the paper leaves open:
    - It does not define the gap. GoML, the method under test, gives no dual bound, so its gap must be measured against a reference value. Whether BARON's gap was measured the same way is not stated.
    - The time of 1502.2 s indicates that BARON stopped at the time limit. It did not terminate with optimality proved within its own tolerances. Its own default tolerance may be tighter than 0.1%, so this does not show that BARON's dual gap exceeded 0.1%. The paper does not report the dual bound.
  - The text (PDF p. 25) counts these instances among the 73 of 77 that "BARON is able to solve … to optimality".
  - **Not a certificate**, and not a stated floating-point global solve. The paper should cite it with this explanation.
- **MINLPLib**: point p1 by CONOPT (2014), objective −0.160847615463598. Open in 2018 and now; the best listed dual is BARON's −1.06726714.
- **Cuesta et al. (2026)**, arXiv:2510.14122v3 (8 Sep 2026), Section 6 (PDF pp. 32–34) and Table 5 (PDF p. 35). Copy in `sources/cuesta_et_al_arxiv2510.14122v3.pdf`.
  - Gurobi 12.0.1, BARON 24.5.8 and COUENNE 0.5.8 directly solved the original MINLPLib models with a 600 s limit and default settings. Equation (32) defines gap (%) as 100·|UB − LB|/|UB|, using the solver's bounds. These are the "MINLP solver" rows, distinct from the MISSOC surrogate results.
  - For ex6_2_7, all three report objective −0.161. Gurobi takes 600.633 s with gap 2400.913%; BARON takes 602.975 s with gap 1359.993%; COUENNE takes 607.277 s with gap 10913.441%.
  - None closes the instance. The authors selected it from the Bertsimas & Margaritis test set because Gurobi could not solve it within 600 s. These runs do not establish what BARON would do with that earlier study's 1500 s limit.
- **Method precedents** (not instance results):
  - the tangent-plane criterion (Baker, Pierce & Luks 1982; Michelsen 1982);
  - its Lagrangian-dual reading (Mitsos & Barton 2007). Mitsos & Barton has NRTL and UNIQUAC case studies but was not read. It cites McDonald & Floudas 1995a, so its UNIQUAC case may be the same ternary system, at an unknown feed.

### 4.3 Consequence
**Partly known.**
- The handbook and GLOPEQ very likely reported the optimal point and value as an ε-global solution in floating point. We could not read either text to confirm the exact claim.
- No rigorous certificate was found. The interval solvers that aim at rigor failed on this instance, and BARON and MAiNGO did not close it either. The 2025 "GOpt" label is not a proof (Section 4.2).
- Our contribution is the first rigorous closure as far as found, not the first solution. The tangent-plane method itself is classical.

## 5. ex6_2_5

**Our claim.** Rigorous dual bound −70.75207783344770759, outward-rounded from the proved −70.7520778334477075803539… (`reviews/closing-confirm-r2.md`, `-r3.md`), gap 2.0e-15. Same method as for ex6_2_7.

### 5.1 Provenance
- **MINLPLib**: "Test Problem ex6.2.5 of Chapter 6 of Floudas e.a. handbook", with the same references. Added 31 Jul 2001.
- **Handbook supplement**: Test Problem 5, "SBA - DSBE - Water -- Gibbs energy minimization (UNIQUAC)", that is, sec-butyl alcohol, di-sec-butyl ether and water (`sources/titan/ex6.2.5.gms`).
  - Phases 1 and 2 are liquids: UNIQUAC with q' ≠ q and Gibbs energies of formation. Phase 3 is an ideal vapour.
  - P = 1.16996 atm; feed (40.30707, 5.14979, 54.54314).
  - The file sets `T = 721.67659` and has `T = 363.19909` commented out. Since 721.67659 = 1.987 × 363.19909, "T" holds R·T in cal/mol (our inference).
  - Test Problem 6 is the tangent-plane distance problem for the same system.
- **The MINLPLib model is the handbook model up to rounding**: it is identical to the GLOBALLib scalar file, and differs from the re-implemented handbook objective by ≤ 9.4e-14 relative at 200 random points.

### 5.2 Prior results
- **Handbook, GLOPEQ, McDonald & Floudas (1994) and Floudas (2000): not read**, as for ex6_2_7.
  - The handbook start point gives the two liquid phases; we set the vapour by mass balance.
  - After swapping the two identical liquid phases, it lies within 3.0e-5 of our optimal point.
  - Its objective is −70.7520778333, 1.0e-10 above our certified optimum.
- Stadtherr et al. (2007) note that McDonald & Floudas also treated the asymmetric case with an excess-Gibbs-energy model for the liquids and an ideal-gas vapour. That is the structure of this problem.
- **COCONUT Library 1**: Fbest −70.7521, found by MINOS (local).
- **Rigorous interval solvers failed**:
  - Ninin (2010), Table 3.1: not solved in 1 h.
  - Same thesis, Table 3.6: with the known value −70.7521 supplied, the lower bound was −7036.008545972 after 4036.4 s.
  - Ninin, Messine & Hansen (2015): same outcome.
  - Trombettoni et al. (2011): quoted in Section 4.2.
- **BARON "GOpt" label**: Bertsimas & Margaritis (2025), Table 1 (arXiv v1, PDF p. 27). ex6_2_5 (9 variables) has BARON 2021.01.13 "GOpt" at 1502.2 s, with a 1500 s limit. Same caveats as in Section 4.2. **Not a certificate.**
- **Cuesta et al. (2026)**, arXiv:2510.14122v3, Table 5 (PDF p. 35), "MINLP solver" rows. The setup is as in Section 4.2: Gurobi 12.0.1, BARON 24.5.8 and COUENNE 0.5.8, a 600 s limit and default settings; gap (%) = 100·|UB − LB|/|UB|.
  - Gurobi reports objective −70.599 in 600.278 s with gap 345.257%; BARON reports −70.752 in 603.024 s with gap 203.848%; COUENNE reports −70.752 in 607.002 s with gap 1386.825%.
  - None closes ex6_2_5. The MISSOC surrogate results in the same table do not certify optimality for the original model.
- **Kosolap (2019)**, "Finding the Global Minimum of the General Quadratic Problems During Deterministic Global Optimization in Cyber-Physical Systems", Advances in Cyber-Physical Systems 4(1), pp. 32–36 per Crossref. Copy in `sources/kosolap/kosolap2019_acps_4-1_32.pdf`.
  - Method: the abstract says the method, "exact quadratic regularization" (EQR), uses "only local search (primal-dual interior point method) and a dichotomy method". Section IV says the test problems come from GLOBALLib.
  - Table 1 is on PDF p. 4, which carries the printed page number 34. Its row reads "Ex6_2_5, n = 10, m = 3, Method EQR −70.9586, The best glob. min. −70.75, Ref. GL". The counts n = 10 and m = 3 match the GLOBALLib model with objvar included and the objective row excluded.
  - −70.9586 lies 0.2065 below our certified lower bound −70.75207783344770759. The MINLPLib model equals the GLOBALLib scalar model (Section 5.1), so no feasible point of that model has this value. **Not attainable** (method: local search; listed by the paper as better than the best known global minimum).
  - 14 of the 15 EQR values in the same table lie below their listed best known global minima. The exception is G16, printed as 1.914608 against −1.9046617, so it lies above. Examples below the listed value: Haverly −406 against −400, Ex2_1_8 15639 against 15990, Ex8_4_7 26.994309 against 28.898. We checked only ex6_2_5 against a certificate.
  - This paper was a hit of our round-1 OpenAlex query "ex6_2_5" but was not read then. The round-2 reviewer read it, and I re-fetched it (same sha256).
- **MINLPLib**: point p1 by CONOPT (2014), −70.752077833445796. Open in 2018 and now; the best listed dual is BARON's −111.4201713.
- Not included in the MAiNGO study of Najman et al. (2021).

### 5.3 Consequence
**Partly known**, for the same reasons as ex6_2_7. The value was very likely reported as an ε-global solution in floating point. No rigorous certificate was found; ours is the first as far as found. The paper may cite Kosolap (2019) among the published values that cannot be attained.

## 6. etamac

**Our claim.** Rigorous dual bound −15.294675643368093, outward-rounded from the proved −15.2946756433680921685… (`reviews/closing-confirm-r2.md`). Gap 2.6e-15 to an exactly feasible point.

Method: a convex relaxation (the production equalities relaxed to ≤, with a concave majorant) and a KKT tangent-plane certificate.

### 6.1 Provenance
- **MINLPLib**: source "GAMS Model Library model etamac". Reference: Manne, "ETA-MACRO: A Model of Energy-Economy Interactions", in Hitch (ed.), *Modeling Energy-Economy Interactions: Five Approaches*, Resources for the Future, 1977. Added 31 Jul 2001.
- **GAMS Model Library page** (`sources/gamslib/gamslib_etamac.html`): "Eta-Macro Energy Model for the USA (ETAMAC, SEQ=80)".
  - It is an NLP that maximizes discounted log consumption, subject to nested CES production rows written as equalities (newprod, ftotalprod).
  - The library also has ETAMGE (SEQ=144), the same model in MPSGE (complementarity) format.
- The MINLPLib scalar model is identical to the GLOBALLib scalar model; residuals agree exactly at 20 random points. We did not compare it with Manne's 1977 text, which we could not obtain.

### 6.2 Prior results
- **Local values**: COCONUT Library 1 gives Fbest −15.2947 from MINOS (.res objective −15.2946756434). MINLPLib point p1 by CONOPT (2014) is −15.29467564, with infeasibility 1e-10.
- **Global solvers, root-node studies only**:
  - Tawarmalani & Sahinidis (2005), Table 1 (p. 242): etamac is problem (8) of the GLOBALLib set used in the root-node cutting-plane study. It is not among the 26 problems solved to global optimality in Table 4 (p. 246).
  - Gleixner, Berthold, Müller & Weltge (2017): etamac is in the root-node OBBT tables (Tables 4 and 6) but not in the tree experiment (Table 8). Table 8 leaves out instances that no setting solved within 1 h, and instances excluded for errors. So SCIP either did not solve etamac or it was excluded.
  - Müller, Serrano & Gleixner (2020, arXiv v2), Table 3: etamac appears only with bilinear-term statistics.
- **MINLPLib**: open in 2018 (best dual: ANTIGONE −15.835) and now (SCIP −15.40567054).
- **The convexity argument** we used is standard economics:
  - a CES function with negative exponent is concave and increasing;
  - log utility is concave and increasing;
  - so the equalities can be relaxed to ≤.

  We found no source that states this for etamac or derives a global bound from it.

### 6.3 Consequence
**New as far as found.** No global optimality claim was found, and no valid dual bound close to the optimum.
- The local value has long been known (MINOS, CONOPT), and the hidden convexity is classical in spirit; the paper should say so.
- The contribution is the certificate. It includes the concave majorant that handles the degree excess of 4e-16 coming from the file's exact decimals.

## 7. pricing050

**Our claim (maximization).** Rigorous upper bound −1813.8290784519730577 (verifier), with gap 1.0e-17 to an exactly feasible point. Method: a Lagrangian over the 5 rows, with certified one-dimensional minimizations. In min form: min Σ c_j x_j ≥ 1813.8290784519730577.

### 7.1 Provenance
- **MINLPLib page**: "A firm seeks to determine the price of several new products to enter a competitive market".
  - Source: "Mohammadreza Kiaghadi". References: Davarnia (2021, Oper. Res. Lett.) and Davarnia & van Hoeve (2021, Math. Program.). Added 25 Mar 2024.
  - The April 2024 snapshot lists no points and no bounds.
  - Point p1: "found by KNITRO and contributed by Çağrı Latifoğlu" (26 Aug 2024).
- **Davarnia & van Hoeve** (read in the preprint, optimization-online 6512, Section 6.2, pp. 17–18; the journal version was not read):
  - Integer pricing model: min Σ c_i x_i s.t. Σ_i a_i^j x_i e^(−x_i^(k_i^j)) ≥ b_j, with x_i ∈ {0, …, 10} and a "scaling factor 10, i.e., the prices are chosen among {0, 0.1, …, 1.0}".
  - Data: c ∈ u.d.d.[0, 20], a ∈ u.d.d.[0, 100], b ∈ u.d.d.[10n, 20n], k ∈ {1, 2, 3}, |J| = 5, five random instances per size.
  - The MINLPLib description sentence is taken from this section.
- **Davarnia (2021, ORL)** (read in the preprint, optimization-online 7681, pp. 15–18; the journal version was not read):
  - It uses the continuous version on the "benchmark problem instances studied in [9]", that is, Davarnia & van Hoeve.
  - Its formulation (9) is printed on preprint p. 15 as min Σ c_i x_i s.t. Σ_i a_ji x_i e^(−x_i^(k_ij)) ≥ b_j, x ∈ [l, u] (9c). The bounds [l, u] = [0, 10] are stated on p. 16. This is without the 1/10 price scaling that Davarnia & van Hoeve and pricing050 use.
- **pricing050's data fit the scaled generator**:
  - integer c in [0, 20];
  - a = integer/10;
  - demand exp(−(x/10)^k) with k ∈ {1, 2, 3};
  - right-hand sides in [500, 1000] = [10n, 20n];
  - x ∈ [0, 10].
- **Which instance?**
  - We solved the integer version of pricing050 (x ∈ {0, …, 10}) exactly as a MILP, with one binary per (product, value). This used HiGHS in floating point (`checks/pricing050_integer_version.py`).
  - Its optimum is 1825.0.
  - Davarnia & van Hoeve, Table 6.1 (preprint p. 20), report the integer-version primal values 1592, **1825**, 1891, 2403 and 1800 for their five n = 50 instances.
  - So pricing050 is very likely the continuous version of their n = 50 instance #2. This is numerical evidence, not proof.

### 7.2 Prior results
Both tables below were read in the optimization-online preprints, not in the published journal versions.
- **Davarnia & van Hoeve (2021), Table 6.1**, n = 50, #2 (integer version, 300 s; preprint p. 20). These bound the integer problem, not pricing050.
  - UB 1825, decision-diagram (DD) bound 1786.3.
  - Solver bounds: ANTIGONE 1063.3, BARON 1299.0, COUENNE 1452.5, SCIP 1367.2.
- **Davarnia (2021, ORL), Table 1**, n = 50, #2 (continuous version, 300 s; preprint p. 18):
  - UB 1813.3, DD bound 1663.7.
  - Solver bounds: ANTIGONE 1037.4, BARON 1354.2, COUENNE 1437.6, SCIP 1368.3.
  - "UB" is "the best primal bound obtained across all solvers within the time limit".
- **Inconsistency.** If this is the same instance, 1813.3 lies 0.53 below our certified minimum 1813.8290784519… (2.9e-4 relative). So no feasible point has that value.
  - With our multipliers (3.05 and 2.17 on two rows), a point would need row violations of about 0.1 to gain 0.53. Normal solver tolerances do not allow that.
  - Other explanations are possible:
    - a transcription error in the table;
    - different data;
    - runs on the unscaled formula (9) as printed, which would be a different instance.

    The UB 1813.3 sits next to the integer value 1825, which suggests that the scaled model was run. This cannot be settled without the authors' data.
- **Davarnia, Kiaghadi & Qiu** (2026, J. Glob. Optim.; preprint optimization-online 2024/09) present a decision-diagram global solver tested on MINLPLib instances. pricing050 is not among them.
- **MINLPLib**: open; best listed dual SCIP −1534.3281 (max form).

### 7.3 Consequence
**New as far as found.** No global solution or close dual bound was found.
- The best published dual bound for this instance at n = 50 is the DD bound 1663.7 (min form), 8% below the optimum.
- The paper may mention the ORL value as an inconsistency, with two caveats: the instance identity rests on our MILP evidence, and the table was read in the preprint.

## 8. pindyck

**Our claim.** Rigorous dual bound −1170.4862854360886163932, gap ≤ 5.44e-14. Method: the reduced objective is proved concave on a polytope that contains the feasible set, then a tangent-plane bound is applied. Verified by an independent rebuild.

### 8.1 Provenance
- **MINLPLib**: source "GAMS Model Library model pindyck". Reference: Pindyck, "Gains to Producers from the Cartelization of Exhaustible Resources", Rev. Econ. Stat. 60(2) (1978) 238–251. Added 31 Jul 2001.
- **GAMS Model Library page** (`sources/gamslib/gamslib_pindyck.html`): "Optimal Pricing and Extraction for OPEC (PINDYCK, SEQ=28)". Supply equation: s(t) = 0.75 s(t−1) + (1.1 + 0.1 p(t)) · 1.02**(−cs(t)/7).
- The MINLPLib scalar model is identical to the GLOBALLib scalar model: residuals agree exactly, and x51 = cs_0 is fixed at 0 in both. Not compared with Pindyck's paper.

### 8.2 Prior results
- **COCONUT Library 1**: Fbest −1612.1783, "obtained by solver MINOS". This is **not** a value of the MINLPLib model.
  - The COCONUT GAMS file (written by a dag2gams converter in 2004) uses exp((−0.01980262729617973) · cs), which is 1.02^(−cs). The factor 1/7 is lost.
  - Re-running the recursion at COCONUT's prices with exponent factor 1 reproduces J = 1612.17830322903.
  - With the correct factor 1/7, the same prices give J = 1057.218 and a negative OPEC demand (`checks/coconut_pindyck.py`).
  - The COCONUT AMPL file itself has the correct exponent; MINOS's point fits the GAMS/DAG version.
- **Tawarmalani & Sahinidis (2005), Table 1**: pindyck is problem (28) of the root-node study. It is not among the 26 problems solved in Table 4.
- **Gleixner et al. (2017)**: root-node tables only (Tables 4 and 6); absent from the tree experiment (Table 8).
- **Müller, Serrano & Gleixner (2020, SIAM J. Optim.; arXiv v2)**:
  - Table 4: root dual bound −2239.98 with their bilinear separation, −3972.57 without (reference primal −1170.49).
  - Table 5: all three settings hit the 1800 s limit (233.6K–265.6K nodes).
- **Smith (2011)** removed pindyck from his test set because of AMPL interface errors.
- **MINLPLib**: point p1 by CONOPT (2014), −1170.486285. Open in 2018 and now; best dual SCIP −1437.941134.

### 8.3 Consequence
**New as far as found.** The SCIP studies report the instance unsolved, and the only published value below the optimum belongs to a mistranslated model.

## 9. eg_int_s

**Our claim.** Rigorous dual bound 6.4531031529331155, exactly feasible point 6.4531031593842275 (gap 1.0e-9 relative). Verified: all leaves were re-certified independently.

### 9.1 Provenance (all three eg_* instances)
- **MINLPLib**: source "Bram Schoonen's Model Collection", added 25 Jul 2002, no reference. We found no paper or report that describes this collection or where the models come from.
- **Point histories** (MINLPLib point pages):
  - eg_disc_s.p1 and eg_disc2_s.p1 were found by SBB with CONOPT3 (25 Jul 2002).
  - eg_int_s.p1 was found by LaGO with CONOPT3 (11 Jan 2007).
  - **The old MINLPLib point file for eg_int_s** (GAMS World archive, `sources/gamsworld/MINLPLib_points_eg_int_s.inc`) has objvar.L = 6.4531031527. This is 2.3e-10 *below* our certified lower bound 6.4531031529331155. It is not the value of a feasible point:
    - At its x, row e12 is violated by 6.3678e-9. This was proved in outward-rounded interval arithmetic on the current MINLPLib `.mod` rows (`checks/eg_int_s_oldpoint.py`, log `checks/logs/eg_int_s_oldpoint.log`); the round-2 reviewer found the same on the OSIL.
    - All other rows, the bounds and integrality hold.
    - At that x, rows e1–e24 need objvar ≥ 6.4531031591.

    So the value is a tolerance artifact and should not be quoted as a solution value.
- **Row count**:
  - The GAMS World archive copy of eg_int_s has the same 28 rows as today's file (`checks/logs/compare_eg_int_s_current_vs_gamsworld.log`).
  - But its header ("GAMS Convert at 08/22/01", 26 equations, 206 nonzeros) and the old MINLPLib table (26 rows) suggest that two rows were added after August 2001.
  - The COIN-OR GAMSlinks MINLP benchmark logs of 2 Sep 2008 show the current size for all three eg_* models: "28 rows 8 columns 220 non-zeroes" and 196 nl-non-zeroes (BONMIN logs in `sources/coinor_2008/BONMIN-1_eg_*.log`). So the two rows were added between August 2001 and September 2008. Why is unknown.
  - The saved BARON and LindoGlobal trace records (`sources/coinor_2008/BARON-2.trc.canall` and `LINDOGLOBAL-1.trc.canall`) list 28 equations, 8 variables, 220 nonzeros and 196 nonlinear nonzeros for each of the three eg_* instances. This confirms the current model size for both solvers; the full logs are not online (HTTP 404 at the analogous URLs). Size alone does not prove that every coefficient is identical.
  - Our claims concern the current OSIL model.

### 9.2 Prior results
- **Göß, Burlacu & Martin (2026), J. Glob. Optim. 94:951–996**, Appendix B.5, Table 17 (p. 988; Table 15 in arXiv v2):
  - Table 17 was read in the arXiv v2 text and confirmed in an archived copy of the published PDF (`sources/eg/goss_jogo_2026_archive.pdf`, PDF p. 38).
  - Setup (Section 4.2): SCIP 8.1 and Gurobi 11.0.1, run through GAMS 46.4.0, with 8 threads, a 4 h limit and a 60 GB memory limit. "If not stated otherwise, default settings are used."
  - eg_int_s, SCIP, original model: run time 9085.1 s, "primal value 6.5, dual value 6.5". That is, solved (floating-point global).
  - **Gap tolerance.** The paper does not state it, but it can be pinned down with one caveat:
    - The GAMS 32 release notes (July 2020; `sources/gams/RN_32.html`) list optCR among the "new default values": 0.0001, previously 0.1.
    - The authors' public code (github.com/adriangoess/paraboloids, fetched 2026-10-02) writes GAMS files without any optCR statement. An example is `sources/eg/paraboloids_repo/batchdes_orig.gms`. The time and thread limits must have been set outside those files.
    - The repository's README (line 38) says the written files are included "except the `eg_...` ones due to their size". So the absence of optCR is observed only on the other instances' files and inferred for eg_*.
    - The repository's option files set no gap either. `para_relaxation/instances/scip.opt` contains only `limits/memory=61440`, which is 60 GB and matches the paper's memory limit. `gurobi.opt` contains only `nonconvex=2` and `memlimit=60`. Copies are in `sources/eg/paraboloids_repo/`.
    - So "solved" very likely means GAMS's relative gap ≤ 1e-4, unless optCR was overridden on the command line.
  - Gurobi reached the time limit on the original model.
  - **Publisher correction.** Crossref lists "Publisher Correction: Parabolic approximation & relaxation for MINLP", J. Glob. Optim. 95(4) (2026) 1095–1141, doi:10.1007/s10898-026-01614-9. It has 47 pages, so it apparently republishes the article; the original Crossref record spells the first author "Göss". **Not read**:
    - Springer served a bot page (also to the round-2 reviewer);
    - the Internet Archive has no copy;
    - arXiv has no version after v2 (21 Mar 2025);
    - the TRR154 repository has only the preprint record.

    Before the paper relies on Table 17, someone should check that the correction did not change it.
- **2008 COIN-OR/GAMSlinks MINLP benchmark** (1 h runs; `sources/coinor_2008/`):
  - BARON 8.1.5: primal 6.45310315899, bound −8.0807.
  - LindoGlobal 5.0: primal 7.4631, bound −3.1577.
- **CAMINO: Ghezzi, Van Roy, Sager & Diehl** (Math. Program. Comput. 2026). Read in arXiv:2404.11786v2 (26 Mar 2026) and in the public data repository CAMINO-benchmark (github.com/minlp-toolbox/CAMINO-benchmark). The results were last changed in commit 66a134daf8 (19 Mar 2026). Copies are in `sources/eg/camino_benchmark/`; my downloads have the same sha256 as the round-2 reviewer's.
  - **Setup** (Section 4.1, PDF p. 26):
    - Bonmin 1.8, SHOT 1.1 and the authors' S-B-MIQP and S-B-MIQP-ee have a 300 s limit.
    - SCIP 9.2.2 and Gurobi 13.0.0 "are called using the AMPL Python interface which loads the MINLPLib as .mod file".
    - "The MINLP gap for termination is set to 10−2", and primal solutions satisfy a tolerance of 1e-8.
  - **Nonconvex instances** (PDF pp. 28–29):
    - "all algorithms except SCIP and Gurobi are only heuristics".
    - The time limit of SCIP and Gurobi on each instance equals the S-B-MIQP time on that instance, or 300 s if S-B-MIQP failed.
    - The Table 3 caption reads: "For SCIP and Gurobi 'success' correspond to a global optimal solution".
    - The abstract says that "for nonconvex problems, the algorithm functions as a heuristic without global optimality guarantees". This refers to the authors' own method.
  - **Table 8** (caption PDF p. 49, eg rows PDF p. 51) prints objective values and wall times only. For eg_int_s: Bonmin 7.89 (32.7 s), Gurobi 11.7 (70.8 s), SCIP 7.46 (213 s), SHOT 8.39 (300 s), S-B-MIQP 7.89 (213 s), S-B-MIQP-ee 8.03 (300 s).
  - **Gurobi's optimality claim is wrong.**
    - Data: the driver `benchmark/using_amplpy.py` runs Gurobi with `bestbound=1 feastol=1e-8 mipgap=1e-2 threads=1 timelimit=<S-B-MIQP time>`. It records the objective and `obj.bestbound` when AMPL's `solve_result` is "solved" or "limit". The bound column holds Gurobi's own bound: on 59 other instances that stopped early, it is a real finite value different from the objective. Two more, eg_all_s and hadamard_9, report only the 1e100 placeholder for no bound (stored as its decimal floating-point representation). Here "early" means time < 0.99 × the per-instance limit.
    - Result: for eg_int_s, `results/26_03_10_results/noncvx_gurobi.csv` gives objective 11.65415903480683 and best bound 11.65415903480683 after 70.80 s. The per-instance limit was 212.66 s (`benchmark/wall_time_noncvx_sbmiqp.json`). A best bound equal to the objective, reported before the time limit, is Gurobi's claim that its point is globally optimal. By the Table 3 caption, this is also a "global optimal solution".
    - Proof that the claim is wrong: `checks/eg_camino_gurobi.py` evaluates every row, bound and integrality condition of the MINLPLib `eg_int_s.mod` at the project's recorded point (`open-instances-wave3/eg/retry/sol/eg_int_s.retry.sol`), in outward-rounded interval arithmetic (mpmath `iv`, 200 bits). All 28 rows hold on the enclosure; the smallest proved slack is 5.6e-20. So that point is feasible for the .mod model, with objective 6.4531031593842274088, and Gurobi's claimed bound exceeds the optimum by at least 5.201056 (81%).
    - Assumptions: mpmath's interval arithmetic, including `exp`, is outward-rounded; my parser reads the .mod rows correctly (row and variable counts match the file header); CAMINO's local copy of the .mod file (path `/workspace/local-home/ghezzi/minlplib_mod/`) is the current MINLPLib file, whose header reads "GAMS Convert at 01/12/18". The round-2 reviewer found the .mod rows numerically identical to the OSIL rows.
    - The csv does not record Gurobi's termination status. The optimality claim is inferred from bound = objective and the early stop.
    - The cause of the wrong claim is unknown. We did not rerun Gurobi 13.0.0 through AMPL.
  - **SCIP 9.2.2** in the same data stopped at its limit (213.17 s) with objective 7.4631 and bound −4.2643. The bound is valid.
  - **How the paper counts "success".** The authors' counting script (`benchmark/create_plot.py`, lines 630–658) counts a SCIP or Gurobi run as a "success" whenever its objective is finite and nonzero and its time is below 300 s. It does not look at the bound. So Table 3's success counts also include runs that stopped at a per-instance limit below 300 s, such as SCIP's runs on all three eg_* instances. The caption's "global optimal solution" therefore does not hold for every counted success. The Gurobi claims above rest on Gurobi's own reported bound, not on Table 3.
  - The published version and its correction (doi:10.1007/s12532-026-00337-y) were not read.
- **Primal-only results**:
  - Cristofari, Di Pillo, Liuzzi & Lucidi (2026, JOTA 209:38), Table 1 (p. 16): best known value 6.4531.
  - D'Ambrosio, Frangioni, Liberti & Lodi (2012, "A storm of feasibility pumps"), tables reprinted in D'Ambrosio's habilitation thesis: feasibility-pump runs only.
- **Blomqvist (2025, MSc thesis, Åbo Akademi, SHOT)** lists the eg_* instances in its test set (Appendix A) but reports only aggregate results.
- **MINLPLib**: best dual −1.21 (LINDO, −1.20527282) in 2018; now 6.32629896 (SCIP).

### 9.3 Consequence
**Already solved globally in floating point** (Göß et al., SCIP 8.1).
- As far as found, ours is the first rigorous certificate, to 1e-9 relative, with an exactly feasible point.
- The paper must cite Göß et al. (and the publisher correction) and must not claim to be the first to solve it.
- The wrong Gurobi 13.0.0 claim in the CAMINO data does not change this label. The paper may cite it as an example of an incorrect floating-point optimality claim (Section 12, item 7).

## 10. eg_disc_s

**Our claim.** Rigorous dual bound 5.760539610694994, exactly feasible point 5.7605396164535107 (1.0e-9 relative). Verified.

### 10.1 Prior results
- **Göß et al. (2026), Table 17** (arXiv v2 and the archived published PDF):
  - SCIP on the original model reached the 4 h limit with the values 3.6 | 5.8.
  - The column headers read "primal value | dual value", but only the reverse reading fits a minimization problem with optimum 5.7605 (as our retry note found). So the dual bound is 3.6.
  - This SCIP entry carries an asterisk: the instance "caused numerical and/or memory errors" with SCIP and was excluded from the SCIP evaluation.
  - Gurobi, original model: time limit, 2.0 | 7.5.
- **2008 COIN-OR benchmark**:
  - BARON: primal 5.76053961645, bound −8.0807.
  - LindoGlobal: primal 5.76053961646, bound −7.3125.
- **Cristofari et al. (2026), Table 1**: best known value 5.7605 (primal only).
- **CAMINO (arXiv v2, Table 8, and the public data; setup and caveats in Section 9.2)**:
  - Table 8: Bonmin 5.76 (33.6 s), Gurobi 6.19 (0.991 s), SCIP 7.96 (19.6 s), SHOT 6.41 (75.8 s), S-B-MIQP 5.76 (19.2 s), S-B-MIQP-ee 5.76 (8.97 s).
  - **Gurobi 13.0.0: wrong optimality claim.**
    - Data: objective = best bound = 6.191829847658548 after 0.99 s, against a limit of 19.24 s.
    - Our recorded point is proved feasible for the MINLPLib `eg_disc_s.mod` (interval arithmetic; smallest slack 7.8e-20), with objective 5.7605396164535106058.
    - So the claimed bound exceeds the optimum by at least 0.431290 (7.5%).
  - SCIP 9.2.2 stopped at its limit (19.58 s) with bound −6.7350, which is valid.
- **MINLPLib**: best dual −4.02 (LINDO) in 2018; now 3.36596129 (SCIP).

### 10.2 Consequence
**New as far as found.** The best published valid dual bound is 3.6 (SCIP, with errors reported). The best MINLPLib bound is 3.366. The only published optimality claim, by Gurobi 13.0.0 in the CAMINO data, is wrong.

## 11. eg_disc2_s

**Our claim.** Rigorous dual bound 5.642100574331458, exactly feasible point 5.6421005799711068 (1.0e-9 relative).
- Verified on all 1,114,361 leaves of run G, with zero failures, under the earlier review certifier's assumptions A1/A2; 1,152,830 counts processed boxes. [The all-leaf track](../../eg-recheck/report.md) and [review r1](../../reviews/eg-recheck-review-r1.md) give an exact coverage proof and a separate outward-rounded interval certification of 10,404 leaves of parts 0 and 2–7 (including the 300 tightest per part), without a libm assumption.
- The earlier 110,676-of-979,044-leaf sample outside part 1 is historical; it has been superseded by the all-leaf recheck under A1/A2.

### 11.1 Prior results
- **Göß et al. (2026), Table 17**:
  - SCIP, original model: time limit, −1.1 | 6.3. The dual is −1.1 under the reverse reading.
  - Gurobi: time limit, −5.2 | 7.0.
- **2008 COIN-OR benchmark**:
  - BARON: primal 5.93701554196 (not optimal), bound −8.0807.
  - LindoGlobal: primal 5.64210057997, bound −9.9793.
- **Cristofari et al. (2026), Table 1**: best known value 5.6421.
- **CAMINO (arXiv v2, Table 8, and the public data; setup and caveats in Section 9.2)**:
  - Table 8: Bonmin 5.64 (56 s), Gurobi 5.89 (2.15 s), SCIP 6.71 (33 s), SHOT 5.67 (300 s), S-B-MIQP 5.64 (32.6 s), S-B-MIQP-ee 5.64 (22.2 s).
  - **Gurobi 13.0.0: wrong optimality claim.**
    - Data: objective = best bound = 5.88669499573929 after 2.15 s, against a limit of 32.63 s.
    - Our recorded point is proved feasible for the MINLPLib `eg_disc2_s.mod` (interval arithmetic; smallest slack 7.5e-20), with objective 5.6421005799711067563.
    - So the claimed bound exceeds the optimum by at least 0.244594 (4.3%).
  - SCIP 9.2.2 stopped at its limit (32.99 s) with bound −5.8305, which is valid.
  - **S-B-MIQP value below our bound.** The combined data file (`results/26_03_10_results/noncvx.csv`) gives the same objective, 5.642100351878204, for S-B-MIQP and S-B-MIQP-ee. That is 2.2e-7 below our certified lower bound, so it is not the value of an exactly feasible point. These methods are heuristics with a stated tolerance of 1e-8. The paper prints the value as 5.64.
- **MINLPLib**: best dual −7.57 (LINDO) in 2018; now 0 (SHOT).

### 11.2 Consequence
**New as far as found.** No published valid dual bound above 0 was found. The only published optimality claim, by Gurobi 13.0.0 in the CAMINO data, is wrong. Every leaf is certified under A1/A2; 10,404 leaves are also certified without the libm assumption.

## 12. Side findings for the paper

1. **COCONUT pindyck value.**
   - The COCONUT benchmark lists Fbest = −1612.1783 for pindyck, below the certified optimum −1170.486.
   - Its GAMS translation has 1.02^(−cs) instead of 1.02^(−cs/7). The listed point reproduces −1612.17830322903 exactly under that change (`checks/logs/coconut_pindyck.log`).
   - A paper that cites COCONUT best values should not use this one.
2. **Pricing value in Davarnia (2021).**
   - Our MILP evidence links pricing050 to the n = 50 instance #2: its integer version has optimum 1825, the value reported for #2.
   - If that link holds, the continuous primal value 1813.3 in Table 1 of Davarnia (2021) cannot be attained. We read the table in the optimization-online preprint 7681, not in the ORL article.
   - The formula (9) printed there lacks the 1/10 price scaling. This is a second possible source of the discrepancy, next to a transcription error or different data.
   - Asking the authors would settle this; we did not contact anyone.
3. **HVYCRASH SIF bounds.**
   - In HVYCRASH.SIF, the XX cards that fix X(3,0) and X(3,N) at 0 have no effect: the later loop sets X(3,T) ∈ [0, 2π] for every T = 0..N, and SIFDecode lets later bound cards overwrite earlier ones. The same holds for the 2013 version.
   - The decoded problem at N = 50 is exactly MINLPLib's hvycrash, up to the elimination of fixed and unused variables. Its objective is constant at −0.2185 on the feasible set, for every N.
   - Whether the SIF author meant to fix θ_0 and θ_N is unknown. Had θ_N been fixed at 0, row C(2,N) would have no real solution.
4. **hvycrash values that are not feasible.** These cannot come from feasible points: −0.0481 (COCONUT), −1.905155235 (Smith 2011), the SIF's SOLTN(100)/(500)/(1000), and the local-solver objectives in Omheni (2014).
5. **Handbook start points.**
   - The handbook GAMS files for ex6.2.5 and ex6.2.7 start next to our optimal points (Sections 4.2 and 5.2). This is the best evidence available that the handbook reports these optima.
   - Someone should check the book text before the paper says more than "very likely".
6. **BARON "GOpt" on ex6_2_5 and ex6_2_7** (Bertsimas & Margaritis 2025).
   - The label means a gap below 0.1% of undefined type, after a run that hit the 1500 s time limit.
   - The paper should cite this result and explain that it is not a global optimality proof.
7. **Gurobi 13.0.0: wrong optimality claims on eg_disc2_s, eg_disc_s and eg_int_s** (CAMINO public benchmark data, 2026; Sections 9.2, 10.1 and 11.1).
   - Gurobi 13.0.0, run through the AMPL Python interface on the MINLPLib .mod files, stopped long before its per-instance time limits: after 2.15 s, 0.99 s and 70.80 s, against 32.63 s, 19.24 s and 212.66 s. Each time, the reported best bound equaled the objective: 5.88669499573929, 6.191829847658548 and 11.65415903480683.
   - We proved in outward-rounded interval arithmetic that the project's recorded points are feasible for the same .mod models, with objectives 5.64210057997, 5.76053961645 and 6.45310315938 (`checks/eg_camino_gurobi.py`). So the claimed bounds exceed the optima by at least 0.2446, 0.4313 and 5.2011 (4.3%, 7.5% and 81%). This is far beyond the run's 1% gap tolerance.
   - The paper prints only the objective values and times (Table 8). Its Table 3 caption calls a SCIP or Gurobi "success" a global optimal solution. The bounds are in the public data.
   - The cause is unknown. For a paper about rigorous certificates, this is a strong example: a current commercial global solver reported wrong optimal values on three of our instances.
   - Two caveats:
     - the data do not record Gurobi's termination status;
     - the counting script behind Table 3 does not check bounds (Section 9.2).
8. **Kosolap (2019), ex6_2_5.** Table 1 reports −70.9586 (method EQR, built on local interior-point search) against a "best known glob. min." of −70.75. The value is 0.2065 below our certified lower bound, so it cannot be attained by a feasible point of the GLOBALLib/MINLPLib model. 14 of the table's 15 EQR values lie below their listed best known values; G16 is printed as 1.914608 against −1.9046617 and lies above.
9. **Tolerance-level values below eg_\* certified bounds.**
   - The old GAMS World point of eg_int_s (objvar 6.4531031527) violates row e12 by 6.4e-9.
   - S-B-MIQP's eg_disc2_s value in the CAMINO data (5.642100351878204) is 2.2e-7 below the certified bound.

   These matter only if the paper lists every published value.

## 13. What could not be read, and other limits

- **Not read**:
  - the Floudas et al. handbook (1999) text;
  - McDonald & Floudas (1994, J. Glob. Optim. 5:205–251) and McDonald & Floudas (1995a, 1995b, 1995c, 1997);
  - Floudas, *Deterministic Global Optimization* (2000);
  - Mitsos & Barton (2007);
  - Manne (1977), Pindyck (1978) and Tyatushkin et al. (1992);
  - the publisher correction of Göß et al. (J. Glob. Optim. 95(4), 2026);
  - Prudente (2012, Unicamp thesis): repository HTTP 503;
  - the published versions of the Davarnia (2021) ORL article and the Davarnia & van Hoeve (2021) MP article (the preprints were read);
  - the published CAMINO article (MPC 2026) and its correction (arXiv v2 and the public data were read);
  - the published Bertsimas & Margaritis article (arXiv v1 was read);
  - the 2001 OQGRG report, a hit for ex6_2_*, a local multistart method;
  - the BARON and LindoGlobal logs of the 2008 COIN-OR benchmark (HTTP 404).

  Reasons:
  - Springer, Elsevier and Wiley pages returned bot challenges or 403.
  - The Google Books quota was exhausted.
  - The UT repository returned 403.
  - FreiDok returned 404.
  - The Unicamp repository returned 503.
  - No open copy was found by WebSearch.
- **Services that failed**: Semantic Scholar snippet search (HTTP 429, repeated), CORE (429), DuckDuckGo (rate-limited after one query), arXiv API (503), Unpaywall (request rejected). The Internet Archive was offline at first and worked later.
- **Search coverage**:
  - OpenAlex full-text search covers only part of the literature, and WebSearch indexed the instance names poorly.
  - The round-3 reviewer found Cuesta et al., arXiv:2510.14122v3, through WebSearch after OpenAlex searches missed it. I checked the saved PDF and added its ex6_2_5 and ex6_2_7 runs. Recent arXiv preprints can be missed by OpenAlex searches.
  - Papers that report per-instance results only in supplementary files or data repositories may have been missed (for example BARON, ANTIGONE or Octeract benchmark papers). The CAMINO case shows that data repositories can hold results the paper does not print. The Octeract claims we found concern other instances (transswitch).
  - One OpenAlex hit (Kosolap 2019) was not followed up in the first version. Other hit lists were read in full, but this shows that a hit can be overlooked.
- **Model identity** was checked numerically at random points, not proved.
  - For hvycrash, the bounds were compared by code. The rows were compared by inspection (this track) and numerically by the round-2 reviewer (maximum difference 2.1e-48).
  - The instance identity of pricing050 rests on one floating-point MILP solve.
  - For the CAMINO eg_* runs, we assume that CAMINO's local .mod copies equal the current MINLPLib .mod files.

## 14. Commands and queries actually run

All runs were single-process and short (seconds to about 2 minutes), from `research-20260929/publication/literature/small/` unless stated otherwise. No project-wide checks were run, no CI was inspected, nothing was committed and nothing was posted. No background jobs were started.

### 14.1 First version (2026-10-01)

**Checks written for this track (numerical evidence):**
- `python3 checks/compare_gms.py sources/minlplib_gms/<n>.gms sources/gamsworld/GlobalLib_scalar_models_<n>.gms 20`, for n = ex6_2_5, ex6_2_7, etamac, pindyck. Result: same equations, variables and bounds; residuals agree to ≤ 2.4e-39 (term order only) or exactly.
- `python3 checks/compare_gms.py sources/minlplib_gms/eg_int_s.gms sources/gamsworld/MINLPLib_Scalar_models_eg_int_s.gms 5`. Result: identical.
- `python3 checks/gibbs_source_vs_minlplib.py`. Result: maximum relative objective difference between handbook and MINLPLib models, 4.13e-14 (ex6_2_7) and 9.37e-14 (ex6_2_5).
- `python3 checks/handbook_start_points.py`. Result: objectives at the handbook start points are −0.160846800 (ex6_2_7) and −70.7520778333 (ex6_2_5); distances to our optimal points are 4.3e-4 and 3.0e-5.
- `OMP_NUM_THREADS=1 python3 checks/pricing050_integer_version.py`. Result: the integer version of pricing050 has MILP optimum 1825.0 (HiGHS, gap 0).
- `python3 checks/coconut_pindyck.py`. Result: COCONUT's prices give J = 1612.17830322903 with exponent factor 1, and J = 1057.218 (min d_t = −0.87) with the correct factor 1/7.

Notes on these runs:
- The first two runs of `pricing050_integer_version.py` parsed too few row terms and reported "Infeasible". The final version evaluates the rows with the generic evaluator.
- `compare_gms.py` was edited once so that it accepts spaces in `sqr (`.
- One ad hoc inline Python run did the first pindyck recomputation. It is superseded by `coconut_pindyck.py`.

**Fetches** (curl, sequential, about 1 s apart). Every saved file is listed with its URL and sha256 in `sources/manifest.tsv`. For seven large, marginal PDFs only text extracts were kept; their PDF sha256 values are recorded in the manifest.

Fetches that failed or were discarded:
- Springer chapter and article pages (bot challenge).
- ScienceDirect GLOPEQ page (403).
- HAL direct downloads (bot challenge); Internet Archive copies were used instead.
- Google Books API (429) and HTML search (JavaScript only).
- CORE (429); Semantic Scholar snippet search (429, three attempts); Unpaywall (rejected); arXiv API (503).
- FreiDok CAMINO PDF (404); UT repository OQGRG (403).
- Mittelmann's benchmark pages: fetched; none of the target instances is in the instance list.
- GAMS presentations (present_ifors2008_global, present_global, present_globalSB): fetched; no mention of the target instances.
- Brazilian J. Chem. Eng. 2006 and InTech 2011 Gibbs papers: fetched; the target systems are absent; deleted.
- MINLPLib2 2015 archive URLs: 404.
- titan chapter 6 and index pages: needed several Internet Archive retries.

**API queries.**
- Crossref: about 20 bibliographic look-ups.
- Semantic Scholar paper API: 3 DOIs.
- OpenAlex full-text search, 22 queries:
  - single names: hvycrash, etamac, pindyck, eg_int_s, ex6_2_5, ex6_2_7, pricing050, eg_disc2_s, eg_disc_s, eg_all_s, GLOPEQ;
  - name pairs: "pindyck minlplib", "pindyck globallib", "etamac globallib", "etamac minlplib", "etamac gams", "hvycrash minlplib", "ex6_2_7 minlplib", "pricing050 minlplib", "Kiaghadi pricing";
  - Gibbs systems: "lauryl alcohol nitromethane ethylene glycol UNIQUAC", "di-sec-butyl ether sec-butyl alcohol water Gibbs".

**WebSearch queries:**
- the handbook's chapter 6 on Gibbs/UNIQUAC (2 variants);
- "ex6_2_5" OR "ex6_2_7";
- HVYCRASH.SIF; "hvycrash" test problem;
- McDonald Floudas GLOPEQ; handbook biconvex UNIQUAC three phases (extended mode);
- the ex6_2_5 feed numbers ("54.54314" OR "40.30707" OR "5.14979"); UNIQUAC "6.0909" "5.168";
- Mitsos–Barton dual extremum principle;
- Davarnia–van Hoeve outer approximation PDF; Kiaghadi dissertation;
- "Schoonen" MINLPLib eg_*; "eg_int_s" MINLP;
- Octeract open MINLPLib instances; "pindyck" globallib BARON; "etamac" GAMS global;
- ethylene glycol lauryl alcohol nitromethane feed; SBA DSBE water Gibbs UNIQUAC;
- Manne ETA-MACRO concave (2 variants);
- Trombettoni et al. AAAI 2011; Ninin–Messine–Hansen 4OR.

**WebFetch**: the Springer chapter (redirect), ScienceDirect GLOPEQ (403), yoric.mit.edu (Mitsos–Barton abstract), the HAL Ninin thesis (bot page).

**DuckDuckGo**: three queries through curl. One returned the COCONUT and SIF-mirror leads; then the service rate-limited.

**Local**: grep over `literature/papers/*/fulltext.md` for all nine instance names and for ETA-MACRO, GLOPEQ, UNIQUAC, Gibbs and Schoonen; pdftotext on the fetched PDFs; GAMS 54.3 `optgams.def` read for the default OptCR.

### 14.2 Revision after review round 1 (2026-10-02)

**hvycrash**
- `sed -n` of the BOUNDS, ELEMENT USES, GROUP USES, OBJECT BOUND and ELEMENTS sections of `sources/hvycrash/HVYCRASH.SIF`.
- `diff` of the BOUNDS sections of the 2013 and 2026 versions: identical. `diff` of the whole files: they differ only in the "Updated … May 2026" header line and the SOLTN spacing.
- The commit list (reviewer's `commits.json`): a4c9117d7d (2013-04-26), 8b7efc2b2a (2026-05-29).
- `sed -n 5020,5100p` of `sifdecode.f90` (SBOUND; sha256 06cfe6d7…). Result: individual XL/XU/XX cards assign B_l/B_u unconditionally.
- `python3 checks/hvycrash_sif_bounds.py 50` (log `checks/logs/hvycrash_sif_bounds_N50.log`). Result:
  - SIF 2026 and 2013 versions: 204 variables, fixed only X(1,0) and X(2,0); every θ_T ∈ [0, 6.2831854].
  - AMPL: 204 variables, fixed x1_0 and x2_0; all x3 ∈ [0, 6.2831854].
  - SIF vs AMPL: no variable with different bounds.
  - MINLPLib gms: 51 θ variables with .up = 6.2831854 and no .fx.
- `python3 checks/hvycrash_sif_bounds.py 1000` (log `…_N1000.log`). Result: 4004 variables, fixed only X(1,0) and X(2,0); every θ_T ∈ [0, 2π], in both versions.
- `grep` of the MINLPLib OSIL (201 variables, 150 constraints) and `sed` of the first rows of `hvycrash.gms`.
- `grep`/`sed` of the PrincetonLib indexed file (lines 714–822). Result: x1_0 fixed at 0.005, x2_0 at 2.20405, all 51 θ_k ∈ [0.005, 2π + 0.005].
- `grep` of the COCONUT Library 2 row (202 variables, 150 constraints).
- `grep` of the Buchanan, Andretta and JNVA texts for HVYCRASH sizes.
- Omheni (2014), PDF copied from the reviewer folder: `pdftotext` of PDF pp. 120, 134, 146, 158, 170, and of the error-code legends (Tables B.1, E.1).
- Prudente (2012): `curl` of the DOI, which redirects to repositorio.unicamp.br (HTTP 503, three attempts in total); Wayback availability API (no snapshot); OpenAlex metadata.

**ex6_2_5 / ex6_2_7**
- Bertsimas & Margaritis (arXiv 2311.01742v1, copied from the reviewer folder): `pdftotext`; Table 1 rows on PDF p. 27; setup text on PDF p. 24; `grep` for any gap definition (none found).
- `head` of the COCONUT `lib1_ex6_2_7.res`, `lib1_ex6_2_5.res` and `lib1_etamac.res` (all `modelstatus = 2.00`).
- Trombettoni et al.: `pdftotext` and the Tables 2 and 3 headers.
- WebSearch: McDonald Floudas "Decomposition based and branch and bound global optimization approaches for the phase equilibrium problem" pdf. No open copy found.

**eg_\***
- Archived JOGO PDF of Göß et al. (copied from the reviewer folder): `pdftotext -f 38 -l 38`. Table 17 eg_* rows confirmed.
- `pdftotext` of Göß arXiv v2: settings paragraphs (lines 812–824 and 1074–1100).
- Publisher correction:
  - OpenAlex (OA URL: Springer only);
  - Wayback availability API (no snapshot);
  - `curl` of the Springer PDF (3 KB HTML bot page);
  - WebFetch of the article page (redirect to idp.springer.com, not followed);
  - WebSearch for the correction (no copy);
  - `curl` of the TRR154 OPUS RIS export (preprint record only);
  - `curl` of the arXiv abs page (versions v1 and v2 only).
- `curl -L` of github.com/adriangoess/paraboloids main.zip (sha256 71ee269a…); `unzip`; `grep` for optcr, reslim, threads and gap. Result:
  - `pyomo_solver.py` sets SCIP and Gurobi gaps only for its own Pyomo calls;
  - the written GAMS files in `para_relaxation/instances/` contain no optCR;
  - three files were saved under `sources/eg/paraboloids_repo/`.
- GAMS: text extraction of `docs/RN_32.html` (optCR new default 0.0001, old 0.1) and `grep -i optcr optgams.def` (default 1e-4).
- CAMINO: `curl` of arxiv.org/pdf/2404.11786 (v2); `pdftotext`; `grep` for eg rows (Table 8, PDF p. 51) and for the time limit and gap settings; arXiv abs page (v1 17 Apr 2024, v2 26 Mar 2026); OpenAlex title search (MPC doi:10.1007/s12532-026-00331-4; correction doi:10.1007/s12532-026-00337-y).

**pricing050**
- `pdftotext` of the ORL preprint 7681, lines 568–640 (formula (9), bounds [0, 10], data).

**Other**
- `grep` of `sources/minlplib.solu` for the nine instances.
- `grep` of `reviews/closing-confirm-r2.md` and `-r3.md` for the proved ex6_2_5 and etamac digits.
- `grep` of `open-instances-summary.md` for the certified values.
- Manifest: 11 rows appended. A Python sha256 recheck of all rows gave 112 rows, 0 bad and no unlisted files.

### 14.3 Revision after review round 2 (2026-10-02)

**Review material**: `cat` of the reviewer's `PROGRESS.json`, logs and `sources/manifest.tsv` in `publication/reviews/lit-small-r2/`.

**CAMINO (R2-M1, minor 1)**
- `pdftotext -layout` of `sources/eg/camino_ghezzi_et_al_arxiv2404.11786v2.pdf`. Then:
  - `grep` for gurobi, scip, gap, time limit and success;
  - `sed` of the setup (text lines 1415–1450) and of the nonconvex discussion (lines 1565–1625);
  - a Python page lookup: setup on PDF p. 26, "all algorithms except SCIP and Gurobi" on p. 28, the time-limit rule and the Table 3 caption on p. 29, the Table 8 caption and column order on p. 49, the eg rows on p. 51.
- `cat` of the reviewer's copy of `using_amplpy.py`.
- `curl` (sequential, about 1 s apart) of five CAMINO-benchmark files from raw.githubusercontent.com (main branch): `results/26_03_10_results/noncvx_gurobi.csv`, `noncvx_scip.csv`, `noncvx_gurobi/overview.json`, `benchmark/using_amplpy.py`, `benchmark/wall_time_noncvx_sbmiqp.json`. The sha256 values equal those of the reviewer's copies.
- GitHub API: the commit list for `noncvx_gurobi.csv` (one commit, 66a134daf8, 2026-03-19) and the recursive tree of the repository.
- `curl` of `benchmark/create_plot.py` (saved); `grep` and `sed -n 600,670p` (success/fail/time-out logic).
- `curl` to /tmp of `join_csv_using_pandas.py` and `combine_files.sh`; `grep` for time-limit handling (none). `curl` of `results/26_03_10_results/noncvx.csv` (saved).
- Python scan of `noncvx_gurobi.csv` with the per-instance limits. Corrected after the round-3 scan: of 262 rows, 32 stopped early with bound = objective, 59 stopped early with a real finite bound ≠ objective, 2 stopped early with the 1e100 placeholder (eg_all_s and hadamard_9), 4 failed and 165 reached the limit. "Early" means time < 0.99 × the per-instance limit. The 59 real bounds show the column holds a genuine bound.
- `curl` of `https://www.minlplib.org/mod/{eg_disc2_s,eg_disc_s,eg_int_s}.mod` (saved in `sources/eg/minlplib_mod/`); `grep` of the row senses (27 ≥ rows, 1 ≤ row; e25–e28 do not contain x8).
- `sed -n 28,52p` of `open-instances-wave3/eg/retry.md`; `cat` of the three `retry/sol/*.retry.sol` files.
- `python3 checks/eg_camino_gurobi.py` (log `checks/logs/eg_camino_gurobi.log`). The first run printed the eg_disc2_s result and then stopped with a `ValueError` (float conversion of an interval). I fixed the print statement and moved the code into functions; the second run completed. Result: all three recorded points lie within the bounds, are integral, and satisfy all 28 rows on the enclosure. The smallest slacks are 7.5e-20, 7.8e-20 and 5.6e-20. The Gurobi bound minus the point objective is 0.244594, 0.431290 and 5.201056. Every SCIP bound is ≤ the point objective.

**Kosolap (minor 2)**
- `curl -L` of the PDF from science.lpnu.ua (sha256 d4128720…, equal to the reviewer's copy); `pdfinfo`; `pdftotext`; per-page `grep`. Table 1 is on PDF p. 4 (printed 34).
- Crossref record of doi:10.23939/acps2019.01.032: pages 32–36, vol. 4, issue 1.
- OpenAlex: `search="ex6_2_5"` and `filter=fulltext.search:ex6_2_5`, 4 hits each, including Kosolap 2019.

**eg_int_s history (minor 3)**
- `cat` of `sources/gamsworld/MINLPLib_points_eg_int_s.inc`; `grep objvar` of the eg_disc and eg_disc2 point files.
- `cd checks && python3 eg_int_s_oldpoint.py` (log `checks/logs/eg_int_s_oldpoint.log`). Result: within bounds and integral; one row not proved to hold, e12, with slack in [−6.3678e-9, −6.3678e-9]; the smallest objvar meeting rows e1–e24 at that x is 6.4531031591.
- `curl` of the three COIN-OR 2008 BONMIN logs (saved); `grep` of the size lines: "28 rows 8 columns 220 non-zeroes" and 196 nl-non-zeroes for each; job start 09/02/08. `curl` of the BARON-2 and LINDOGLOBAL-1 logs at the analogous URLs: HTTP 404. `grep` of the benchmark `index.html` links.

**Small fixes (minor 4)**
- `grep` of `sources/minlplib_gms/hvycrash.gms`: x51..x100 have .lo = 0.08 and .up = 0.417; x101.up = 6.2831854.
- `pdftotext -f 15 -l 15` and `-f 16 -l 16` of the ORL preprint 7681: (9c) "x ∈ [l, u]" on p. 15; "[l, u] = [0, 10]" on p. 16.
- `sha256sum` of the reviewer's paraboloids zip (71ee269a…, the same as my round-1 download); `unzip` to /tmp; README lines 25–50 (line 38 has the eg_ exception); `cat` of `scip.opt` and `gurobi.opt`; `grep -ril optcr` (no match); `cmp` of README with the saved copy (identical); the two .opt files copied to `sources/eg/paraboloids_repo/`.

**Other**
- `ps` to check that no process of mine was left running (none). Removed the temporary /tmp folder and `checks/__pycache__`.
- Manifest: 16 rows appended. A Python sha256 recheck of all rows gave 128 rows, 128 distinct paths, 0 bad, 0 unlisted and 0 missing.

### 14.4 Revision after review round 3 (2026-10-03)

Commands were run from the repository root; paths below start with `research-20260929/publication/` unless they are absolute. All checks were single-process, used at most two CPU cores, and covered only this track. No project-wide verification or CI checks were run.

- `rg`, `sed`, `head` and `cat` to read the report, round-3 review, saved trace headers and records, CAMINO data and the reviewer's check scripts and source manifest; `git status --short` to inspect existing changes.
- `pdftotext -layout -f 4 -l 4 literature/small/sources/kosolap/kosolap2019_acps_4-1_32.pdf -`; repeated with output `literature/small/checks/logs/kosolap_round3_page4.txt`.
- `pdftoppm -f 4 -l 4 -scale-to 1600 -singlefile -png literature/small/sources/kosolap/kosolap2019_acps_4-1_32.pdf literature/small/checks/logs/kosolap_table_round3`, followed by visual inspection of the PNG. I counted all 15 rows and compared both value columns, including the printed positive sign for G16.
- `pdfinfo reviews/lit-small-r3/sources/cuesta_et_al_arxiv2510.14122v3.pdf` and `pdftotext -layout` on that PDF, followed by a focused `rg` scan. `pdftotext -layout -f 32 -l 35` confirmed the setup, equation (32) and Table 5. After copying the source, the same extract was saved as `literature/small/checks/logs/cuesta_round3_pages32-35.txt`.
- `python3 literature/small/checks/review_round3.py > literature/small/checks/logs/review_round3.log`. This new check reads the trace field names and independently scans the CAMINO CSV with decimal arithmetic. All six trace records have size (28, 8, 220, 196). CAMINO counts: 32 early equal bounds, 59 early real unequal bounds, 2 early placeholders, 4 failed and 165 at the limit; total 262.
- `cp reviews/lit-small-r3/sources/cuesta_et_al_arxiv2510.14122v3.pdf literature/small/sources/cuesta_et_al_arxiv2510.14122v3.pdf`; `sha256sum` on both copies gave `b740fcc0cc143bf57cda5c5ab4a105854e9f2d45f6afe56126eca9da2fe8c6de`. Added the version-specific URL, original fetch date and verified hash to the track manifest.
- `python3 reviews/lit-small-r3/manifest_check.py > literature/small/checks/logs/manifest_check_round3.log`: 129 rows, 129 distinct paths, 0 bad hashes, 0 missing and 0 unlisted.
- `git diff --stat`, `git diff`, `git diff --check -- research-20260929/publication/literature/small/` and scoped `git status` returned no tracked changes. `git check-ignore` confirmed that the report, manifest and new script are ignored. I therefore also ran `git diff --no-index --check /dev/null <file>` on each of those three files: no whitespace diagnostics (exit 1 denotes differences from the empty file). Final `rg` and `sed` reads checked the repeated claims and review response.

## 15. References

**Libraries and instance sources**
- MINLPLib instance and point pages for the nine instances, https://www.minlplib.org (pages last updated 2026-09-14); `minlplib.solu`; Internet Archive snapshots from 2018-09-22 and 2024-04-13; AMPL files https://www.minlplib.org/mod/eg_disc2_s.mod, eg_disc_s.mod, eg_int_s.mod (fetched 2026-10-02; header "GAMS Convert at 01/12/18").
- GAMS World archive (GLOBALLib, old MINLPLib, PrincetonLib), https://github.com/GAMS-dev/gamsworld.
- C. A. Floudas et al., *Handbook of Test Problems in Local and Global Optimization*, Kluwer, 1999, doi:10.1007/978-1-4757-3040-1 (not read). Web supplement http://titan.princeton.edu/TestProblems/ (archived copies of chapter6.html and ex6.2.5–ex6.2.8.gms).
- HVYCRASH.SIF (Ph. L. Toint, 1994; updated by P. Heeman, 2026), https://github.com/ralna/SIF; first repository version commit a4c9117d7d (2013).
- SIFDecode, `src/decode/sifdecode.f90`, https://github.com/ralna/SIFDecode (master, fetched 2026-10-02); SIF manual section 3.2.12 (BOUNDS), archived copy of https://www.numerical.rl.ac.uk/lancelot/sif/node26.html.
- Yurttan's AMPL translation: https://vanderbei.princeton.edu/ampl/nlmodels/cute/hvycrash.mod.
- GAMS Model Library: etamac (SEQ=80), etamge (SEQ=144), pindyck (SEQ=28). GAMS 32 release notes (`docs/RN_32.html` in the GAMS distribution).
- COCONUT benchmark, Libraries 1 and 2, https://arnold-neumaier.at/glopt/coconut/Benchmark/Benchmark.html. O. Shcherbina, list of handbook misprints (2002).
- A. S. Manne, ETA-MACRO (1977, not read).
- R. S. Pindyck, Rev. Econ. Stat. 60(2) (1978) 238–251, doi:10.2307/1924977 (not read).
- A. I. Tyatushkin, A. I. Zholudev, N. M. Erinchek, LNCIS 180 (1992) 456–464, doi:10.1007/BFb0113313 (not read).

**Gibbs problems**
- C. M. McDonald, C. A. Floudas, Decomposition based and branch and bound global optimization approaches for the phase equilibrium problem, J. Glob. Optim. 5(3) (1994) 205–251, doi:10.1007/BF01096454 (not read).
- McDonald & Floudas, AIChE J. 41 (1995) 1798–1814, doi:10.1002/aic.690410715 (not read).
- McDonald & Floudas, Comput. Chem. Eng. 21 (1997) 1–23, doi:10.1016/0098-1354(95)00250-2 (not read).
- C. A. Floudas, *Deterministic Global Optimization: Theory, Methods and Applications*, Kluwer, 2000, doi:10.1007/978-1-4757-4949-6 (not read).
- Tessier, Brennecke, Stadtherr, Chem. Eng. Sci. 55 (2000) 1785–1796, doi:10.1016/S0009-2509(99)00442-X.
- Stadtherr, Xu, Burgos-Solórzano, Haynes, Int. J. Reliability and Safety 1 (2007) 465–488, doi:10.1504/IJRS.2007.016260.
- J. Ninin, PhD thesis, INP Toulouse, 2010, HAL tel-04275036.
- Ninin, Messine, Hansen, 4OR 13 (2015) 247–277, doi:10.1007/s10288-014-0269-0.
- Trombettoni, Araya, Neveu, Chabert, Proc. AAAI 25 (2011) 99–104, doi:10.1609/aaai.v25i1.7817 (French version: JFPC 2011, HAL hal-00654307).
- Najman, Bongartz, Mitsos, J. Glob. Optim. 80 (2021) 731–756, doi:10.1007/s10898-020-00977-x.
- D. Bertsimas, G. Margaritis, Global optimization: a machine learning approach, J. Glob. Optim. 91(1) (2025) 1–37, doi:10.1007/s10898-024-01434-9; read as arXiv:2311.01742v1 (Table 1, PDF p. 27).
- M. Cuesta, C. D'Ambrosio, M. Durbán, V. Guerrero, R. Spencer Trindade, On leveraging constrained smooth additive regression models for global optimization, arXiv:2510.14122v3 (8 Sep 2026), https://arxiv.org/abs/2510.14122v3; Section 6, PDF pp. 32–34; Table 5, PDF p. 35.
- A. Kosolap, Finding the global minimum of the general quadratic problems during deterministic global optimization in cyber-physical systems, Advances in Cyber-Physical Systems 4(1) (2019) 32–36 (Crossref pages), doi:10.23939/acps2019.01.032; PDF http://science.lpnu.ua/sites/default/files/journal-paper/2019/aug/17917/7.pdf (Table 1, PDF p. 4, printed p. 34).
- Mitsos & Barton, AIChE J. 53 (2007) 2131–2147, doi:10.1002/aic.11230 (abstract only).
- Baker, Pierce, Luks (1982), doi:10.2118/9806-PA; Michelsen (1982), doi:10.1016/0378-3812(82)85001-2.

**Global-solver studies (etamac, pindyck)**
- Tawarmalani & Sahinidis, Math. Program. 103 (2005) 225–249, doi:10.1007/s10107-005-0581-8.
- Gleixner, Berthold, Müller, Weltge, J. Glob. Optim. 67 (2017) 731–757, doi:10.1007/s10898-016-0450-4.
- Müller, Serrano, Gleixner, SIAM J. Optim. 30 (2020) 1339–1365, doi:10.1137/19M1249825; arXiv:1903.05521v2.

**pricing050**
- Davarnia & van Hoeve, Math. Program. 187 (2021) 111–150, doi:10.1007/s10107-020-01475-4; read as optimization-online preprint 6512.
- Davarnia, Oper. Res. Lett. 49 (2021) 239–245, doi:10.1016/j.orl.2021.01.011; read as optimization-online preprint 7681.
- Davarnia, Kiaghadi, Qiu, J. Glob. Optim. (2026), doi:10.1007/s10898-026-01635-4.

**eg_***
- Göß, Burlacu, Martin, Parabolic approximation & relaxation for MINLP, J. Glob. Optim. 94(4) (2026) 951–996, doi:10.1007/s10898-026-01591-z; arXiv:2407.06143v2. Code: https://github.com/adriangoess/paraboloids (README line 38; `para_relaxation/instances/scip.opt`, `gurobi.opt`).
- Publisher Correction: Parabolic approximation & relaxation for MINLP, J. Glob. Optim. 95(4) (2026) 1095–1141, doi:10.1007/s10898-026-01614-9 (not read).
- Göß, arXiv:2603.16505 (2026); it has no eg_* entry.
- Cristofari, Di Pillo, Liuzzi, Lucidi, J. Optim. Theory Appl. 209 (2026) 38, doi:10.1007/s10957-026-02981-9.
- A. Ghezzi, W. Van Roy, S. Sager, M. Diehl, A sequential Benders-based mixed-integer quadratic programming algorithm and its implementation in the CAMINO toolbox, Math. Program. Comput. (2026), doi:10.1007/s12532-026-00331-4; correction doi:10.1007/s12532-026-00337-y (neither read); read as arXiv:2404.11786v2 (setup PDF p. 26; Table 3 PDF p. 29; Table 8 PDF pp. 49–51).
- CAMINO-benchmark repository, https://github.com/minlp-toolbox/CAMINO-benchmark, results of commit 66a134daf8 (2026-03-19): `results/26_03_10_results/noncvx_gurobi.csv`, `noncvx_scip.csv`, `noncvx.csv`, `noncvx_gurobi/overview.json`; `benchmark/using_amplpy.py`, `wall_time_noncvx_sbmiqp.json`, `create_plot.py`.
- D'Ambrosio, Frangioni, Liberti, Lodi, Math. Program. 136 (2012) 375–402, doi:10.1007/s10107-012-0608-x.
- COIN-OR GAMSlinks MINLP benchmark of 29 Sep 2008, https://www.coin-or.org/GAMSlinks/benchmarks/MINLP/080929_all/ (BARON-2 and LINDOGLOBAL-1 trace files; BONMIN-1 logs of eg_int_s, eg_disc_s and eg_disc2_s, run 2 Sep 2008).
- Blomqvist, MSc thesis, Åbo Akademi, 2025.

**hvycrash: local-solver reports**
- Gomes, Comput. Appl. Math. 26 (2007) 337–379, doi:10.1590/S0101-82052007000300003.
- Buchanan, MPhil thesis, Univ. Edinburgh, 2008.
- Andretta, thesis, USP, 2008.
- R. Omheni, Méthodes primales-duales régularisées pour l'optimisation non linéaire avec contraintes, PhD thesis, Univ. Limoges, 2014, HAL tel-01136063 (archived copy).
- L. F. Prudente, Inviabilidade em métodos de lagrangiano aumentado, PhD thesis, Unicamp, 2012, doi:10.47749/t/unicamp.2012.862465 (not read).
- Smith, PhD thesis, Carleton Univ., 2011, doi:10.22215/etd/2011-09468.
- Ahmadzadeh & Mahdavi-Amiri, J. Nonlinear Var. Anal. 10 (2026) 435–470, doi:10.23952/jnva.10.2026.2.10.

## 16. Revision after review round 1 (2026-10-02)

The round-1 review found one major and eleven minor issues. I checked each against the sources before changing the text.

**M1 (major): HVYCRASH SIF infeasibility and "modified" provenance. Accepted and fixed.**
- I read the BOUNDS section and SIFDecode's SBOUND myself, and wrote `checks/hvycrash_sif_bounds.py`, which applies the bound cards in file order. Result: the decoded SIF problem fixes only X(1,0) and X(2,0), and all θ_T lie in [0, 2π], at N = 50 and N = 1000, in both the 2013 and 2026 versions. At N = 50 it has exactly the AMPL bounds.
- The earlier claim that "the SIF fixes θ_0 and θ_N at 0" came from reading the XX cards without noticing that the later loop overrides them.
- Changes:
  - Summary table: "Modified … infeasible" replaced by "Same model".
  - Section 3.1 rewritten: new bounds paragraph and identity for every N; also, MINLPLib eliminates x1_0 as well, not only x2_0 and u0.
  - Section 3.2: "The SIF version has no feasible points" and "Our infeasibility observation explains these failures" deleted. The SOLTN(100)/(500)/(1000) argument now rests only on the identity.
  - Section 3.3: "differs from the infeasible SIF version" deleted. "Partly known" now rests on SOLTN −0.21850 being recorded for the identical problem.
  - Side finding 3 replaced by a neutral remark on the overridden XX cards.
- I also corrected "since 1994": the SOLTN line is present at least since the 2013 repository version; when it was added is not recorded.

**Minor issues**

| # | issue | what I did |
|---|---|---|
| 1 | PrincetonLib variant described inaccurately | Accepted. Confirmed in the indexed file (lines 714–822): x1_0 fixed at 0.005, x2_0 at 2.20405, all 51 θ_k ∈ [0.005, 2π + 0.005]. Section 3.1 fixed. I added that, by the identity, any feasible point of this variant has objective −0.2135 (feasibility not checked). |
| 2 | Missed Bertsimas & Margaritis (2025) | Accepted. Read Table 1 (arXiv v1, PDF p. 27) and the setup (PDF p. 24). Added to the summary table, Sections 4.2 and 5.2, side finding 6 and the references. The source is saved in `sources/`. |
| 3 | Publisher correction to Göß et al. not mentioned | Accepted. Cited in Section 9.2 and the references. My own attempts to read it failed (Section 14.2). Table 17 confirmed in the archived published PDF (copied to `sources/eg/`). Listed as unread in Section 13. |
| 4 | Gap tolerance can be pinned down | Accepted. Confirmed the GAMS 32 release notes (optCR default 1e-4, previously 0.1) and the paper's "default settings" sentence. I also checked the authors' public code: the GAMS files it writes set no optCR. Section 9.2 now says "very likely relative gap ≤ 1e-4, unless overridden on the command line". |
| 5 | Two dual bounds rounded the wrong way | Accepted. Section 5 now gives −70.75207783344770759 and Section 6 gives −15.294675643368093, the summary's outward-rounded values (proved digits from `reviews/closing-confirm-r2.md`). |
| 6 | Missed Omheni (2014) and Prudente (2012) | Accepted. Omheni read (PDF pp. 120, 134, 146, 158, 170; copied to `sources/hvycrash/`) and added to Section 3.2 and side finding 4. Prudente could not be read (Unicamp repository HTTP 503, three attempts); listed as unread. |
| 7 | McDonald & Floudas (1994) and Floudas (2000) not listed as unread | Accepted. Added to Sections 4.2, 5.2 and 13 and to the references. One WebSearch found no open copy. |
| 8 | pricing050: unscaled formula (9); preprint versus journal | Accepted. Confirmed that formula (9) is printed without the 1/10 scaling (ORL preprint p. 15). Added it as a further possible source of the discrepancy (Section 7.2, side finding 2). Sections 7.1, 7.2 and 12 and the references now say that both tables were read in the optimization-online preprints. |
| 9 | `minlplib.solu` disagrees with the instance pages | Accepted. Confirmed for all nine instances: all `=bestdual=` values are weaker, and hvycrash has none; ex6_2_5 differs too (−364.116 against −111.42). Added a table in Section 2 and a definition of "MINLPLib best dual". |
| 10 | Trombettoni et al.: tolerance stated too broadly | Accepted. The Table 2 and 3 headers show 1e-8 for BARON, GlobSol and IBBA+, 1e-3 for Icos, and both 1e-3 and 1e-8 for IbexOpt. Section 4.2 now states this, with the time limits per solver. |
| 11 | Small supporting details | **Partly accepted.** The COCONUT ex6_2_7 BARON 7.2 `modelstatus = 2.00` is confirmed and added to Section 4.2. The review said CAMINO's arXiv text has no eg_* entries. That is not so for the current version: arXiv:2404.11786v2 (26 Mar 2026), Table 8 (PDF p. 51), lists eg_all_s, eg_disc2_s, eg_disc_s and eg_int_s. pdftotext renders the names with spaces ("eg disc s"), which a search for "eg_" misses. At that point I agreed with the review's conclusion "primal only". **That conclusion was wrong for Gurobi; corrected in round 2 (Section 17, R2-M1).** CAMINO moved from "not read" to "read (arXiv v2)". |

**Effect on the consequences.** No consequence label changed:
- hvycrash, ex6_2_7 and ex6_2_5: partly known;
- etamac, pricing050, pindyck, eg_disc_s and eg_disc2_s: new as far as found;
- eg_int_s: already solved globally in floating point.

For hvycrash the reason for "partly known" is now stronger: the recorded value belongs to the identical problem.

## 17. Revision after review round 2 (2026-10-02)

The round-2 review confirmed the round-1 fixes and raised one major and four minor issues. I accepted all five after checking them myself, with my own downloads and my own code. The reviewer's files are in `publication/reviews/lit-small-r2/`.

**R2-M1 (major): CAMINO is not "primal values only"; Gurobi 13.0.0 claimed wrong optima on eg_disc2_s, eg_disc_s and eg_int_s. Accepted and fixed.**
- **Paper text read again.** In arXiv v2:
  - the setup is on PDF p. 26 (SCIP 9.2.2 and Gurobi 13.0.0 through the AMPL Python interface on .mod files; MINLP gap 1e-2; tolerance 1e-8);
  - the heuristic remark is on p. 28;
  - the per-instance time-limit rule and the Table 3 caption ("For SCIP and Gurobi 'success' correspond to a global optimal solution") are on p. 29;
  - Table 8 is on pp. 49–51.
- **Data re-fetched.** My downloads of the CAMINO-benchmark files have the same sha256 as the reviewer's copies. The driver records `obj.bestbound`. That column holds a genuine bound: it is a real finite value different from the objective on 59 runs that stopped early. Two more runs (eg_all_s and hadamard_9) carry only the 1e100 placeholder for no bound; they are excluded from the 59 (round-3 correction). On the three eg_* instances, Gurobi stopped after 2.15 s, 0.99 s and 70.80 s (limits 32.63 s, 19.24 s and 212.66 s), with bound = objective.
- **Independent proof that the claims are wrong.** `checks/eg_camino_gurobi.py` evaluates every row, bound and integrality condition of the MINLPLib .mod files at the project's recorded points, in outward-rounded interval arithmetic. All rows hold. This proves that the points are feasible for the models Gurobi solved, without relying on the .mod = OSIL identity. Gurobi's bounds exceed the point objectives by 0.244594, 0.431290 and 5.201056. The SCIP 9.2.2 bounds in the same data (−5.83, −6.74 and −4.26) are valid.
- **One refinement to the review.** The review says the Gurobi results are claimed global optima "by CAMINO's own definition". The Table 3 caption does say this. But the authors' counting script (`benchmark/create_plot.py`) counts a SCIP or Gurobi run as a "success" whenever the objective is finite and nonzero and the time is below 300 s, without checking the bound. So the Table 3 counts include runs that stopped at a per-instance limit, such as SCIP's runs here. I therefore base the finding on Gurobi's own bound = objective, reported before its limit, and cite the caption only as support.
- **Caveats stated.**
  - The csv does not record Gurobi's termination status.
  - CAMINO's local .mod copies are assumed to equal the current MINLPLib files.
  - The cause is unknown. As the review asked, I do not guess at it.
- **New detail found.** The same data give S-B-MIQP 5.642100351878204 on eg_disc2_s, 2.2e-7 below our certified bound (Section 11.1, side finding 9).
- **Changes:**
  - summary table rows for eg_int_s, eg_disc_s and eg_disc2_s;
  - side finding 6 in Section 1 and item 7 in Section 12;
  - Section 9.2: CAMINO rewritten as its own bullet, moved out of "primal-only results";
  - Sections 10.1 and 11.1: CAMINO bullets rewritten;
  - Sections 9.3, 10.2 and 11.2: one sentence each;
  - Section 13: limits;
  - Section 15: references;
  - Section 16, item 11: annotated as superseded.
- **Labels unchanged**, because a wrong optimality claim closes nothing:
  - eg_int_s: already solved globally in floating point (Göß et al.);
  - eg_disc_s and eg_disc2_s: new as far as found.

**Minor issues**

| # | issue | what I did |
|---|---|---|
| 1 | CAMINO time limits and versions | Accepted. The 300 s limit applies to Bonmin, SHOT and the S-B-MIQP variants. SCIP 9.2.2 and Gurobi 13.0.0 (through the AMPL Python interface) had the S-B-MIQP time of each instance: 32.63 s, 19.24 s and 212.66 s for eg_disc2_s, eg_disc_s and eg_int_s (`wall_time_noncvx_sbmiqp.json`; paper p. 29). Stated in Sections 9.2, 10.1 and 11.1, with all Table 8 wall times. |
| 2 | Missed Kosolap (2019) | Accepted. Re-fetched (same sha256) and read. Table 1 is on PDF p. 4 (printed p. 34); Crossref gives pp. 32–36. Ex6_2_5: n = 10, m = 3, EQR −70.9586 against "best glob. min." −70.75 (GL). The method uses local interior-point search. −70.9586 is 0.2065 below our certified lower bound. Added to the summary table, Section 5.2, Section 5.3, side finding 7 / item 8, and the references. Corrected in round 3: 14 of the 15 EQR values lie below their listed best known values; G16 is printed as 1.914608 against −1.9046617 and lies above. This paper was a round-1 OpenAlex hit that I did not follow up (Sections 2 and 13). |
| 3 | eg_int_s old point and model history | Accepted. `checks/eg_int_s_oldpoint.py` proves in interval arithmetic that the GAMS World point (objvar 6.4531031527) violates row e12 by 6.3678e-9, with everything else satisfied. Section 9.1 now calls it a tolerance artifact. I fetched the 2 Sep 2008 COIN-OR BONMIN logs of all three eg_* models: "28 rows 8 columns 220 non-zeroes", 196 nl-non-zeroes. So the two extra rows were added between August 2001 and September 2008. Confirmed in round 3: the saved BARON and LindoGlobal traces also list 28 equations, 8 variables, 220 nonzeros and 196 nonlinear nonzeros for each of these instances. Their full logs are not online (HTTP 404). |
| 4(a) | hvycrash summary cell | Accepted. Replaced "near-zero local-solver values at N = 1000" with the full list: COCONUT, Smith, SOLTN for N = 100/500/1000, and Omheni's objectives at N = 1000 (−0.18 to 1.1e-19). |
| 4(b) | "c_k" in Section 3.1 | Accepted. Now "the controls U(1..50) = x51..x100 lie in [0.08, 0.417]" (checked in `hvycrash.gms`). I also cite the reviewer's numerical row comparison (maximum difference 2.1e-48), which replaces "by inspection only" in Sections 3.1 and 13. |
| 4(c) | Page of the pricing bounds | Accepted. Formula (9) with (9c) x ∈ [l, u] is on ORL preprint p. 15; "[l, u] = [0, 10]" is on p. 16. Section 7.1 fixed. |
| 4(d) | paraboloids README and option files | Accepted. README line 38 says the eg_ files are not included "due to their size", so the absence of optCR is inferred for eg_*. `scip.opt` (`limits/memory=61440`) and `gurobi.opt` (`nonconvex=2`, `memlimit=60`) set no gap. Both were saved and cited in Section 9.2. |

**Not adopted:** none. The reviewer's cross-track notes (Kosolap 2021 on chain50, CAMINO values for the KAN instances, and the Gurobi 13.0.2 eg_* results of the solver campaign) concern other tracks and are not changed here.

**Sources added in this revision** (16 manifest rows):
- seven CAMINO-benchmark files;
- three MINLPLib .mod files;
- Kosolap (2019);
- three BONMIN 2008 logs;
- two paraboloids option files.

The manifest recheck gives 128 rows, 0 bad, 0 missing and 0 unlisted.

## 18. Response to review round 3 (2026-10-03)

Integration review r1, item 15: replaced the sample-only eg_disc2_s status with the all-leaf result, exact coverage proof and separate interval sample; retained A1/A2 and the earlier sample as history.

I checked all four minor issues against the saved sources and accepted all four.

1. **Kosolap Table 1:** visually read PDF p. 4 and counted 15 rows. 14 EQR values lie below the listed best known values; G16 is printed as 1.914608 against −1.9046617 and lies above. Fixed Sections 5.2, 12 and 17. The ex6_2_5 finding is unchanged.
2. **2008 BARON and LindoGlobal:** read the trace headers and checked all six eg_* records by code. Each lists 28 equations, 8 variables, 220 nonzeros and 196 nonlinear nonzeros. Replaced the model-size assumption in Sections 9.1 and 17 with this evidence. Matching size alone does not prove equality of every coefficient.
3. **Cuesta et al.:** read arXiv:2510.14122v3, Section 6 and Table 5. Gurobi 12.0.1, BARON 24.5.8 and COUENNE 0.5.8 close neither ex6_2_5 nor ex6_2_7 with a 600 s limit. Added the exact printed values, times and gaps in Sections 4.2 and 5.2, a reference in Section 15 and a search limitation in Section 13. Copied the reviewer's saved PDF into `sources/` and added its verified sha256 to the manifest.
4. **CAMINO bound count:** my independent decimal scan gives 59 early runs with a real finite bound different from the objective. eg_all_s and hadamard_9 carry only the 1e100 placeholder. Corrected Sections 9.2, 14.3 and 17. The three eg_* optimality findings are unchanged.

Evidence and commands are in Section 14.4 and `checks/logs/`. The manifest check passes: 129 rows, 129 distinct paths, 0 bad hashes, 0 missing and 0 unlisted. No disagreement with the review and no consequence label changes.
