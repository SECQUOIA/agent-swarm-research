<!-- Written to disk by the root from the structured return value of agent 'author:lit-control' (the harness blocks subagents from writing report files). Status: partial. -->

# Literature check: optimal control and CUTE-type instances (lit-control)

Date: 2026-10-01. Scope: lnts50/100/200/400, dtoc5, camshape100/200/400/800, lukvle10, optcdeg2, chain50/100/200/400, catmix100/200/400/800. Our claims are those of open-instances-summary.md; all 19 instances are in its "closed" table.

- Sources are in `publication/literature/control/sources/`, listed in `MANIFEST.md` with URL, fetch date and sha256.
- Floating-point provenance checks are in `publication/literature/control/checks/` (see `README.md`). They are evidence, not proofs.

Terms used below:
- **Rigorous certificate**: a bound proved with exact or outward-rounded arithmetic.
- **Floating-point claim**: a solver reported a gap within its tolerance, usually with a 1e-6 feasibility tolerance.
- **Local value**: the result of a local NLP solver.

## 1. Bottom line

- **16 of 19 instances: no prior global result found.** I found nothing, rigorous or floating-point, beyond the weak solver bounds listed on MINLPLib. For these, the closure is new as far as found.

- **lnts50–400: partly known.**
  - Gurobi solved lnts50 to its default tolerance. Source: Göß, Burlacu, Martín, J. Global Optim. 94 (2026) 951–996, doi:10.1007/s10898-026-01591-z, Table 17, p. 992.
  - Göß, arXiv:2603.16505v1 (17 Mar 2026), App. B, Table 4, p. 32, reports parabolic (PARA) relaxation dual bounds. The printed gaps are 0.00% for lnts50/100/200 and 0.01% for lnts400. These are floating-point claims.
  - Our closure to 5.5e-13 with a rigorous certificate is new as far as found. The paper must cite both works.

- **camshape100: already solved globally in floating point.**
  - Bestuzheva et al., arXiv:2301.00587v1 (JOGO 91 (2025) 287–310), App. B.1, pp. 36–37: Octeract 4.5.1 solved camshape100 in 19.40 s.
  - Settings: gap limits 1e-6 relative and 1e-6 absolute; feasibility tolerance 1e-6.
  - MINLPLib also lists an ANTIGONE bound within 1.2e-6 relative.
  - New for camshape100 is only the exact optimum with rational verification. camshape200–800 are new as far as found.

- **dtoc5 and optcdeg2 in MINLPLib are variants of their sources.** Both came through QPLIB (8585 and 8803). In both, the quadratic term in the dynamics is 4 times the coefficient in CUTEst and in the original source.
  - dtoc5: the term is 4h·y² instead of h·y² (Coleman–Liao problem 5).
  - optcdeg2: the damping is 0.2 instead of 0.05 (Murtagh–Saunders Ex. 5.11 / OPTCNTRL).
  - Our certificates are valid for the MINLPLib models as written. Published DTOC5/OPTCDEG2 values belong to different models.

- **Two published values lie below our certified bounds.** Both are explained as tolerance artifacts:
  - The CUTEst LUKVLE10.SIF line `SOLTN 3.52237E+02` is 1.0e-3 below our bound 352.2380254. IPOPT with |c_j| ≤ 1e-6 reaches 352.23762, which prints as 3.52237E+02.
  - Gurobi's optcdeg2 "optimum" 292.417 (MINLPLib point p2, row violation 1e-6) is 1.46 below the exact optimum 293.876.

- **COPS models: same models, local values only.** The MINLPLib chain, camshape, catmix and lnts are the GAMS translations of COPS 2.0.
  - The COPS 2.0 tables contain only local-solver values. The best of them agree with our exact optima to the printed digits, which appear to be truncated.
  - COPS never claims global optimality for these four problems.
  - COPS 3.0 catmix uses 3-stage collocation, so it is a different model from MINLPLib catmix.

### Summary table

| instance | provenance | strongest prior result | consequence |
|---|---|---|---|
| lnts50 | GAMS `lnts` = COPS 2.0 #9, nh=50; same model | Gurobi solved it to its default tolerance (JOGO 2026, Table 17); MINLPLib GUROBI bound 0.55464755 (rel. gap 3.8e-5); PARA gap "0.00%" | partly known (floating point); rigorous closure new as far as found |
| lnts100 | same, nh=100 | PARA dual bound, gap "0.00%" (<5e-5 rel.), Göß 2026 Table 4 | partly known (floating point) |
| lnts200 | same, nh=200 | PARA gap "0.00%" | partly known (floating point) |
| lnts400 | same, nh=400 | PARA gap "0.01%" | partly known (floating point) |
| dtoc5 | QPLIB_8585 ← CUTEst DTOC5 ← Coleman–Liao problem 5, N=50000; variant (4h·y²) | none; local values only for the h·y² variant | new as far as found |
| camshape100 | GAMS `camshape` = COPS 2.0 #4; drops one COPS curvature row (slack at the optimum) | Octeract 4.5.1 solved to 1e-6 gap (Bestuzheva et al.); ANTIGONE bound within 1.2e-6 | already solved globally in floating point; exact optimum new |
| camshape200 | same, n=200 | ANTIGONE −4.63229 (8.3% gap); COPS local values | new as far as found |
| camshape400 | same, n=400 | ANTIGONE −4.97266; COPS local values | new as far as found |
| camshape800 | same, n=800 | GUROBI −5.12584; COPS local values | new as far as found |
| lukvle10 | CUTEst LUKVLE10 = Lukšan–Vlček problem 5.10, N=1000; same model | SCIP bound 351.223; SIF SOLTN 352.237 (tolerance artifact) | new as far as found |
| optcdeg2 | QPLIB_8803 ← CUTEst OPTCDEG2 ← Murtagh–Saunders Ex. 5.11, T=50000; variant (damping 0.2) | Gurobi "optimal" 292.417 at 1e-6 violation; false under exact feasibility | new as far as found |
| chain50–400 | GAMS `chain` = COPS 2.0 #3; same model | COPS 2.0/3.0 local values; ANTIGONE bounds ≈ 0.08–0.17 | new as far as found |
| catmix100–800 | GAMS `catmix` = COPS 2.0 #14 (trapezoidal); not the COPS 3.0 model | COPS 2.0 LOQO local values; LINDO bounds only | new as far as found |

## 2. What was searched

**Primary sources read**
- COPS 2.0 (HTML, ANL/MCS-246) and COPS 3.0 (ANL/MCS-TM-273).
- GAMS library sources for camshape, chain, catmix and lnts (GAMS 54.3).
- CUTEst SIF files DTOC5, OPTCDEG2, OPTCNTRL and LUKVLE10, and Benson's AMPL versions.
- Coleman–Liao technical report (1993).
- Lukšan–Vlček V-767 (1999).
- QPLIB pages and .qplib files for 8585 and 8803.
- GLOBALLib archive (GAMS-dev/gamsworld on GitHub).
- COCONUT Library 1/2 tables and .res files.
- MINLPLib pages (cached) and bounddates.html.
- Mittelmann's MINLP benchmark: current page and compare.txt.

**Papers read or grepped for the instance names**
- Bestuzheva et al. 2023 (SCIP 8 MINLP).
- SCIP Optimization Suite 8.0 and 10.0 reports.
- Göß 2026 (arXiv) and Göß–Burlacu–Martín 2026 (JOGO).
- Neumaier–Shcherbina–Huyer–Vinkó 2005.
- Griva–Vanderbei 2005 (preprint) and Gabrys–Sremac 2025.
- Houska–Chachuat branch-and-lift (preprint).
- Mevissen–Lasserre–Henrion 2010.
- Mattick–Mutschler 2023.
- Smith 2011 PhD thesis.
- Bertsimas–Öztürk (arXiv:2202.06017).
- FICO Xpress Global 2025.
- QPLIB paper (Furini et al. 2019).
- GAMS GLOBALLib presentations.

**Web searches** (instance names and topics)
- Instance names; camshape with global solvers.
- Catalyst mixing global optimization; linear tangent steering global optimality; discretized hanging chain global minimum.
- QPLIB/CUTEst conversion errors.
- Octeract and open MINLPLib instances.
- Occupation-measure and moment-SOS bounds.
- SparsePOP and Lukšan–Vlček.
- Esposito–Floudas, Chachuat, Stadtherr and Barton global dynamic optimization.

**OpenAlex full-text search**
- All instance names, QPLIB_8585, QPLIB_8803, "COPS camshape" and "COPS catmix".
- New hits: Smith 2011, Mattick–Mutschler 2023 and Göß 2026.

**Failed attempts**
- Semantic Scholar snippet search: HTTP 429 on every query; abandoned.
- Internet Archive: offline at first. The archived 2023 Mittelmann compare.txt did not include camshape100.
- COCONUT per-model solver tables: cited online in 2005 but not retrievable.
- IBM report RC25385: connection refused.
- COPS 3.0 AMPL zip: 404.

**Not read** (paywall or no access)
- Murtagh–Saunders 1982; Lukšan–Vlček 1998 (NLAA); Anitescu–Serban 1998; Betts et al. 1993; Gunn–Thomas 1965; von Stryk 1999.
- Andrei 2013 (NOA book); ANTIGONE 2014 per-instance results; Esposito–Floudas 2000.

**Scope of these searches**
- An unsuccessful search does not establish novelty. Google Scholar and paywalled full text were not available.
- The global optimal-control literature I found (branch-and-lift, occupation measures, Esposito–Floudas) treats continuous-time problems. None of it used these discrete models.

## 3. Per-instance findings

### Family: COPS models (lnts, camshape, chain, catmix)

**MINLPLib and GLOBALLib**
- The MINLPLib pages say "Source: GAMS Model Library model <name>, COPS"; the instances were added 31 Jul 2001.
- They were GLOBALLib models. The GLOBALLib scalar files are dated 07/30/01. GLOBALLib stored no solution points and made no optimality claim.
- The GAMS headers name "COPS 2.0 #3/#4/#9/#14".

**COPS 2.0** (Dolan and Moré, ANL/MCS-246, Nov 2000, rev. 2 Jan 2001)
- Trapezoidal discretization, same sizes as MINLPLib.
- Local solvers only: LANCELOT, LOQO, MINOS, SNOPT. No global claims.

**COPS 3.0** (Dolan, Moré and Munson, ANL/MCS-TM-273, Feb 2004)
- Local solvers FILTER, KNITRO, LOQO, MINOS, SNOPT.
- It mentions global minima only for the polygon and electron problems.
- The printed COPS values appear truncated to 6 significant digits.

**COCONUT Library 1** (from GLOBALLib)
- Contains all 16 instances. Fbest values: camshape100 −4.2841, camshape200 −4.2785, catmix100/200 −0.0481, chain50 5.0723, chain100 5.0698, chain200 5.0689, chain400 5.0686, lnts50 0.5547, lnts100 0.5546.
- The stored .res files have modelstatus = 2 (locally optimal).
- Neumaier et al. (2005, Math. Program. 103:335–356) ran complete solvers on models with fewer than 1000 variables, but report only aggregates.

**Smith (2011) thesis, Table A.1**
- Gives heuristic values for COCONUT versions. Where comparable they are consistent with ours, e.g. chain50 5.072261494.
- The lnts50 −339.2, lnts400 −1255.1 and optcdeg2 0.009 entries are impossible for the MINLPLib models (lnts objective N·h ≥ 0). They come from different translations and are not comparable.

**MINLPLib bound history** (bounddates.html)
- Primal points date from 2014-08-15; camshape400/800 points p2 from 2018-05-22.
- Dual bounds were added 2014–2025, the latest from GUROBI on 2025-07-31 and 2025-08-07.
- No instance is marked solved (site update 2026-09-14).

### lnts50/100/200/400 (particle steering)

**Provenance**
- COPS 2.0 §9: minimize time; a = 100; |u| ≤ π/2; terminal y₂ = 5, ẏ₁ = 45, ẏ₂ = 0; trapezoidal rule.
- Boundary data from Betts et al. (1993); the classical problem is in Bryson and Ho (1975), pp. 59–62.
- MINLPLib is the GAMS conversion: bounds ±1.5707963267949, objective N·h, lnts50 has 256 variables = 5(nh+1)+1 as in COPS. Same model.
- The continuous linear-tangent solution does not certify the discrete optimum.

**Local values**
- COPS 2.0 Table 9.2, MINOS: 0.554668, 0.554595, 0.554577, 0.554572. SNOPT gives 0.554573 at nh=400.
- LANCELOT in the same table: 0.554672, 0.554594, 0.554588, 0.554552 (flagged), at violations 1.9e-6 to 8.6e-6. The nh=100 and nh=400 values lie below our exact optima (tolerance artifacts).
- COPS 3.0 Table 9.2 (p. 22): 0.554577 (nh=200) and 0.554572 (nh=400).
- All agree with our optima (0.55466876, 0.55459540, 0.55457702, 0.55457241) to the printed digits.

**Floating-point global results**
- MINLPLib GUROBI bounds: 0.55464755 (rel. gap 3.8e-5), 0.55299042, 0.55219867, 0.55204395.
- JOGO 2026, Table 17 (p. 992): Gurobi solves the original lnts50 in 5811.5 s (primal and dual printed as 0.6). lnts100–400 hit the 4 h limit.
- JOGO 2026, Table 11 (p. 972): SCIP gaps at the time limit are 0.0251, 0.0334, 0.0821 and 0.1033.
- Göß arXiv 2026, Table 4 (p. 32):
  - PARA relaxations with ε = 1e-4 (lnts50/100/200) and ε = 1e-3 (lnts400), solved by SCIP 10.0 (§4.2, p. 17).
  - Dual bounds printed as 5.5e-1; gaps 0.00% (lnts50/100/200) and 0.01% (lnts400); times 39, 161, 505 and 576 s.
  - The author writes that PARA "lead to dual bounds which can reduce the original gap to nearly zero".
  - The parabolas are computed and checked numerically, so these bounds are floating-point. They are not on MINLPLib.

**Per instance**
- **lnts50**: partly known. Gurobi solved it at tolerance 1e-4 (bound within 3.8e-5). Our rigorous 5.5e-13 closure is new as far as found; the improvement is marginal.
- **lnts100**: partly known. The PARA bound is within about 5e-5 relative; the listed best was 0.29%.
- **lnts200**: partly known, as for lnts100; the listed best was 0.43%.
- **lnts400**: partly known. The PARA bound is within about 1e-4 relative; the listed best was 0.46%.

### dtoc5

**Provenance: the MINLPLib model is a variant**
- MINLPLib: "Problem 5 in Coleman and Liao (1995)"; source QPLIB 8585 (Gould), CUTEr DTOC5; added 18 Aug 2018; N = 50000.
- The MINLPLib row is −h·u_t + y_t − y_{t+1} + 4h·y_t² = 0 (OSIL coefficient 8e-5, with h = 2e-5).
- The sources all use h·y_t²:
  - Coleman–Liao report (8 Jul 1993), Appendix Problem 5: y_{i+1} = y_i + h(y_i² − x_i);
  - DTOC5.SIF (Toint 1993): weight H = 1/N;
  - Benson's AMPL version: h*y[t]^2.
- QPLIB_8585.qplib stores the constraint Hessian as 0.00016, which is 4h under the ½xᵀQx convention. The objective is correct (h).
- Where the factor 4 entered was not determined.

**Floating-point confirmation** (checks/dtoc5_coef_check.py, damped Newton)
- The h version reproduces Coleman–Liao Table 3 (problem 5) exactly: 1.4519006 (N=10), 1.5325863 (100), 1.5347290 (500), 1.5349460 (1000).
- The 4h version with N = 50000 gives 5.389672119181, the MINLPLib value.
- The h version with N = 50000 gives about 1.53515.

**Prior results**
- Local values exist only for the h variant: Coleman–Liao Table 3; SIF SOLUTION lines (e.g. 1.531611890390 for N=5000; inexact); Smith 2011 (1.535111532 for N=5000, matching our Newton run).
- QPLIB gives only the solution value 5.38967212. QPLIB kept only instances that no complete solver solved within 120 s (Furini et al. 2019, §3.2).
- MINLPLib bounds: BARON 0.00243, COUENNE 0.00238, SCIP 0.00063, GUROBI −175.2.
- The SIF header says "The problem is convex." This is unproved and not literally true (the equality rows are nonconvex). DTOC1L, DTOC3 and DTOC6 carry the same remark, while DTOC4 says "not convex". It refers to the h variant.

**Consequence: new as far as found.** Describe the instance as the MINLPLib/QPLIB variant.

### camshape100/200/400/800

**Provenance**
- COPS 2.0 §4 (after Anitescu and Serban 1998):
  - maximize (π/n)·Σr_i;
  - convexity rows for i = 0..n+1;
  - curvature rows |r_{i+1} − r_i| ≤ αθ for i = 0..n;
  - θ = 2π/(5(n+1)), r ∈ [1, 2], α = 1.5.
- GAMS camshape.gms encodes the end rows as bounds on r_1 and r_n. It bounds rdiff only for i ≥ 2, so it **omits the curvature row on (r_1, r_2)** (d_1 is free). MINLPLib (minimizing −area) is this GAMS model, so it is a one-row relaxation of COPS 2.0.
- At our exact optimizer the omitted row is slack: |r_2 − r_1| = 3.1e-4, 7.8e-5, 2.0e-5 and 4.9e-6, against αθ = 1.87e-2, 9.4e-3, 4.7e-3 and 2.4e-3. This is a floating-point check on open-instances/logs/camshape*_envelope.npy.
- Hence our optima are also the COPS 2.0 discrete optima, up to decimal rounding of the constants.

**Local values**
- COPS 2.0 Table 4.2, LOQO: 4.28414, 4.27850, 4.27568, 4.27427 (violations ≤ 2e-12). Our areas are 4.2841471, 4.2785002, 4.2756885, 4.2742741: agreement to the printed digits.
- LANCELOT (flagged): 4.30178, 4.35538, 4.45009, 4.85693, at violations 3–5e-6. These exceed the exact optima by 0.018 to 0.58. COPS itself says the n=800 point "violates the problem constraints to an extent obvious in a graph". This is early evidence of the ill-conditioning we documented.
- COPS 3.0 Table 3.2 (p. 8): n=800 gives 4.27427 for all five solvers.
- COCONUT and Smith 2011 values are not below our optima.

**Solver bounds**
- SCIP 8.0 suite report (arXiv:2112.08872, App. A, pp. 94–95), SCIP 7/8 gaps: 7.3%/6.1%, 14.8%/13.3%, 18.6%/18.4%, 21.4%/21.6%.
- Mattick–Mutschler 2023 (Table 8, SCIP after 45 s): gaps 0.076–0.226.
- Mittelmann (26 Feb 2026): BARON, SHOT, LINDO and SCIP all exceed 7200 s on camshape100.

**camshape100**
- Bestuzheva et al., arXiv:2301.00587v1, App. B.1 (pp. 36–37): Octeract 4.5.1 solved it in 19.40 s, and its four permutations in 110.89, 97.31, 111.83 and 113.55 s. With gap limit 1e-4: 19.42 s (App. B.2, p. 49).
- In the same table, BARON (9.2–11.1%), Lindo (9.2–9.6%) and SCIP (5.2–5.6%) did not solve it in 2 h.
- Settings (§3.2, pp. 22–23): 1e-6 relative and absolute gap limits for Octeract; 1e-6 feasibility tolerance; missing bounds set to ±1e12.
- Correctness checks (§3.3, p. 23): runs inconsistent with the MINLPLib bounds were marked "nonopt". camshape100 was not flagged.
- §3.3 also states that an instance entered the test set only if some solver solved it.
- Octeract's dual value is not published. MINLPLib does not list Octeract bounds and still shows ANTIGONE −4.28415233 (rel. gap 1.2e-6).
- Consequence: **already solved globally in floating point**, and nearly closed by the listed ANTIGONE bound. The exact optimum (−4.28414712174675…, attained by an exactly feasible point and verified in rational arithmetic) is new as far as found.
- Caveat: a 1e-6-feasible incumbent can lie below the exact optimum here (SCIP's 1e-8-feasible incumbent lies 5.3e-5 below). Octeract's claim and our result therefore concern slightly different feasibility notions.

**camshape200**: best listed bound ANTIGONE −4.63229055 (8.3% gap); COPS LOQO 4.27850 (local). **New as far as found.**

**camshape400**: listed ANTIGONE −4.97265746 (16.3%); COPS 4.27568 (local); MINLPLib p2 is a tolerance artifact. **New as far as found.**

**camshape800**: listed GUROBI −5.12584096 (19.9%); COPS 2.0/3.0 4.27427 (local); p2 is a tolerance artifact. **New as far as found.**

### lukvle10

**Provenance**
- MINLPLib: Lukšan–Vlček problem 5.10 (generalized Brown function with Broyden tridiagonal constraints); source CUTEr LUKVLE10; added 06 Feb 2017; N = 1000.
- LV TR V-767 (Jan 1999), problem 5.10 (p. 25): F = Σ[(x_{2i−1}²)^(x_{2i}²+1) + (x_{2i}²)^(x_{2i−1}²+1)], c_k = (3 − 2x_{k+1})x_{k+1} + 1 − x_k − 2x_{k+2}. Their typical size is n = 1000.
- LUKVLE10.SIF (Gould 2001) is the same model (default N = 10000). Same model.

**Prior results**
- The LV report gives no values; its source paper (LV 1998, NLAA) was not accessed.
- The SIF line `*LO SOLTN 3.52237E+02` gives no N; the magnitude implies N = 1000. It is 1.0e-3 below our bound 352.2380254050784.
- IPOPT from MINLPLib point p5 with |c_j| ≤ tol (checks/lukvle10_tolerance_check.gms):

| tol | IPOPT value |
|---|---|
| 0 | 352.23803 |
| 1e-8 | 352.23802 |
| 1e-7 | 352.23799 |
| 1e-6 | 352.23762 (prints as 3.52237E+02) |
| 1e-5 | 352.23396 |

  The SIF value is therefore consistent with a 1e-6-feasible local point; its true origin is undocumented.
- MINLPLib points p1–p5 (2017–2022) are local. From the SIF start, IPOPT gives 353.12245 (= p1); CONOPT failed.
- Bounds: SCIP 351.223393 (2025), LINDO 2.11, BARON 0.051, COUENNE 6.7e-5, ANTIGONE 0. The SCIP 8 suite report shows gap ∞.

**Consequence: new as far as found.** Mention the SIF SOLTN value in the paper as a tolerance artifact.

### optcdeg2

**Provenance: the MINLPLib model is a variant**
- MINLPLib: Murtagh–Saunders 1982 Ex. 5.11; source QPLIB 8803 (Gould), CUTEr OPTCDEG2; added 18 Aug 2018; T = 50000, Δt = 4e-4.
- MINLPLib/QPLIB dynamics: v' = Δt(u − 0.02y − 0.2v²). The OSIL coefficient is 8e-5; the QPLIB Hessian is 1.6e-4.
- OPTCDEG2.SIF and Benson's AMPL version use damping 0.05 (C2 = 0.05·DT). So does OPTCNTRL.SIF, the original MS encoding (Δt = 0.2, damping 0.01 = 0.05·0.2, spring 0.004 = 0.02·0.2).
- The objective is correct (Δt/2). Murtagh–Saunders 1982 itself was not read.

**Floating-point confirmation** (IPOPT, checks/optcdeg2_coef_check.gms)
- Damping 0.05 reproduces the SIF SOLTN values: 340.6053 (T=10), 253.2756 (40), 237.2764 (100), 229.573 (400).
- Damping 0.2 at T = 50000 gives 293.8762 (MINLPLib primal 293.8760751).
- Damping 0.05 at T = 50000 gives 227.044.

**Prior results**
- Local SIF values (damping 0.05).
- QPLIB solution value 293.8760751.
- MINLPLib, 2023-04-11: GUROBI dual 292.41713458 was added together with point p2 of the same value, which has infeasibility 1e-6. This is Gurobi's tolerance-level "optimal" claim. It is false under exact feasibility: the exact optimum is 293.876075…, bracketed by us to 9e-16, which is 1.46 (0.50%) higher. The 292.417 bound itself is valid but weak.
- Other bounds: SCIP 264.42, BARON 4.40, COUENNE 0.42. SCIP 8 suite report: SCIP 7 gap 76.3%, SCIP 8 ∞.

**Consequence: new as far as found.** The only prior "global" claim is a tolerance artifact that our certificate refutes for exact feasibility. Describe the instance as "MINLPLib optcdeg2 (QPLIB 8803; damping 4 times that of CUTEst OPTCDEG2)".

### chain50/100/200/400 (hanging chain)

**Provenance**
- COPS 2.0 §3 (suggested by Mittelmann; Cesari 1983, pp. 126–127): minimize ∫x√(1+u²) subject to x' = u, ∫√(1+u²) = 4, x(0) = 1, x(1) = 3; trapezoidal rule; 2nh free variables; nh+1 rows.
- GAMS chain.gms is this model, and MINLPLib (2nh+2 variables) is its conversion. Same model.
- COPS 3.0 §4 reformulates with auxiliary states; its values agree.

**Local values**
- COPS 2.0 Table 3.2, LOQO/MINOS/SNOPT: 5.07226, 5.06978, 5.06891, 5.06862. Our optima 5.0722615, 5.0697846, 5.0689173, 5.0686217 agree to the printed (truncated) digits.
- LANCELOT: 5.07230, 5.07005, 5.06903, 5.06788, at violations 2e-6 to 9.6e-6. The nh=400 value lies 7.4e-4 below the exact optimum (tolerance artifact).
- COPS 3.0 Table 4.2 (p. 10): 5.06891 and 5.06862.
- COCONUT and Smith 2011 agree.

**Structural context**
- Griva–Vanderbei (Optim. Eng. 6 (2005) 463–482, doi:10.1007/s11081-005-2068-0; preprint §2.3) use LOQO and midpoint rules. They write that "it is apparently not possible to make a convex model when parameterizing along x", which is exactly the COPS parameterization. Relaxing the length equality gives an inequivalent model.
- Gabrys–Sremac (arXiv:2510.20917, Oct 2025): convex reformulation of the fixed-link-length chain, a different model.
- MINLPLib bounds: ANTIGONE 0.1745, 0.0937, 0.0826, 0.0956; all other solvers negative. SCIP 8 suite report: gap ∞.
- The continuous catenary's global optimality does not bound the discrete model.

**Per instance**
- chain50: COPS local value 5.07226; ANTIGONE 0.1745. **New as far as found.**
- chain100: COPS 5.06978; ANTIGONE 0.0937. **New as far as found.**
- chain200: COPS 5.06891; ANTIGONE 0.0826. **New as far as found.**
- chain400: COPS 5.06862; LANCELOT's 5.06788 is a tolerance artifact; ANTIGONE 0.0956. **New as far as found.**

### catmix100/200/400/800 (catalyst mixing)

**Provenance**
- COPS 2.0 §14 (Gunn–Thomas; von Stryk DIRCOL): x₁' = u(10x₂ − x₁), x₂' = u(x₁ − 10x₂) − (1 − u)x₂, 0 ≤ u ≤ 1; minimize −1 + x₁(1) + x₂(1); trapezoidal rule; 3(nh+1) variables.
- GAMS catmix.gms is this model with smoothing α = 0, and MINLPLib (303 variables at nh = 100) is its conversion. Same as COPS 2.0.
- COPS 3.0 switched to k = 3 collocation. Its value −4.80556e-02 belongs to a different model.

**Local values**
- COPS 2.0 Table 14.2, LOQO: −4.80694e-02, −4.80591e-02, −4.80565e-02, −4.80559e-02 (violations 1.2e-8 to 7e-8). Our optima −0.0480694320, −0.0480591456, −0.0480565478, −0.0480559013 agree to the printed digits.
- MINOS, SNOPT and LANCELOT found worse points.
- COPS notes that the value "fluctuates … probably due to the bang-singular-bang nature" and that the singular controls are non-unique (Fig. 14.1). This is consistent with the chattering we observed.
- COCONUT −0.0481; Smith 2011 catmix800 −0.048055605 (worse than our optimum).

**Solver bounds**
- MINLPLib lists only LINDO: −0.0666, −0.0725, −0.658, −1.489. The last is below the trivial bound −1.
- SCIP 8 suite report and Mattick–Mutschler: gap ∞.
- Global optimal-control methods (Esposito–Floudas; branch-and-lift, whose case study is a bioreactor; occupation measures) were not found applied to catalyst mixing or its discretization.

**Per instance**: catmix100, 200, 400, 800 are all **new as far as found**. COPS gives only local values and the listed bounds are LINDO's.

## 4. Cross-cutting points for the paper

1. **Name the models precisely.**
   - dtoc5 and optcdeg2 are QPLIB/MINLPLib variants with a 4× coefficient on the quadratic dynamics term.
   - The COPS instances are COPS 2.0 discretizations: identical to COPS 3.0 for camshape, chain and lnts, but not for catmix.
   - MINLPLib camshape drops one curvature row, which is slack at the optimum.
2. **Cite the floating-point predecessors**:
   - camshape100: Octeract in Bestuzheva et al., arXiv:2301.00587 App. B. Whether the JOGO version includes the appendix was not checked.
   - lnts: Göß–Burlacu–Martín (JOGO 2026) and Göß (arXiv 2026).

   For these instances the contribution is rigor and exactness, not first closure.
3. **Published tolerance artifacts support the exact-feasibility framing.** Each of these lies below our certified optima: LANCELOT values in COPS 2.0 (camshape, chain400, lnts100/400), the LUKVLE10 SOLTN value, and Gurobi's optcdeg2 point.
4. **Incidental notes for other tracks** (not checked): Göß 2026 Table 4 also lists powerflow0039p; JOGO 2026 Table 17 lists eg_int_s, eg_disc_s and eg_disc2_s.

## 5. Caveats

- **Novelty statements are bounded by the searches in Section 2.** Main gaps: paywalled originals, ANTIGONE per-instance results, COCONUT per-model tables, and Google Scholar full text.
- **Octeract (camshape100):** the result is a table entry; Octeract's dual value and log were not seen.
- **Göß 2026:** dual values are printed to 2 significant digits and gaps to 2 decimals in percent, so "0.00%" means < 0.005%. The PARA under-estimators are validated numerically; their validity for exact feasibility was not assessed.
- **Factor-4 discrepancy:** shown only for QPLIB 8585 and 8803. Other CUTEst-derived QPLIB/MINLPLib instances were not checked, and no public erratum was found.
- **LUKVLE10 SOLTN origin** is inferred, not documented.
- **camshape = COPS 2.0 optimum** rests on a floating-point slack check and on the verbal COPS description, not on the COPS AMPL file (that archive returned 404).

## 6. References used

- Bestuzheva, Chmiela, Müller, Serrano, Vigerske, Wegscheider. Global optimization of mixed-integer nonlinear programs with SCIP 8. JOGO 91 (2025) 287–310, doi:10.1007/s10898-023-01345-1; arXiv:2301.00587v1, §3.1–3.3 (pp. 21–23) and App. B (pp. 36–37, 49, 51, 54, 57, 59).
- Bestuzheva et al. The SCIP Optimization Suite 8.0. arXiv:2112.08872, App. A (pp. 93–103).
- Coleman, Liao. Comput. Optim. Appl. 4 (1995) 47–66, doi:10.1007/BF01299158. Report: Cornell, 8 Jul 1993, hdl:1813/5463 (Appendix Problem 5, Table 3).
- Dolan, Moré. Benchmarking optimization software with COPS. ANL/MCS-246 (Nov 2000, rev. 2 Jan 2001), https://www.mcs.anl.gov/~more/cops/bcops/bcops.html (§§3, 4, 9, 14; Tables 3.2, 4.2, 9.2, 14.2).
- Dolan, Moré, Munson. Benchmarking optimization software with COPS 3.0. ANL/MCS-TM-273 (Feb 2004), https://www.mcs.anl.gov/~more/cops/cops3.pdf (Tables 3.2 p. 8, 4.2 p. 10, 9.2 p. 22, 14.2 p. 34).
- Furini et al. QPLIB. Math. Program. Comput. 11 (2019) 237–265, doi:10.1007/s12532-018-0147-4 (§3.2); qplib.zib.de pages and files for 8585 and 8803.
- Gabrys, Sremac. arXiv:2510.20917v1 (2025).
- GAMS Model Library: camshape (SEQ=232), chain (231), catmix (242), lnts (237). GLOBALLib archive: github.com/GAMS-dev/gamsworld.
- Göß. Clash of MINLP relaxations: piecewise linear vs. global parabolic. arXiv:2603.16505v1, §4.2 (p. 17) and App. B Table 4 (p. 32).
- Göß, Burlacu, Martín. Parabolic approximation & relaxation for MINLP. JOGO 94 (2026) 951–996, doi:10.1007/s10898-026-01591-z (Table 11 p. 972, Table 17 p. 992).
- Griva, Vanderbei. Case studies in optimization: catenary problem. Optim. Eng. 6 (2005) 463–482, doi:10.1007/s11081-005-2068-0.
- Houska, Chachuat. Branch-and-lift. JOTA (2014); optimization-online preprint 3594 (case study only).
- Lukšan, Vlček. TR V-767 (1999), https://invenio.nusl.cz/record/33842 (problem 5.10, p. 25).
- Mattick, Mutschler. arXiv:2310.00112 (Table 8).
- Mevissen, Lasserre, Henrion. arXiv:1003.4608 (examples are not our problems).
- MINLPLib: instance pages (cached 2026-09-29) and bounddates.html (2026-10-01).
- Mittelmann. plato.asu.edu/ftp/minlp.html (26 Feb 2026) and compare.txt.
- Neumaier, Shcherbina, Huyer, Vinkó. Math. Program. 103 (2005) 335–356, doi:10.1007/s10107-005-0585-4. COCONUT benchmark pages.
- Smith. PhD thesis, Carleton University (2011), doi:10.22215/etd/2011-09468 (Table A.1).
- CUTEst SIF files (bitbucket.org/optrove/sif) and Benson's AMPL files (vanderbei.princeton.edu/ampl/nlmodels/cute/).

Cited but not read: Anitescu–Serban 1998; Betts–Eldersveld–Huffman 1993; Bryson–Ho 1975; Cesari 1983; Gunn–Thomas 1965; von Stryk 1999; Murtagh–Saunders 1982; Lukšan–Vlček 1998 (NLAA 5:219–247); Andrei 2013.

## Commands run (from the agent's structured return)

- `Read research files: open-instances-summary.md, open-instances/open-instances-report.md, open-instances-wave2/cops/report.md, reviews/catmix-recheck.md, prior novelty sections in reviews/open-instances-verification and reviews/cops-verification, closing-research-results.md excerpts, bound-audit/pages/*.html for the 19 instances.`
- `curl -sSL downloads, sequential with >=1 s spacing: COPS 3.0 pdf and index; COPS 2.0 HTML report pages; arXiv 2301.00587, 2112.08872, 2603.16505, 2310.00112, 2510.20917, 2202.06017, 2312.16216, 1003.4608, 2511.18580; optimization-online 7065, 3594 and the FICO paper; LV V-767 pdf; Coleman–Liao report .ps (ecommons API); CUTEst SIF files DTOC5, OPTCDEG2, LUKVLE10, OPTCNTRL, DTOC1L, DTOC3, DTOC4, DTOC6; Benson AMPL dtoc5/optcdeg2; QPLIB 8585/8803 pages and .qplib files; COCONUT benchmark pages, Library 1/2 tables and .res files; Neumaier et al. comparison pdf; GAMS-dev/gamsworld GlobalLib files via GitHub API/raw; Mittelmann minlp.html and compare.txt; MINLPLib bounddates.html and dates.html; mittelmann-plots repo pages; Griva–Vanderbei preprint; Smith 2011 thesis; GAMS presentations. Outcome: all succeeded except the COPS 3.0 zip (404) and IBM RC25385 (connection refused); Wayback CDX was offline at first and wayback/available later returned a snapshot.`
- `WebSearch (about 20 queries) and WebFetch (Wikipedia Octeract page, CONICET item); OpenAlex fulltext.search API queries for all instance names and related terms; Crossref API for DOI verification; arXiv API (timed out).`
- `Semantic Scholar snippet search: background job PID 181314 (python3 /tmp/ctl_s2/s2.py, log /tmp/ctl_s2/s2.log). All queries were rate-limited (HTTP 429); the job was killed and no results were used.`
- `pdftotext -layout, ps2pdf, and pypdf for page location; grep for instance names in all fetched papers.`
- `python3 checks/dtoc5_coef_check.py (damped Newton; first L-BFGS-B version timed out, exit 143) -> checks/dtoc5_coef_check.log. Outcome: the h version reproduces Coleman–Liao Table 3 exactly; the 4h version with N=50000 gives 5.389672119181.`
- `gams checks/optcdeg2_coef_check.gms --T={10,40,100,400,50000} --damp={0.05,0.2} --solver=ipopt (and conopt for T=40) lo=0 threads=1 -> checks/optcdeg2_coef_check.log. Outcome: damping 0.05 reproduces the SIF SOLTN values; damping 0.2 at T=50000 gives 293.8762; damping 0.05 at T=50000 gives 227.044.`
- `gams checks/lukvle10_local_check.gms --N=1000 --solver={ipopt,conopt} -> IPOPT 353.12245 (= MINLPLib p1); CONOPT failed (model status 6).`
- `gams checks/lukvle10_tolerance_check.gms --tol={0,1e-8,1e-7,1e-6,1e-5} --solver=ipopt (start point MINLPLib p5) -> 352.23803, 352.23802, 352.23799, 352.23762, 352.23396.`
- `python3 floating-point read of open-instances/logs/camshape{100,200,400,800}_envelope.npy: the omitted COPS curvature row (r1,r2) is slack by a factor of about 60 to 480.`
- `sha256sum of all stored sources -> sources/MANIFEST.md; wrote checks/README.md.`
- `No project-wide checks, no CI inspection, no git commits.`

## Open issues (from the agent's structured return)

- report.md was NOT written: the harness blocked report files for this subagent. The full report text is in this structured output's summary field; the integration step should save it to /workspace/minlp-notes/research-20260929/publication/literature/control/report.md.
- Novelty is limited to what was searched. Not accessed: Google Scholar full text and paywalled originals (Murtagh–Saunders 1982, Lukšan–Vlček 1998 NLAA, Anitescu–Serban 1998, Betts et al. 1993, Gunn–Thomas 1965, von Stryk 1999, Andrei 2013), ANTIGONE 2014 per-instance results, and the COCONUT per-model solver tables (cited online in 2005, not retrievable). Semantic Scholar was rate-limited; IBM RC25385 was unreachable.
- camshape100 Octeract result: only the table entry and settings in arXiv:2301.00587 were seen; Octeract's dual value and log are not published. It is unknown whether the JOGO (2025) version contains the appendix.
- lnts: the Göß 2026 PARA dual bounds are printed to 2 significant digits, with gaps to 2 decimals in percent. The PARA under-estimators are validated numerically; their validity for exact feasibility was not assessed.
- The factor-4 coefficient discrepancy (dtoc5, optcdeg2) is shown only for QPLIB 8585/8803; where it arose (CUTEst-to-QPLIB conversion or elsewhere) was not determined, and other CUTEst-derived QPLIB/MINLPLib instances were not checked. No public erratum was found.
- The origin of the LUKVLE10.SIF SOLTN value 352.237 is inferred from the 1e-6 tolerance experiment, not documented.
- The claim that our camshape optima equal the COPS 2.0 discrete optima rests on a floating-point slack check and on COPS's verbal description, not on the COPS AMPL file (the COPS 3.0 zip returned 404).
- Incidental items for other tracks, not checked: Göß 2026 Table 4 lists powerflow0039p; JOGO 2026 Table 17 lists eg_int_s, eg_disc_s and eg_disc2_s.
