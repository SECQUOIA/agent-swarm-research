<!-- Written to disk by the root from the structured return value of agent 'author:lit-small' (the harness blocks subagents from writing report files). Status: partial. -->

# Literature check: small process, economics and geometry models (track lit-small)

Date: 2026-10-01. Instances: hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck, eg_int_s, eg_disc_s, eg_disc2_s. The claims checked are those in `research-20260929/open-instances-summary.md` and the notes it links (`open-instances-wave2/small/report.md`, `open-instances-wave2/small/pindyck-extension.md`, `open-instances-wave3/eg/retry.md`).

Status: the planned searches are finished. Some key sources could not be read (Section 13), and the harness did not allow this file to be written, so the parent needs to save it. A search that finds nothing does not show that a result is new.

Labels used below:
- **rigorous**: a bound proved with exact or outward-rounded arithmetic.
- **floating-point global**: a deterministic global solver or an ε-global method reports optimality within its own tolerances.
- **local**: a value from a local or heuristic solver.
- **listing**: a value given in a test library.

Saved copies of fetched sources are in `publication/literature/small/sources/`. `sources/manifest.tsv` lists each file with its URL, fetch date (2026-10-01) and sha256 (101 files). The checks written for this track are in `checks/`, with logs in `checks/logs/`. They give numerical evidence, not proofs.

## 1. Summary

| instance | provenance (is the MINLPLib model the source model?) | strongest prior result found | consequence for our claim |
|---|---|---|---|
| hvycrash | CUTE problem HVYCRASH (SIF file by Ph. Toint, 1994), taken through H. Yurttan's AMPL translation with N = 50. **Modified**: the AMPL and MINLPLib versions leave θ_0 and θ_50 free in [0, 2π]. The SIF fixes both at 0, which makes the SIF version infeasible. | listing: the SIF file records the solution value SOLTN = −0.21850, with no proof. No global result or dual bound was found in the literature. Other published values (−0.0481, −1.905) cannot come from feasible points. | **partly known**. The value has been on record since 1994. The identity (the objective is constant on the feasible set) and an exactly feasible point are new as far as found, but both are elementary. |
| ex6_2_7 | Floudas et al. handbook (1999), Ch. 6, Test Problem 7: ethylene glycol – lauryl alcohol – nitromethane, UNIQUAC, three liquid phases. **Same model**: the handbook GAMS model with constants rounded to double (relative difference ≤ 4.1e-14). | floating-point global, very likely but not read: MINLPLib cites McDonald & Floudas (1997, GLOPEQ), a deterministic ε-global method. The handbook GAMS start point is within 4.3e-4 of our optimum, with objective 8.2e-7 above it. Rigorous interval solvers and BARON failed (2010–2015). MAiNGO failed in 8 h (2021). | **partly known**. The optimal value was very likely reported as an ε-global solution in floating point. No rigorous certificate was found, so ours is new as far as found. |
| ex6_2_5 | Same handbook, Ch. 6, Test Problem 5: sec-butyl alcohol – di-sec-butyl ether – water, with UNIQUAC liquids and an ideal vapour. **Same model** up to rounding (≤ 9.4e-14). | As for ex6_2_7. The handbook start point is within 3.0e-5 of our optimum, with objective 1.0e-10 above it. Interval solvers and BARON failed (2010–2015). | **partly known**, as for ex6_2_7. |
| etamac | GAMS Model Library model etamac (SEQ=80), A. Manne's ETA-MACRO (1977). **Same model** as the GLOBALLib scalar version (checked). Not checked against Manne's text. | local: MINOS −15.2947 (COCONUT) and CONOPT point p1 (MINLPLib). Global solvers: root-node studies only (BARON 2005, SCIP 2017). | **new as far as found**. No global claim or certificate was found. |
| pricing050 | Continuous version of the marketing pricing model of Davarnia & van Hoeve (2021), n = 50. There is strong evidence that it is their instance #2 (Section 7). Contributed to MINLPLib in 2024 by M. Kiaghadi. | Dual bounds only: decision-diagram bound 1663.7 and solver bounds ≤ 1437.6 (Davarnia 2021, 300 s). MINLPLib best dual 1534.33 (SCIP). All values in min form. | **new as far as found**. The primal value 1813.3 that Davarnia (2021) reports for instance #2 is below our certified minimum 1813.829. |
| pindyck | GAMS Model Library model pindyck (SEQ=28), after Pindyck (1978). **Same model** as the GLOBALLib scalar version. | SCIP studies did not solve it: root bound −2239.98, and the 1800 s tree runs hit the limit (Müller et al. 2020). The COCONUT "best" value −1612.18 belongs to a mistranslated model. | **new as far as found**. |
| eg_int_s | "Bram Schoonen's Model Collection" (MINLPLib, 2002). We found no document on its origin. | floating-point global: SCIP 8.1 solved it (Göß, Burlacu, Martin 2026: 9085 s on 8 threads; gap tolerance not stated). | **already solved globally in floating point**. As far as found, ours is the first rigorous certificate. |
| eg_disc_s | same collection | Best dual 3.6 (SCIP 8.1, 4 h; the authors flag this run for numerical or memory errors). MINLPLib best dual 3.366 (SCIP). | **new as far as found** |
| eg_disc2_s | same collection | Best dual −1.1 (SCIP 8.1, 4 h). MINLPLib best dual 0 (SHOT). | **new as far as found** |

Side findings the paper may need (details in Section 12):
1. The COCONUT benchmark's best value for pindyck (−1612.1783) comes from a translation that drops the factor 1/7 in the exponent. It is not a value of the MINLPLib model.
2. Davarnia (2021, Table 1) gives the primal value 1813.3 for the instance that is very likely pricing050. Our certified minimum is 1813.8290784519…. So, unless the data differ, no feasible point of pricing050 has that value.
3. The CUTE SIF version of HVYCRASH is infeasible for every N.
4. The published "best" hvycrash values −0.0481 (COCONUT) and −1.905155235 (Smith 2011) cannot come from feasible points.

## 2. How the search was done

- **MINLPLib**: current instance pages (cached in `bound-audit/pages/`), point pages (`sources/minlplib_points/`), the file `minlplib.solu`, and the earliest Internet Archive snapshot of each instance page (2018-09-22; for pricing050, 2024-04-13), saved in `sources/minlplib_history/`.
- **Original sources**: the GAMS World archive on GitHub (GLOBALLib and old MINLPLib scalar models, PrincetonLib CUTE translations), the handbook's web supplement (titan.princeton.edu, archived copy), the CUTE SIF file, Vanderbei's AMPL file, the GAMS Model Library pages and the COCONUT benchmark pages.
- **Literature**:
  - WebSearch, about 23 queries (listed in Section 14).
  - OpenAlex full-text search, 22 queries. This found most of the useful papers.
  - Crossref for bibliographic data.
  - The project's local literature collection (`literature/papers/`), searched with grep for every instance name.
  - DuckDuckGo: one useful query before it was rate-limited.
- **Reading**: every fact below was read in the source itself (PDF text or HTML), not taken from search snippets, unless it is marked "not read".

## 3. hvycrash

**Our claim.** The objective equals −0.2185 at every feasible point. This is an exact identity that follows from the rows alg_k. An exactly feasible point exists, so the optimum is −0.2185 (wave-2 small report, Section 3; verified).

### 3.1 Provenance
- **MINLPLib page**: source "CUTE model hvycrash", added 6 Feb 2017. References: Ivashkevich (1976) and Tyatushkin, Zholudev & Erinchek (1992).
- **SIF file** HVYCRASH (`sources/hvycrash/HVYCRASH.SIF`). It says "SIF input: Ph. Toint, February 1994" and "Updated to improve processing, Pim Heeman, May 2026".
  - The header calls the problem "freely inspired by" the heavy spacecraft landing problem. Because "No feasible point was found for the original formulation by any of the packages at hand", it drops the final-state constraint on the second variable and sets EPS = 0 in the second constraint.
  - Classification LOR2-AN-V-V. Objective X(1,N).
  - Fixed variables: X(1,0) = 0, X(2,0) = 2.19905, X(3,0) = 0, X(3,N) = 0.
  - N = 50 is marked as the "original value"; the current default is N = 1000.
- **AMPL translation** by Hande Yurttan (Vanderbei's CUTE collection, `sources/hvycrash/hvycrash.mod`, N = 50). It keeps x1_0 = 0 and x2_0 = 2.19905, but gives x3_0 and x3_50 the bounds [0, 6.2831854] instead of fixing them at 0.
- **MINLPLib hvycrash matches the AMPL version**: θ_0 = x101 ∈ [0, 6.2831854], θ_50 ∈ [0, 6.2831854], c_k ∈ [0.08, 0.417]. The unused x2_0 and u0 are removed. The GAMS World PrincetonLib translation is a third variant: it fixes x1_0 at epsi = 0.005 and bounds θ_0 and θ_50 below by 0.005.
- **The SIF version is infeasible.** This is our own observation, exact and checked by hand.
  - Row C(2,N) of the SIF reads −1/r − cos θ_N/(D r³) = 0, with D = 1.62079 (0.01 + 0.3 u²) > 0.
  - With θ_N fixed at 0, this becomes −(D r² + 1)/(D r³) = 0, which has no real solution.
  - So MINLPLib's instance is a modified, feasible version of the CUTE problem, not the SIF problem as written.

### 3.2 Prior results
- **SIF file, solution line** (listing, no proof): "`*LO SOLTN -0.21850`".
  - Further lines give SOLTN(100) = 3.26705331D-8, SOLTN(500) = 2.36171208D-8 and SOLTN(1000) = 8.48265630D-8.
  - −0.21850 equals −TT, the value our identity forces for every N. The file does not say why.
  - The other SOLTN values cannot come from feasible points. The SIF version has no feasible points, and every feasible point of the AMPL variants has objective X(1,0) − 0.2185.
- **COCONUT benchmark, Library 2** (#2439; `sources/coconut/`): the table gives Fbest = −0.0481. The linked "best solution" (solver OQNLP) has objective −0.1573199996, model status 5 and "infeas = 14". Neither value comes from a feasible point.
- **Smith (2011), PhD thesis, Carleton University**, Appendix A, Table A.1 ("Best Known Objective Function Values for Feasible Solution Vectors to Test Models from the COCONUT Benchmark"): hvycrash −1.905155235.
  - By the tolerance remark in our wave-2 report (Section 3), a point whose rows are violated by at most τ has objective ≥ −0.2185(1 + 7.86τ) − 50τ.
  - Reaching −1.905 needs τ ≈ 0.03, so this is not the value of a feasible point.
- **Local-solver studies of the CUTE (SIF) HVYCRASH** (local results, on the infeasible SIF version):
  - Gomes (2007), p. 375: HVYCRASH (n = 4004, m = 3000) is among the problems where the GMM code "has found a lower objective function" than Lancelot.
  - Buchanan (2008), MPhil thesis (Edinburgh), PDF pp. 115 and 124: iteration limit; "Feasible point is never found".
  - Andretta (2008), USP thesis, PDF pp. 46–47: Algencan stops at the time or iteration limit.
  - Ahmadzadeh & Mahdavi-Amiri (2026) include it in their test set.
  - Our infeasibility observation explains these failures. None of these sources states it.
- **MINLPLib**:
  - Points p1–p3 were found by COUENNE (2017–2018). p3 = −0.2185 (infeasibility 1e-12). p1 and p2 = −0.21413 are tolerance artifacts (our report).
  - The only dual bound is SCIP's −2.185e8. The 2018 snapshot lists no dual bound.

### 3.3 Consequence
**Partly known.** The optimal value −0.2185 has been in the SIF file since 1994, without a proof, and MINLPLib still lists the instance as open. We found no source that says the objective is constant on the feasible set, or that gives an exactly feasible point. The closure is a short exact argument, not a computational result. The paper should present it that way, credit the SIF value, and note that the MINLPLib version differs from the infeasible SIF version.

## 4. ex6_2_7

**Our claim.** Rigorous dual bound −0.16084761546364905 (the verifier's value), with gap 4.8e-14 to an exactly feasible point. Method: a Lagrangian over the mass balances plus a tangent-plane test by interval branch and bound.

### 4.1 Provenance
- **MINLPLib**: "Test Problem ex6.2.7 of Chapter 6 of Floudas e.a. handbook". References: the handbook (Floudas et al. 1999) and McDonald & Floudas (1997, GLOPEQ). Added 31 Jul 2001.
- **Handbook web supplement** (archived copies in `sources/titan/`):
  - Chapter 6 is "Biconvex and Difference of Convex Functions (D.C.) Problems". In its D.C. part, Test Problem 7 is "Ethylene Glycol - Lauryl Alcohol - Nitromethane -- Gibbs energy minimization (UNIQUAC)" (ex6.2.7.gms).
  - The GAMS file sets T = 295 K, P = 1 atm, three liquid phases and feed (0.4, 0.1, 0.5), with UNIQUAC r = (2.4088, 8.8495, 2.0086), q = q' = (2.248, 7.372, 1.868), the interaction parameters, and bounds 1e-7 ≤ n ≤ ntot.
  - Test Problem 8 (ex6.2.8) is the tangent-plane distance problem for the same system, at a different composition (0.29672, 0.46950, 0.23378).
- Tessier, Brennecke & Stadtherr (2000), Table 10 (preprint p. 28), attribute the same UNIQUAC data to McDonald & Floudas (1995a, AIChE J.). Their feeds differ from (0.4, 0.1, 0.5).
- **The MINLPLib model is the handbook model up to rounding.**
  - The MINLPLib GAMS file equals the GLOBALLib scalar file (GAMS Convert, 2001) up to term order. Equation residuals agree to 1e-39 at 20 random points (`checks/compare_gms.py`).
  - We re-implemented the handbook objective from its GAMS source. It agrees with the MINLPLib objective to ≤ 4.1e-14 relative at 200 random points (`checks/gibbs_source_vs_minlplib.py`).
  - The difference comes from constants rounded to about 15 digits. This rounding also explains the 5e-14 non-cancellation R_p in our scaling analysis.

### 4.2 Prior results
- **Handbook (1999) and GLOPEQ (1997): not read.** Publisher pages were blocked, and no open copy was found.
  - Indirect evidence that they report our optimum: the handbook GAMS file starts from n.l = (0.00880, 0.33595, 0.05525; 0.00065, 0.00193, 0.09742; 0.30803, 0.14700, 0.04497).
  - This point satisfies the mass balances and lies within 4.3e-4 of our optimal point in every coordinate.
  - Its objective is −0.1608468, which is 8.2e-7 above our certified optimum −0.16084761546 (`checks/handbook_start_points.py`).
  - The start point is most likely the handbook's reported solution, rounded.
- **Status of the McDonald–Floudas methods** (floating-point global):
  - Stadtherr, Xu, Burgos-Solórzano & Haynes (2007, preprint p. 2) describe them as deterministic global optimization (GOP, and branch and bound with convex underestimators). They note that whether α-BB bounds are "rigorously valid bounds depends on the proper choice of a parameter (α)".
  - Tessier et al. (2000) call them methods "which provide a mathematical guarantee of reliability".
  - Neither source treats ex6.2.7 itself. These are ε-global methods in floating point, not outward-rounded certificates.
- **COCONUT, Library 1**: Fbest −0.1608, best point found by BARON 7.2 (objective −0.1608476155 in the .res file). This is a primal value only.
- **Rigorous interval solvers failed**:
  - Ninin (2010), PhD thesis, INP Toulouse, Table 3.1 (p. 63): no IBBA variant solved ex6_2_7 within 1 h at precision 1e-8.
  - Same thesis, Table 3.6 (p. 71): started with the best known value −0.1608, IBBA+CP+rART reached only the lower bound −66.227346367 after 4025.5 s.
  - Ninin, Messine & Hansen (2015, 4OR; preprint 2012, Tables 1 and 3): the same outcome.
  - Trombettoni, Araya, Neveu & Chabert (AAAI 2011), p. 103: "Three systems (ex6_2_5, ex6_2_7 and ex7_2_3) are removed from this table because they are not solved by any solver, including Baron". The solvers were IbexOpt, IBBA+, GlobSol and Icos with ε_obj = 1e-8, and BARON 9.0.7 on NEOS with a 1000 s limit.
- **MAiNGO** (floating-point global): Najman, Bongartz & Mitsos (2021), Table 7. ex6_2_7 was not solved within 8 h at tolerance 1e-4 with any of five linearization strategies. The final lower/upper bound ratio was 14.8%–17.8%.
- **MINLPLib**: point p1 by CONOPT (2014), objective −0.160847615463598. Open in 2018 and now; the best listed dual is BARON's −1.06726714.
- **Method precedents** (not instance results): the tangent-plane criterion (Baker, Pierce & Luks 1982; Michelsen 1982), and its Lagrangian-dual reading (Mitsos & Barton 2007). Mitsos & Barton has NRTL and UNIQUAC case studies but was not read. It cites McDonald & Floudas 1995a, so its UNIQUAC case may be the same ternary system, at an unknown feed.

### 4.3 Consequence
**Partly known.** The handbook and GLOPEQ very likely reported the optimal point and value as an ε-global solution in floating point; we could not read either text to confirm the exact claim. No rigorous certificate was found. The interval solvers that aim at rigor failed on this instance, and BARON and MAiNGO did not close it either. Our contribution is the first rigorous closure as far as found, not the first solution. The tangent-plane method itself is classical.

## 5. ex6_2_5

**Our claim.** Rigorous dual bound −70.75207783344770758 (verifier), gap 2.0e-15. Same method as for ex6_2_7.

### 5.1 Provenance
- **MINLPLib**: "Test Problem ex6.2.5 of Chapter 6 of Floudas e.a. handbook", with the same references. Added 31 Jul 2001.
- **Handbook supplement**: Test Problem 5, "SBA - DSBE - Water -- Gibbs energy minimization (UNIQUAC)" — sec-butyl alcohol, di-sec-butyl ether, water (`sources/titan/ex6.2.5.gms`).
  - Phases 1 and 2 are liquids: UNIQUAC with q' ≠ q and Gibbs energies of formation. Phase 3 is an ideal vapour.
  - P = 1.16996 atm; feed (40.30707, 5.14979, 54.54314).
  - The file sets `T = 721.67659` and has `T = 363.19909` commented out. Since 721.67659 = 1.987 × 363.19909, "T" holds R·T in cal/mol (our inference).
  - Test Problem 6 is the tangent-plane distance problem for the same system.
- **The MINLPLib model is the handbook model up to rounding**: it is identical to the GLOBALLib scalar file, and differs from the re-implemented handbook objective by ≤ 9.4e-14 relative at 200 random points.

### 5.2 Prior results
- **Handbook and GLOPEQ: not read**, as for ex6_2_7. The handbook start point gives the two liquid phases; we set the vapour by mass balance. After swapping the two identical liquid phases, it lies within 3.0e-5 of our optimal point. Its objective is −70.7520778333, 1.0e-10 above our certified optimum.
- Stadtherr et al. (2007) note that McDonald & Floudas also treated the asymmetric case with an excess-Gibbs-energy model for the liquids and an ideal-gas vapour. That is the structure of this problem.
- **COCONUT Library 1**: Fbest −70.7521, found by MINOS (local).
- **Rigorous interval solvers failed**:
  - Ninin (2010), Table 3.1: not solved in 1 h.
  - Same thesis, Table 3.6: with the known value −70.7521 supplied, the lower bound was −7036.008545972 after 4036.4 s.
  - Ninin, Messine & Hansen (2015): same outcome.
  - Trombettoni et al. (2011): quoted in Section 4.2.
- **MINLPLib**: point p1 by CONOPT (2014), −70.752077833445796. Open in 2018 and now; the best listed dual is BARON's −111.4201713.
- Not included in the MAiNGO study of Najman et al. (2021).

### 5.3 Consequence
**Partly known**, for the same reasons as ex6_2_7. The value was very likely reported as an ε-global solution in floating point. No rigorous certificate was found; ours is the first as far as found.

## 6. etamac

**Our claim.** Rigorous dual bound −15.294675643368092 (verifier), with gap 2.6e-15 to an exactly feasible point. Method: a convex relaxation (the production equalities relaxed to ≤, with a concave majorant) and a KKT tangent-plane certificate.

### 6.1 Provenance
- **MINLPLib**: source "GAMS Model Library model etamac". Reference: Manne, "ETA-MACRO: A Model of Energy-Economy Interactions", in Hitch (ed.), *Modeling Energy-Economy Interactions: Five Approaches*, Resources for the Future, 1977. Added 31 Jul 2001.
- **GAMS Model Library page** (`sources/gamslib/gamslib_etamac.html`): "Eta-Macro Energy Model for the USA (ETAMAC, SEQ=80)". It is an NLP that maximizes discounted log consumption, subject to nested CES production rows written as equalities (newprod, ftotalprod). The library also has ETAMGE (SEQ=144), the same model in MPSGE (complementarity) format.
- The MINLPLib scalar model is identical to the GLOBALLib scalar model; residuals agree exactly at 20 random points. We did not compare it with Manne's 1977 text, which we could not obtain.

### 6.2 Prior results
- **Local values**: COCONUT Library 1 gives Fbest −15.2947 from MINOS (.res objective −15.2946756434). MINLPLib point p1 by CONOPT (2014) is −15.29467564, with infeasibility 1e-10.
- **Global solvers, root-node studies only**:
  - Tawarmalani & Sahinidis (2005), Table 1 (p. 242): etamac is problem (8) of the GLOBALLib set used in the root-node cutting-plane study. It is not among the 26 problems solved to global optimality in Table 4 (p. 246).
  - Gleixner, Berthold, Müller & Weltge (2017): etamac is in the root-node OBBT tables (Tables 4 and 6) but not in the tree experiment (Table 8). Table 8 leaves out instances that no setting solved within 1 h, and instances excluded for errors. So SCIP either did not solve etamac or it was excluded.
  - Müller, Serrano & Gleixner (2020, arXiv v2), Table 3: etamac appears only with bilinear-term statistics.
- **MINLPLib**: open in 2018 (best dual: ANTIGONE −15.835) and now (SCIP −15.40567054).
- **The convexity argument** we used is standard economics: a CES function with negative exponent is concave and increasing, log utility is concave and increasing, so the equalities can be relaxed to ≤. We found no source that states this for etamac or derives a global bound from it.

### 6.3 Consequence
**New as far as found.** No global optimality claim was found, and no valid dual bound close to the optimum. The local value has long been known (MINOS, CONOPT), and the hidden convexity is classical in spirit; the paper should say so. The contribution is the certificate, including the concave majorant that handles the degree excess of 4e-16 coming from the file's exact decimals.

## 7. pricing050

**Our claim (maximization).** Rigorous upper bound −1813.8290784519730577 (verifier), with gap 1.0e-17 to an exactly feasible point. Method: a Lagrangian over the 5 rows, with certified one-dimensional minimizations. In min form: min Σ c_j x_j ≥ 1813.8290784519730577.

### 7.1 Provenance
- **MINLPLib page**: "A firm seeks to determine the price of several new products to enter a competitive market".
  - Source: "Mohammadreza Kiaghadi". References: Davarnia (2021, Oper. Res. Lett.) and Davarnia & van Hoeve (2021, Math. Program.). Added 25 Mar 2024.
  - The April 2024 snapshot lists no points and no bounds.
  - Point p1: "found by KNITRO and contributed by Çağrı Latifoğlu" (26 Aug 2024).
- **Davarnia & van Hoeve** (preprint optimization-online 6512, Section 6.2, pp. 17–18):
  - Integer pricing model: min Σ c_i x_i s.t. Σ_i a_i^j x_i e^(−x_i^(k_i^j)) ≥ b_j, with x_i ∈ {0, …, 10} and a "scaling factor 10, i.e., the prices are chosen among {0, 0.1, …, 1.0}".
  - Data: c ∈ u.d.d.[0, 20], a ∈ u.d.d.[0, 100], b ∈ u.d.d.[10n, 20n], k ∈ {1, 2, 3}, |J| = 5, five random instances per size.
  - The MINLPLib description sentence is taken from this section.
- **Davarnia (2021, ORL; preprint optimization-online 7681, pp. 15–18)** uses the continuous version, with x ∈ [0, 10], on the "benchmark problem instances studied in [9]", that is, Davarnia & van Hoeve.
- **pricing050's data fit this generator**: integer c in [0, 20]; a = integer/10; demand exp(−(x/10)^k) with k ∈ {1, 2, 3}; right-hand sides in [500, 1000] = [10n, 20n]; x ∈ [0, 10].
- **Which instance?**
  - We solved the integer version of pricing050 (x ∈ {0, …, 10}) exactly as a MILP, with one binary per (product, value). This used HiGHS in floating point (`checks/pricing050_integer_version.py`).
  - Its optimum is 1825.0.
  - Davarnia & van Hoeve, Table 6.1 (preprint p. 20), report the integer-version primal values 1592, **1825**, 1891, 2403 and 1800 for their five n = 50 instances.
  - So pricing050 is very likely the continuous version of their n = 50 instance #2. This is numerical evidence, not proof.

### 7.2 Prior results
- **Davarnia & van Hoeve (2021), Table 6.1**, n = 50, #2 (integer version, 300 s): UB 1825, decision-diagram (DD) bound 1786.3; ANTIGONE 1063.3, BARON 1299.0, COUENNE 1452.5, SCIP 1367.2. These bound the integer problem, not pricing050.
- **Davarnia (2021, ORL), Table 1**, n = 50, #2 (continuous version, 300 s; preprint p. 18): UB 1813.3, DD bound 1663.7; ANTIGONE 1037.4, BARON 1354.2, COUENNE 1437.6, SCIP 1368.3. "UB" is "the best primal bound obtained across all solvers within the time limit".
- **Inconsistency.** If this is the same instance, 1813.3 lies 0.53 (2.9e-4 relative) below our certified minimum 1813.8290784519…, so no feasible point has that value.
  - With our multipliers (3.05 and 2.17 on two rows), a point would need row violations of about 0.1 to gain 0.53. Normal solver tolerances do not allow that.
  - A transcription error, or different data, are also possible. This cannot be settled without the authors' data.
- **Davarnia, Kiaghadi & Qiu** (2026, J. Glob. Optim.; preprint optimization-online 2024/09) present a decision-diagram global solver tested on MINLPLib instances. pricing050 is not among them.
- **MINLPLib**: open; best listed dual SCIP −1534.3281 (max form).

### 7.3 Consequence
**New as far as found.** No global solution or close dual bound was found. The best published dual bound for this instance at n = 50 is the DD bound 1663.7 (min form), 8% below the optimum. The paper may mention the ORL value as an inconsistency, with the caveat that the instance identity rests on our MILP evidence.

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

**Our claim.** Rigorous dual bound 6.4531031529331155, exactly feasible point 6.4531031593842274 (gap 1.0e-9 relative). Verified: all leaves were re-certified independently.

### 9.1 Provenance (all three eg_* instances)
- **MINLPLib**: source "Bram Schoonen's Model Collection", added 25 Jul 2002, no reference. We found no paper or report that describes this collection or where the models come from.
- **Point histories** (MINLPLib point pages): eg_disc_s.p1 and eg_disc2_s.p1 were found by SBB with CONOPT3 (25 Jul 2002); eg_int_s.p1 by LaGO with CONOPT3 (11 Jan 2007). The old MINLPLib point file for eg_int_s (GAMS World archive) has objvar 6.4531031527.
- **Row count**: the GAMS World archive copy of eg_int_s has the same 28 rows as today's file (`checks/logs/compare_eg_int_s_current_vs_gamsworld.log`). But its header ("GAMS Convert at 08/22/01", 26 equations, 206 nonzeros) and the old MINLPLib table (26 rows) suggest that two rows were added after 2001. We could not find out when or why. Our claims concern the current OSIL model.

### 9.2 Prior results
- **Göß, Burlacu & Martin (2026), J. Glob. Optim. 94:951–996**, Appendix B.5, Table 17 (p. 988; Table 15 in arXiv v2):
  - Setup (Section 4.2): SCIP 8.1 and Gurobi 11.0.1, run through GAMS 46.4.0, with 8 threads, a 4 h limit and default settings.
  - eg_int_s, SCIP, original model: run time 9085.1 s, "primal value 6.5, dual value 6.5". That is, solved (floating-point global).
  - The paper does not state the gap tolerance. The default relative gap OptCR in GAMS 54.3 is 1e-4 (`optgams.def`; we did not check version 46.4), so "solved" probably means a relative gap ≤ 1e-4.
  - Gurobi reached the time limit on the original model.
- **2008 COIN-OR/GAMSlinks MINLP benchmark** (1 h runs; `sources/coinor_2008/`): BARON 8.1.5 primal 6.45310315899, bound −8.0807; LindoGlobal 5.0 primal 7.4631, bound −3.1577.
- **Primal-only results**:
  - Cristofari, Di Pillo, Liuzzi & Lucidi (2026, JOTA 209:38), Table 1 (p. 16): best known value 6.4531.
  - D'Ambrosio, Frangioni, Liberti & Lodi (2012, "A storm of feasibility pumps"), tables reprinted in D'Ambrosio's habilitation thesis: feasibility-pump runs only.
- **Blomqvist (2025, MSc thesis, Åbo Akademi, SHOT)** lists the eg_* instances in its test set (Appendix A) but reports only aggregate results.
- **MINLPLib**: best dual −1.21 (LINDO) in 2018; now 6.32629896 (SCIP).

### 9.3 Consequence
**Already solved globally in floating point** (Göß et al., SCIP 8.1). As far as found, ours is the first rigorous certificate, to 1e-9 relative, with an exactly feasible point. The paper must cite Göß et al. and must not claim to be the first to solve it.

## 10. eg_disc_s

**Our claim.** Rigorous dual bound 5.760539610694994, exactly feasible point 5.7605396164535106 (1.0e-9 relative). Verified.

### 10.1 Prior results
- **Göß et al. (2026), Table 17**: SCIP on the original model reached the 4 h limit with the values 3.6 | 5.8.
  - The column headers read "primal value | dual value", but only the reverse reading fits a minimization problem with optimum 5.7605 (as our retry note found). So the dual bound is 3.6.
  - This SCIP entry carries an asterisk: the instance "caused numerical and/or memory errors" with SCIP and was excluded from the SCIP evaluation.
  - Gurobi, original model: time limit, 2.0 | 7.5.
- **2008 COIN-OR benchmark**: BARON primal 5.76053961645, bound −8.0807; LindoGlobal primal 5.76053961646, bound −7.3125.
- **Cristofari et al. (2026), Table 1**: best known value 5.7605 (primal only).
- **MINLPLib**: best dual −4.02 (LINDO) in 2018; now 3.36596129 (SCIP).

### 10.2 Consequence
**New as far as found.** The best published dual bound is 3.6 (SCIP, with errors reported). The best MINLPLib bound is 3.366.

## 11. eg_disc2_s

**Our claim.** Rigorous dual bound 5.642100574331458, exactly feasible point 5.6421005799711068 (1.0e-9 relative). Verified, but seven of the eight parts only by a sample of leaves.

### 11.1 Prior results
- **Göß et al. (2026), Table 17**: SCIP, original model: time limit, −1.1 | 6.3 (dual −1.1 under the reverse reading). Gurobi: time limit, −5.2 | 7.0.
- **2008 COIN-OR benchmark**: BARON primal 5.93701554196 (not optimal), bound −8.0807; LindoGlobal primal 5.64210057997, bound −9.9793.
- **Cristofari et al. (2026), Table 1**: best known value 5.6421.
- **MINLPLib**: best dual −7.57 (LINDO) in 2018; now 0 (SHOT).

### 11.2 Consequence
**New as far as found.** No published dual bound above 0 was found. The paper should state that part of the independent verification is by sampling.

## 12. Side findings for the paper

1. **COCONUT pindyck value.** The COCONUT benchmark lists Fbest = −1612.1783 for pindyck, below the certified optimum −1170.486. Its GAMS translation has 1.02^(−cs) instead of 1.02^(−cs/7), and the listed point reproduces −1612.17830322903 exactly under that change (`checks/logs/coconut_pindyck.log`). A paper that cites COCONUT best values should not use this one.
2. **Pricing value in Davarnia (2021).** Our MILP evidence links pricing050 to the n = 50 instance #2: its integer version has optimum 1825, the value reported for #2. If that link holds, the continuous primal value 1813.3 in Davarnia (2021, Table 1) cannot be attained. Asking the authors would settle this; we did not contact anyone.
3. **HVYCRASH.** The SIF version is infeasible for every N, because θ_N is fixed at 0. MINLPLib's version, taken from the AMPL translation, frees θ_0 and θ_N; it is feasible and its objective is constant at −0.2185. The values −0.0481 (COCONUT) and −1.905155235 (Smith 2011) cannot come from feasible points.
4. **Handbook start points.** The handbook GAMS files for ex6.2.5 and ex6.2.7 start next to our optimal points (Sections 4.2 and 5.2). This is the best evidence available that the handbook reports these optima. Someone should check the book text before the paper says more than "very likely".

## 13. What could not be read, and other limits

- **Not read**:
  - the Floudas et al. handbook (1999) text;
  - McDonald & Floudas (1995a, 1995b, 1995c, 1997);
  - Mitsos & Barton (2007);
  - Manne (1977), Pindyck (1978) and Tyatushkin et al. (1992);
  - the CAMINO paper (Math. Program. Comput. 2026), an OpenAlex full-text hit for eg_*, probably primal only;
  - the 2001 OQGRG report, a hit for ex6_2_*, a local multistart method.
  
  Reasons: Springer, Elsevier and Wiley pages returned bot challenges or 403; the Google Books quota was exhausted; the UT repository returned 403; FreiDok returned 404.
- **Services that failed**: Semantic Scholar snippet search (HTTP 429, repeated), CORE (429), DuckDuckGo (rate-limited after one query), arXiv API (503), Unpaywall (request rejected). The Internet Archive was offline at first and worked later.
- **Search coverage**: OpenAlex full-text search covers only part of the literature, and WebSearch indexed the instance names poorly. Papers that report per-instance results only in supplementary files (for example BARON, ANTIGONE or Octeract benchmark papers) may have been missed. The Octeract claims we found concern other instances (transswitch).
- **Model identity** was checked numerically at random points, not proved. The instance identity of pricing050 rests on one floating-point MILP solve.
- **This file**: the harness did not let this subagent write report.md. The parent should save this text there.

## 14. Commands and queries actually run

All runs were single-process and short (seconds to about 2 minutes), from `research-20260929/publication/literature/small/` unless stated otherwise. No project-wide checks were run, no CI was inspected, and nothing was committed or posted.

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
- OpenAlex full-text search: hvycrash, etamac, pindyck, eg_int_s, ex6_2_5, ex6_2_7, pricing050, eg_disc2_s, "pindyck minlplib", "pindyck globallib", "etamac globallib", "etamac minlplib", "etamac gams", "hvycrash minlplib", "ex6_2_7 minlplib", eg_disc_s, eg_all_s, "pricing050 minlplib", "Kiaghadi pricing", "lauryl alcohol nitromethane ethylene glycol UNIQUAC", "di-sec-butyl ether sec-butyl alcohol water Gibbs", GLOPEQ.

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

## 15. References

**Libraries and instance sources**
- MINLPLib instance and point pages for the nine instances, https://www.minlplib.org (pages last updated 2026-09-14); `minlplib.solu`; Internet Archive snapshots from 2018-09-22 and 2024-04-13.
- GAMS World archive (GLOBALLib, old MINLPLib, PrincetonLib), https://github.com/GAMS-dev/gamsworld.
- C. A. Floudas et al., *Handbook of Test Problems in Local and Global Optimization*, Kluwer, 1999, doi:10.1007/978-1-4757-3040-1 (not read). Web supplement http://titan.princeton.edu/TestProblems/ (archived copies of chapter6.html and ex6.2.5–ex6.2.8.gms).
- HVYCRASH.SIF (Ph. L. Toint, 1994; updated by P. Heeman, 2026), https://github.com/ralna/SIF. Yurttan's AMPL translation: https://vanderbei.princeton.edu/ampl/nlmodels/cute/hvycrash.mod.
- GAMS Model Library: etamac (SEQ=80), etamge (SEQ=144), pindyck (SEQ=28).
- COCONUT benchmark, Libraries 1 and 2, https://arnold-neumaier.at/glopt/coconut/Benchmark/Benchmark.html. O. Shcherbina, list of handbook misprints (2002).
- A. S. Manne, ETA-MACRO (1977, not read).
- R. S. Pindyck, Rev. Econ. Stat. 60(2) (1978) 238–251, doi:10.2307/1924977 (not read).
- A. I. Tyatushkin, A. I. Zholudev, N. M. Erinchek, LNCIS 180 (1992) 456–464, doi:10.1007/BFb0113313 (not read).

**Gibbs problems**
- McDonald & Floudas, AIChE J. 41 (1995) 1798–1814, doi:10.1002/aic.690410715 (not read).
- McDonald & Floudas, Comput. Chem. Eng. 21 (1997) 1–23, doi:10.1016/0098-1354(95)00250-2 (not read).
- Tessier, Brennecke, Stadtherr, Chem. Eng. Sci. 55 (2000) 1785–1796, doi:10.1016/S0009-2509(99)00442-X.
- Stadtherr, Xu, Burgos-Solórzano, Haynes, Int. J. Reliability and Safety 1 (2007) 465–488, doi:10.1504/IJRS.2007.016260.
- J. Ninin, PhD thesis, INP Toulouse, 2010, HAL tel-04275036.
- Ninin, Messine, Hansen, 4OR 13 (2015) 247–277, doi:10.1007/s10288-014-0269-0.
- Trombettoni, Araya, Neveu, Chabert, Proc. AAAI 25 (2011) 99–104, doi:10.1609/aaai.v25i1.7817 (French version: JFPC 2011, HAL hal-00654307).
- Najman, Bongartz, Mitsos, J. Glob. Optim. 80 (2021) 731–756, doi:10.1007/s10898-020-00977-x.
- Mitsos & Barton, AIChE J. 53 (2007) 2131–2147, doi:10.1002/aic.11230 (abstract only).
- Baker, Pierce, Luks (1982), doi:10.2118/9806-PA; Michelsen (1982), doi:10.1016/0378-3812(82)85001-2.

**Global-solver studies (etamac, pindyck)**
- Tawarmalani & Sahinidis, Math. Program. 103 (2005) 225–249, doi:10.1007/s10107-005-0581-8.
- Gleixner, Berthold, Müller, Weltge, J. Glob. Optim. 67 (2017) 731–757, doi:10.1007/s10898-016-0450-4.
- Müller, Serrano, Gleixner, SIAM J. Optim. 30 (2020) 1339–1365, doi:10.1137/19M1249825; arXiv:1903.05521v2.

**pricing050**
- Davarnia & van Hoeve, Math. Program. 187 (2021) 111–150, doi:10.1007/s10107-020-01475-4.
- Davarnia, Oper. Res. Lett. 49 (2021) 239–245, doi:10.1016/j.orl.2021.01.011.
- Davarnia, Kiaghadi, Qiu, J. Glob. Optim. (2026), doi:10.1007/s10898-026-01635-4.

**eg_***
- Göß, Burlacu, Martin, J. Glob. Optim. 94 (2026) 951–996, doi:10.1007/s10898-026-01591-z; arXiv:2407.06143v2.
- Göß, arXiv:2603.16505 (2026); it has no eg_* entry.
- Cristofari, Di Pillo, Liuzzi, Lucidi, J. Optim. Theory Appl. 209 (2026) 38, doi:10.1007/s10957-026-02981-9.
- D'Ambrosio, Frangioni, Liberti, Lodi, Math. Program. 136 (2012) 375–402, doi:10.1007/s10107-012-0608-x.
- COIN-OR GAMSlinks MINLP benchmark of 29 Sep 2008.
- Blomqvist, MSc thesis, Åbo Akademi, 2025.

**hvycrash: local-solver reports**
- Gomes, Comput. Appl. Math. 26 (2007) 337–379, doi:10.1590/S0101-82052007000300003.
- Buchanan, MPhil thesis, Univ. Edinburgh, 2008.
- Andretta, thesis, USP, 2008.
- Smith, PhD thesis, Carleton Univ., 2011, doi:10.22215/etd/2011-09468.
- Ahmadzadeh & Mahdavi-Amiri, J. Nonlinear Var. Anal. 10 (2026) 435–470, doi:10.23952/jnva.10.2026.2.10.

## Commands run (from the agent's structured return)

- `python3 checks/compare_gms.py sources/minlplib_gms/<n>.gms sources/gamsworld/GlobalLib_scalar_models_<n>.gms 20 for n in ex6_2_5 ex6_2_7 etamac pindyck -> identical models (residuals agree to <=2.4e-39 or exactly); log checks/logs/compare_minlplib_vs_globallib.log`
- `python3 checks/compare_gms.py sources/minlplib_gms/eg_int_s.gms sources/gamsworld/MINLPLib_Scalar_models_eg_int_s.gms 5 -> identical; log checks/logs/compare_eg_int_s_current_vs_gamsworld.log`
- `python3 checks/gibbs_source_vs_minlplib.py -> handbook vs MINLPLib objective max rel. diff 4.13e-14 (ex6_2_7), 9.37e-14 (ex6_2_5)`
- `python3 checks/handbook_start_points.py -> handbook start objectives -0.160846800 / -70.7520778333; distance to our optima 4.3e-4 / 3.0e-5`
- `OMP_NUM_THREADS=1 python3 checks/pricing050_integer_version.py -> integer version MILP optimum 1825.0 (HiGHS); the first two runs, with a faulty term parser, reported Infeasible`
- `python3 checks/coconut_pindyck.py -> J(COCONUT prices) = 1612.17830322903 with exponent factor 1, 1057.218 with the correct 1/7`
- `curl downloads (sequential, ~1 s apart) of MINLPLib gms/point pages/minlplib.solu, GAMS World GitHub raw files, the SIF and AMPL hvycrash files, GAMS model library pages, COCONUT pages/res/mod/gms/dag, Internet Archive copies of titan handbook files and of the 2018 MINLPLib pages, COIN-OR 2008 traces, and PDFs from optimization-online, arXiv, AAAI, nd.edu, lirias, doria, carleton, ed.ac.uk, usp, scielo, jnva; all saved files listed with URL and sha256 in sources/manifest.tsv`
- `Failed fetches: Springer (bot challenge), ScienceDirect (403), HAL direct (bot challenge), Google Books (429/JS), CORE (429), Semantic Scholar snippet search (429 x3), Unpaywall (rejected), arXiv API (503), FreiDok (404), UT repository (403)`
- `OpenAlex full-text search (22 queries, listed in report Section 14); Crossref (~20 look-ups); Semantic Scholar paper API (3 DOIs); DuckDuckGo via curl (3 queries, then rate-limited)`
- `WebSearch (~23 queries, listed in report Section 14); WebFetch (Springer chapter -> redirect; ScienceDirect -> 403; yoric.mit.edu Mitsos-Barton abstract -> ok; HAL Ninin thesis -> bot page)`
- `grep over literature/papers/*/fulltext.md for instance names, ETA-MACRO, GLOPEQ, UNIQUAC, Gibbs, Schoonen; pdftotext -layout on fetched PDFs; read GAMS 54.3 optgams.def (OptCR default 1e-4)`

## Open issues (from the agent's structured return)

- report.md was not written: the harness blocks report .md files for this subagent. The full text is in the summary field; the parent should save it to /workspace/minlp-notes/research-20260929/publication/literature/small/report.md.
- The Floudas et al. handbook (1999) text and McDonald & Floudas GLOPEQ (1997) were not read. The claim that ex6_2_5/ex6_2_7 were solved epsilon-globally rests on MINLPLib's citation and on the handbook GAMS start points. Someone should check the book (Ch. 6, Test Problems 5 and 7) before the paper says more than 'very likely'.
- Mitsos & Barton (2007) was not read. Its UNIQUAC case study may be the same ethylene glycol - lauryl alcohol - nitromethane system (feed unknown).
- pricing050 instance identity (= Davarnia & van Hoeve n=50 #2) rests on one floating-point MILP solve. The discrepancy with the ORL primal value 1813.3 (below our certified 1813.829) is unresolved; it needs the authors' data. Nobody was contacted.
- Goess et al. do not state SCIP's gap tolerance for the eg_int_s solve. 'Solved' probably means relative gap <= 1e-4 (GAMS default), but this was not confirmed for GAMS 46.4.
- Origin of the eg_* models ('Bram Schoonen's Model Collection') is undocumented. Two rows appear to have been added after 2001 (the archived header says 26 rows, the current file has 28); when and why is unknown.
- Search coverage is limited: OpenAlex full text covers only part of the literature, and Semantic Scholar/CORE/DuckDuckGo were rate-limited. Per-instance results that appear only in solver papers' supplementary files may have been missed. CAMINO (MPC 2026) and OQGRG (2001) were not read; both are likely primal-only.
- Manne (1977) and Pindyck (1978) were not read, so the GAMS models were not checked against the original papers.
