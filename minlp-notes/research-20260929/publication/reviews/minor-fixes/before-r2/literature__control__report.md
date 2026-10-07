<!-- Written to disk by the root from the structured return value of fixer round 1 of track lit-control in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Literature check: optimal control and CUTE-type instances (lit-control)

Date: 2026-10-01; revised 2026-10-02 after review round 1 (see Section 7), and 2026-10-03 after review round 2 (Response to review).

**Scope.** lnts50/100/200/400, dtoc5, camshape100/200/400/800, lukvle10, optcdeg2, chain50/100/200/400 and catmix100/200/400/800. Our claims are those of open-instances-summary.md; all 19 instances are in its "closed" table.

**Where the material is.**
- Sources are in `publication/literature/control/sources/`. `MANIFEST.md` lists each with its URL, fetch date and sha256. Files added in revision 1 are in its last table.
- Provenance checks are in `publication/literature/control/checks/`; `README.md` describes them. They use floating-point or decimal data and are evidence, not proofs.

**Terms used below.**
- **Rigorous certificate:** a bound proved with exact or outward-rounded arithmetic.
- **Floating-point claim:** a solver reports a gap within its tolerance, usually with a feasibility tolerance near 1e-6.
- **Local value:** the result of a local NLP solver.
- **Tolerance artifact:** a reported "optimal" or feasible value that lies below a certified lower bound. Such a value is attainable only within the solver's feasibility tolerance.

## 1. Bottom line

**Count:** 10 of 19 instances are new as far as found. For 1 (camshape800), a published global claim exists and is false. 7 are partly known. 1 (camshape100) was already solved globally in floating point.

**New as far as found (10): camshape400, lukvle10, chain50–400, catmix100–800.**
- I found no prior global result for these, rigorous or floating-point, beyond weak solver bounds (MINLPLib, Mittelmann logs, SCIP reports).

**camshape800: a published global claim exists, and our certificate contradicts it.**
- Mittelmann's Continuous Non-Convex QPLIB Benchmark lists MINOTAUR as solving QPLIB_3177 in every version from 3 Dec 2021 to 17 May 2026. QPLIB_3177 is the MINLPLib model with constants rounded at the 1e-10 level.
- The 2026 log reports "Optimal solution found" with value −4.2774. That is 3.1e-3 below our certified optimum −4.27427414195420, so the claim is false.
- Our certificate is for the MINLPLib model, so for the QPLIB copy this is strong evidence, not proof (Section 3, Mittelmann).
- Ours is the first correct global result as far as found.

**Partly known, floating point (7).**
- **lnts50–400.**
  - Gurobi solved lnts50 to its default tolerance: Göß, Burlacu, Martín, J. Global Optim. 94 (2026) 951–996, doi:10.1007/s10898-026-01591-z, Table 17, p. 992.
  - Göß, arXiv:2603.16505v1, App. B, Table 4, p. 32, prints PARA dual-bound gaps of 0.00% (lnts50/100/200) and 0.01% (lnts400).
  - Our rigorous closure to 5.5e-13 is new as far as found.
- **dtoc5.**
  - MINOTAUR 0.4.1 reports "Optimal solution found", value 5.3897, on QPLIB_8585 after 1005 s (Mittelmann, 17 May 2026). QPLIB_8585 is textually identical to MINLPLib dtoc5.
  - The value agrees with our certified optimum 5.38967211918114. However, the log warns that default bounds were assumed for 99983 (lower) and 99997 (upper) of the 99999 variables.
  - On the source model (coefficient h instead of 4h, M = 600–1000), Waki, Kim, Kojima and Muramatsu (SIAM J. Optim. 17 (2006) 218–242) found the order-1 sparse SDP relaxation numerically tight.
  - Ours is the first rigorous certificate.
- **optcdeg2.**
  - MINOTAUR 0.2.1 was listed as solving QPLIB_8803 in 1641 s (Mittelmann, 3 Dec 2021). QPLIB_8803 is identical to MINLPLib optcdeg2. The value and log are no longer available.
  - Gurobi's 292.417 "optimum" on MINLPLib is a tolerance artifact.
  - MINOTAUR 0.4.1 (2026) reports "Detected infeasibility". That is false, since the model has a rigorously feasible point.
  - Ours is the first rigorous certificate.
- **camshape200.**
  - Octeract 4.5.1 was listed as solving QPLIB_2480 (the rounded copy) in 6853 s (Mittelmann, 7 Jan 2023). The value and log are not available. No later table lists this instance as solved.
  - Ours is the first certified optimum.

**Already solved globally in floating point (1): camshape100.**
- Octeract 4.5.1 solved camshape100 in 19.40 s: Bestuzheva et al., arXiv:2301.00587v1 (JOGO 91 (2025) 287–310), App. B.1, pp. 36–37. Settings: 1e-6 relative and absolute gap; 1e-6 feasibility tolerance.
- On the QPLIB copy (QPLIB_2738), Mittelmann's benchmark lists Octeract (2021–2024) and ANTIGONE (2021–2026) as solving it.
- ANTIGONE's 2026 "Global minimum" value −4.284302 is a tolerance artifact: it is 1.55e-4 below the exact optimum, and CONOPT reports 8.7007237331E-06 in its aggregate "Infeasibility" column for the input point. The log does not identify that point as ANTIGONE's incumbent, although that is the natural reading.
- New for camshape100 is only the exact optimum, verified in rational arithmetic.

**dtoc5 and optcdeg2 are variants of their published sources.** Both came into MINLPLib through QPLIB (8585, 8803), and the MINLPLib files are textually identical to the QPLIB files. In both, the quadratic term in the dynamics is 4 times the coefficient in CUTEst:
- **dtoc5:** 4h·y² instead of h·y², which is the form in Coleman–Liao problem 5 and DTOC5.SIF.
- **optcdeg2:** damping 0.2 instead of 0.05, the value in OPTCDEG2.SIF and in OPTCNTRL.SIF, CUTEst's encoding of Murtagh–Saunders Ex. 5.11. Murtagh–Saunders 1982 itself was not read.

Our certificates hold for the MINLPLib models as written. Published DTOC5/OPTCDEG2 values belong to different models.

**Published values below our certified bounds (tolerance artifacts).** These support the exact-feasibility framing; details are in Section 4, point 3:
- LANCELOT values in COPS 2.0;
- the CUTEst LUKVLE10 SOLTN value;
- the DTOC5.SIF SOLUTION lines (an h-variant analogue);
- Gurobi's optcdeg2 point;
- MINOTAUR's camshape800 claim and ANTIGONE's camshape100 "global minimum";
- several BARON, COPT and SCIP incumbents in Mittelmann's 2025–2026 logs.

**COPS models.**
- MINLPLib chain, camshape, catmix and lnts are the GAMS translations of COPS 2.0. COPS gives local values only and never claims global optimality for these four problems.
- COPS 3.0 catmix uses 3-stage collocation, so it is a different model.

### Summary table

| instance | provenance | strongest prior result | consequence |
|---|---|---|---|
| lnts50 | GAMS `lnts` = COPS 2.0 #9, nh=50; same model | Gurobi solved it to default tolerance (JOGO 2026, Table 17); MINLPLib GUROBI bound 0.55464755 (rel. gap 3.8e-5); PARA gap "0.00%" | partly known (floating point); rigorous closure new as far as found |
| lnts100 | same, nh=100 | PARA dual bound, gap "0.00%" (<5e-5 rel.), Göß 2026 Table 4 | partly known (floating point) |
| lnts200 | same, nh=200 | PARA gap "0.00%" | partly known (floating point) |
| lnts400 | same, nh=400 | PARA gap "0.01%" | partly known (floating point) |
| dtoc5 | QPLIB_8585 (identical file) ← CUTEst DTOC5 ← Coleman–Liao problem 5; N=50000; variant (4h·y²) | MINOTAUR 0.4.1 "optimal" 5.3897 on QPLIB_8585 (Mittelmann 2026; default bounds assumed for ~1e5 variables), value agrees with ours; source model (h·y², M = 600–1000): order-1 SDP numerically tight (Waki et al. 2006); local values | partly known (floating point); first rigorous certificate |
| camshape100 | GAMS `camshape` = COPS 2.0 #4; omits one COPS curvature row (slack at the optimum); QPLIB_2738 = this model with constants rounded at ~1e-10 | Octeract 4.5.1 solved to 1e-6 gap (Bestuzheva et al.); Octeract and ANTIGONE on QPLIB_2738 (Mittelmann 2021–2026), ANTIGONE's value a tolerance artifact; MINLPLib ANTIGONE bound within 1.2e-6 | already solved globally in floating point; exact optimum new |
| camshape200 | same, n=200; QPLIB_2480 (rounded copy) | Octeract 4.5.1 listed as solving QPLIB_2480 in 6853 s (Mittelmann, 7 Jan 2023; value and log unavailable); MINLPLib ANTIGONE −4.63229 | partly known (an unverifiable floating-point claim); first certified optimum |
| camshape400 | same, n=400; QPLIB_2703 (rounded copy) | never listed as solved; ANTIGONE −4.97266 (MINLPLib), −4.969835 on QPLIB copy; SCIP 9.2.1 incumbent −4.33024 (tolerance artifact) | new as far as found |
| camshape800 | same, n=800; QPLIB_3177 (rounded copy) | MINOTAUR claims optimality for QPLIB_3177 (2021–2026); 2026 value −4.2774 is 3.1e-3 below our certified optimum (false claim) | prior global claim false; first correct global result as far as found |
| lukvle10 | CUTEst LUKVLE10 = Lukšan–Vlček problem 5.10, N=1000; same model | SCIP bound 351.223; SIF SOLTN 352.237 (tolerance artifact) | new as far as found |
| optcdeg2 | QPLIB_8803 (identical file) ← CUTEst OPTCDEG2 ← Murtagh–Saunders Ex. 5.11 (per OPTCNTRL.SIF), T=50000; variant (damping 0.2) | MINOTAUR 0.2.1 listed as solving QPLIB_8803 in 1641 s (Mittelmann, 3 Dec 2021; value unavailable); Gurobi "optimal" 292.417 (tolerance artifact); MINOTAUR 0.4.1 false "infeasible" | partly known (an unverifiable floating-point claim); first rigorous certificate |
| chain50–400 | GAMS `chain` = COPS 2.0 #3; same model | COPS 2.0/3.0 local values; ANTIGONE bounds ≈ 0.08–0.17 | new as far as found |
| catmix100–800 | GAMS `catmix` = COPS 2.0 #14 (trapezoidal); not the COPS 3.0 model | COPS 2.0 LOQO local values; LINDO bounds only | new as far as found |

## 2. What was searched

**Primary sources read**
- COPS 2.0 (HTML, ANL/MCS-246) and COPS 3.0 (ANL/MCS-TM-273).
- GAMS library sources for camshape, chain, catmix and lnts (GAMS 54.3).
- CUTEst SIF files DTOC5, OPTCDEG2, OPTCNTRL and LUKVLE10, and Benson's AMPL versions.
- Coleman–Liao technical report (1993); Lukšan–Vlček V-767 (1999).
- QPLIB pages and files for 8585 and 8803. In revision 1 also: the QPLIB pages, .gms and .sol files for 2738, 2480, 2703 and 3177; `qplib.solu`; the QPLIB instance listing.
- GLOBALLib archive (GAMS-dev/gamsworld on GitHub).
- COCONUT Library 1/2 tables and .res files.
- MINLPLib pages (cached) and bounddates.html. In revision 1 also the MINLPLib .gms files for camshape100–800, dtoc5 and optcdeg2.
- Mittelmann's MINLP benchmark: current page and compare.txt.
- **Revision 1: Mittelmann's Continuous Non-Convex QPLIB Benchmark.**
  - https://plato.asu.edu/ftp/cnconv.html, version of 17 May 2026.
  - 30 logs: ANTIGONE, BARON, COPT, MINOTAUR and SCIP for QPLIB 2738, 2480, 2703, 3177, 8585 and 8803.
  - 7 Wayback snapshots, with page dates 3 Dec 2021, 7 Jan 2023, 9 Mar 2024, 21 Aug 2024, 4 Apr 2025, 11 Jul 2025 and 28 Sep 2025.
  - Wayback CDX for the log directory: no old logs archived.
  - Mittelmann's benchmark index (bench.html): the other QPLIB pages are discrete, binary or convex, so cnconv is the relevant one.
- **Revision 1: ANTIGONE 1.0 Test Suite** (Misener and Floudas, 1 May 2013) and **GloMIQO 2.0 Test Set** (8 Jul 2012), both from the Wayback copies of helios.princeton.edu.

**Papers read or grepped for the instance names**
- Bestuzheva et al. 2023 (SCIP 8 MINLP); SCIP Optimization Suite 8.0 and 10.0 reports.
- Göß 2026 (arXiv) and Göß–Burlacu–Martín 2026 (JOGO).
- Neumaier–Shcherbina–Huyer–Vinkó 2005.
- Griva–Vanderbei 2005 (preprint) and Gabrys–Sremac 2025.
- Houska–Chachuat branch-and-lift (preprint); Mevissen–Lasserre–Henrion 2010.
- Mattick–Mutschler 2023; Smith 2011 PhD thesis.
- Bertsimas–Öztürk (arXiv:2202.06017); FICO Xpress Global 2025.
- QPLIB paper (Furini et al. 2019; preprint re-read in revision 1 for §3.2); GAMS GLOBALLib presentations.
- Revision 1:
  - Waki–Kim–Kojima–Muramatsu (preprint B-411, Feb 2005);
  - Müller et al. 2019 (arXiv:1912.00356);
  - arXiv:2603.09864, 2410.03720 and 2106.13721, all of which use QPLIB. None mentions our QPLIB IDs or instance names.

**Web searches** (instance names and topics)
- Instance names; camshape with global solvers.
- Catalyst mixing global optimization; linear tangent steering global optimality; discretized hanging chain global minimum.
- QPLIB/CUTEst conversion errors; Octeract and open MINLPLib instances.
- Occupation-measure and moment-SOS bounds; SparsePOP and Lukšan–Vlček.
- Esposito–Floudas, Chachuat, Stadtherr and Barton global dynamic optimization.
- Revision 1: GloMIQO with camshape/catmix; "QPLIB_3177" / "QPLIB_2738" / "QPLIB_8585" / "QPLIB_8803". The latter gave no instance-level hits.

**OpenAlex full-text search**
- All instance names, QPLIB_8585, QPLIB_8803, "COPS camshape" and "COPS catmix". New hits: Smith 2011, Mattick–Mutschler 2023 and Göß 2026.
- Revision 1: QPLIB_2738, _2480, _2703, _3177, _8585 and _8803, with and without the underscore: 0 hits each.

**Failed attempts**
- Semantic Scholar snippet search: HTTP 429 on every query; abandoned.
- Internet Archive was offline at first. The archived 2023 Mittelmann compare.txt did not include camshape100.
- COCONUT per-model solver tables: cited online in 2005 but not retrievable.
- IBM report RC25385: connection refused. COPS 3.0 AMPL zip: 404.
- Revision 1: GloMIQO paper (Springer is closed access; OpenAlex reports no OA copy; CORE returned a Cloudflare challenge). Octeract and MINOTAUR 0.2.1–0.4.0 logs of Mittelmann's benchmark: not online and not archived.

**Not read** (paywall or no access)
- Murtagh–Saunders 1982; Lukšan–Vlček 1998 (NLAA); Anitescu–Serban 1998; Betts et al. 1993; Gunn–Thomas 1965; von Stryk 1999.
- Andrei 2013 (NOA book); Esposito–Floudas 2000.
- GloMIQO paper (Misener, Floudas, JOGO 57 (2013) 3–50, doi:10.1007/s10898-012-9874-7) and ANTIGONE paper (JOGO 59 (2014) 503–526, doi:10.1007/s10898-014-0166-2): per-instance results not seen. Details are in Section 3 (COPS family).
- The published SIAM version of Waki et al. (the preprint was used).

**Scope of these searches**
- An unsuccessful search does not establish novelty. Google Scholar and paywalled full text were not available.
- The global optimal-control literature I found (branch-and-lift, occupation measures, Esposito–Floudas) treats continuous-time problems. Waki et al. (2006) is the only work found that treats one of these discrete models (the DTOC5 source model) with a global method.

## 3. Per-instance findings

### Mittelmann's Continuous Non-Convex QPLIB Benchmark (affects dtoc5, optcdeg2, camshape)

Added in revision 1. Sources are in `sources/mittelmann_cnconv/`. Value differences are in `checks/mittelmann_values_vs_certified.log`.

**The benchmark**
- Page: https://plato.asu.edu/ftp/cnconv.html, version of 17 May 2026. Solvers: BARON 25.12.10, ANTIGONE 1.1, SCIP 10.0.1, MINOTAUR 0.4.1, COPT 8.0.4.
- Setup: 102 continuous non-convex QPLIB instances; 3 h limit; 8 threads.
- The header says "All problems were solved GLOBALLY" and lists only instances that at least one solver solved. This sentence first appears in the 7 Jan 2023 version; the 3 Dec 2021 version says only "at least one solver succeeded".
- The stored SCIP logs (dated 4 Apr 2025) are from SCIP 9.2.1, not the 10.0.1 named in the header.

**Which QPLIB instances are ours**
- QPLIB_8585 and QPLIB_8803 are MINLPLib dtoc5 and optcdeg2. With comment lines removed, the MINLPLib and QPLIB .gms files differ only in the solve statement. The QPLIB_8803 file also has a redundant "Positive Variables" line for two variables that both files fix at 0 (`checks/qplib_dtoc5_optcdeg2_identity.log`).
- QPLIB_2738, 2480, 2703 and 3177 (type LCQ, donor Ruth Misener) are camshape100, 200, 400 and 800 with constants rounded to 8–10 digits.
  - My exact-rational comparison (`checks/qplib_camshape_compare.py`) matches every row of each pair by monomial support and sense.
  - The largest relative coefficient difference is 2.3e-10 and the largest relative bound difference 4.7e-10 (4.708e-10 before display rounding, at camshape400 x1.up).
  - For camshape100: MINLPLib point p1 (−4.2841471217467) violates the QPLIB model by 3.0e-10. QPLIB's point (−4.2841462678) satisfies both models to 2e-14 (objective-defining row excluded).
- No catmix copy was found in QPLIB (a scan of the QPLIB listing by size; evidence only). chain, lnts and lukvle10 are not quadratic, so they cannot be in QPLIB.

**What the tables and logs show**

| QPLIB (MINLPLib) | listed as solved by (page version) | what the available log shows |
|---|---|---|
| 2738 (camshape100) | ANTIGONE 1857 s (Dec 2021, Jan 2023, Mar 2024), 744 s (Aug 2024–Sep 2025), 852 s (May 2026); OCTERACT 3.6.0 37 s (Dec 2021), 4.5.1 8 s (Jan 2023), 4.7.1 17 s (Mar 2024) | ANTIGONE 2026: "Termination Status: Global minimum", best feasible = best possible = −4.284302, relative gap 1e-9, OptCR 0. CONOPT then reports aggregate Infeasibility 8.7007237331E-06 for its input point and polishes it to −4.28414626579. The input is naturally read as ANTIGONE's incumbent but the log does not state that identity; this is not necessarily the largest row violation. −4.284302 is 1.55e-4 below the exact optimum −4.28414712174675. Octeract logs: not available. |
| 2480 (camshape200) | OCTERACT 4.5.1 6853 s (Jan 2023 only) | log not available; value unknown. ANTIGONE 2026 timed out with bound −4.601964 (stronger than MINLPLib's −4.63229055; floating point, rounded copy). |
| 2703 (camshape400) | never listed | ANTIGONE 2026 bound −4.969835 (MINLPLib −4.97265746). SCIP 9.2.1 primal −4.33023953971002, 5.5e-2 below our optimum (tolerance artifact). |
| 3177 (camshape800) | MINOTAUR 0.2.1 19 s (Dec 2021), 0.3.0 5 s (Jan 2023), 0.4.0 16 s (Mar 2024) and 6 s (Aug 2024), 0.4.1 3 s (Apr 2025–May 2026) | MINOTAUR 2026: "Optimal solution found", best value −4.2774, one node, LB = inf. That is 3.13e-3 below our certified −4.27427414195420. The claim is false. |
| 8585 (dtoc5) | MINOTAUR 0.4.1 1005 s (May 2026 only) | "Optimal solution found", value 5.3897, LB = inf after the root. The log warns "Default lower bound was assumed for 99983 variables" and "Default upper bound was assumed for 99997 variables"; the log does not state the values; master source implies [−100,100], with a benchmark-revision caveat. The value agrees with our certified 5.38967211918114. |
| 8803 (optcdeg2) | MINOTAUR 0.2.1 1641 s (Dec 2021 only) | 2021 log not available; value unknown. MINOTAUR 0.4.1 (2026): "status of presolve: Detected infeasibility". That is false: QPLIB's own point has infeasibility 1.75e-15, and the identical MINLPLib model has a rigorously feasible point (open-instances-summary.md). |

**Rigour of the camshape800 refutation**
- "False" here means incompatible with exact feasibility for the certified MINLPLib model. A reported tolerance-feasible value can lie below the exact optimum; ANTIGONE's camshape100 value is another example. For rounded QPLIB_3177, the evidence is strong but the MINLPLib certificate alone is not a rigorous refutation.
- For MINLPLib camshape800, no exactly feasible point has value below −4.27427414195420 (our certificate).
- QPLIB_3177 differs by rounding at the 2e-10 relative level. A rigorous refutation for the copy would need our certificate applied to the rounded constants; I did not do this.
- The MINOTAUR 0.4.1 log provides stronger evidence of a solver error: QPLIB_3177 closes at the root (1 node, 2.89 s), with the remaining-node bound reported as +∞. On the smaller copies the same version reaches its 10800 s limit with bounds −4.5374 (2738), −4.8494 (2480) and −5.1678 (2703), and gaps 5.9%, 13.3% and 20.8%. Root closure on the largest copy is therefore not credible. A tolerance-feasible value by itself is still possible: COPT's incumbent −4.277371 has quadratic violation 2.98e-8 (r2 evidence). The observed sensitivity makes a 3.1e-3 shift implausible. MINLPLib point p1 violates the QPLIB model by only about 5e-10, and BARON's QPLIB_2738 incumbent is within 1.9e-8 of our MINLPLib camshape100 optimum.
- MINLPLib point p1 also violates MINLPLib camshape800 itself by 3.9e-10 at e1562, so it is not the exactly feasible optimizer. The QPLIB reference points for 2480 and 2703 violate MINLPLib's r1 upper bound by 2.481e-11 and 4.7078e-10, respectively (`checks/minor_review_check.log`).
- Whether the rounding moves the camshape optimum at all, for example by the 8.5e-7 separating QPLIB's reference point from ours, was not determined. QPLIB's point is feasible in the MINLPLib model to 1e-14, so it may simply be slightly suboptimal.

**Other values in the 2026 logs** (differences from our certified optima; floating point; camshape on the rounded copies)
- BARON incumbents:
  - dtoc5: 5.38966688447816 (5.2e-6 below);
  - optcdeg2: 293.876075074557 (2.1e-8 below);
  - camshape800: −4.51546318707998 (0.24 below).
- COPT incumbents for camshape100/200/400/800: 4.3e-5, 1.8e-4, 7.4e-4 and 3.1e-3 below.
- All of these are tolerance artifacts.
- Dual bounds:
  - COPT's dtoc5 bound 0.761858 is stronger than MINLPLib's best listed bound (BARON 0.00243).
  - COPT's optcdeg2 bound 283.41 is weaker than MINLPLib's GUROBI 292.417.

### Family: COPS models (lnts, camshape, chain, catmix)

**MINLPLib and GLOBALLib**
- The MINLPLib pages say "Source: GAMS Model Library model <name>, COPS". The instances were added 31 Jul 2001.
- They were GLOBALLib models; the GLOBALLib scalar files are dated 07/30/01. GLOBALLib stored no solution points and made no optimality claim.
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

**ANTIGONE and GloMIQO test suites** (revision 1)
- ANTIGONE 1.0 Test Suite (Misener and Floudas, 1 May 2013), Table 4 (344 GLOBALLib case studies), PDF p. 21: lists camshape100–800, catmix100–800 and chain50–400 with their sizes. lnts is excluded because it contains trigonometric functions.
- The document gives no per-instance results. The ANTIGONE paper (JOGO 59 (2014) 503–526) was not read. These runs are a likely origin of MINLPLib's ANTIGONE bounds.
- The GloMIQO 2.0 Test Set (8 Jul 2012) counts "187 GLOBALLib Test Cases" but does not list them by name. Whether the GloMIQO paper (JOGO 57 (2013) 3–50) includes camshape or catmix, and with what result, is unknown; it was not accessible.
- Ruth Misener later donated the QPLIB camshape copies.

**Smith (2011) thesis, Table A.1**
- Gives heuristic values for COCONUT versions. Where comparable they are consistent with ours, e.g. chain50 5.072261494.
- The lnts50 −339.2, lnts400 −1255.1 and optcdeg2 0.009 entries are impossible for the MINLPLib models (the lnts objective is N·h ≥ 0). They come from different translations and are not comparable.

**Müller et al. 2019** (arXiv:1912.00356v1, surrogate duality; revision 1)
- Weak surrogate dual bounds, e.g. camshape100 −4.908 (Table 4, PDF p. 40; camshape200–800 are on p. 41) and lnts50 0.511 (PDF p. 46). Not a global result.
- Their "best primal" for camshape800, −4.27431, lies 3.6e-5 below our certified optimum. It is evidently the MINLPLib tolerance-artifact point of the time.
- Citing it is optional.

**MINLPLib bound history** (bounddates.html)
- Primal points date from 2014-08-15; camshape400/800 points p2 from 2018-05-22.
- Dual bounds were added 2014–2025, the latest from GUROBI on 2025-07-31 and 2025-08-07.
- No instance is marked solved (site update 2026-09-14).

### lnts50/100/200/400 (particle steering)

**Provenance**
- COPS 2.0 §9: minimize time; a = 100; |u| ≤ π/2; terminal y₂ = 5, ẏ₁ = 45, ẏ₂ = 0; trapezoidal rule.
- Boundary data come from Betts et al. (1993); the classical problem is in Bryson and Ho (1975), pp. 59–62.
- MINLPLib is the GAMS conversion: bounds ±1.5707963267949, objective N·h; lnts50 has 256 variables = 5(nh+1)+1, as in COPS. Same model.
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
- **lnts50:** partly known. Gurobi solved it at tolerance 1e-4 (bound within 3.8e-5). Our rigorous 5.5e-13 closure is new as far as found; the improvement is marginal.
- **lnts100:** partly known. The PARA bound is within about 5e-5 relative; the listed best was 0.29%.
- **lnts200:** partly known, as for lnts100; the listed best was 0.43%.
- **lnts400:** partly known. The PARA bound is within about 1e-4 relative; the listed best was 0.46%.

### dtoc5

**Provenance: the MINLPLib model is a variant**
- MINLPLib: "Problem 5 in Coleman and Liao (1995)"; source QPLIB 8585 (Gould), CUTEr DTOC5; added 18 Aug 2018; N = 50000. The MINLPLib .gms file is textually identical to QPLIB_8585.gms (revision 1 check).
- The MINLPLib row is −h·u_t + y_t − y_{t+1} + 4h·y_t² = 0 (OSIL coefficient 8e-5, with h = 2e-5).
- The sources all use h·y_t²:
  - Coleman–Liao report (8 Jul 1993), Appendix Problem 5: min h·Σ_{i=1}^{N−1}(y_i² + x_i²) s.t. y_{i+1} = y_i + h(y_i² − x_i);
  - DTOC5.SIF (Toint 1993): weight H = 1/N;
  - Benson's AMPL version: h*y[t]^2.
- QPLIB_8585.qplib stores the constraint Hessian as 0.00016, which is 4h under the ½xᵀQx convention. The objective is correct (h).
- Where the factor 4 entered was not determined.

**Floating-point confirmation** (checks/dtoc5_coef_check.py, damped Newton)
- The h version reproduces Coleman–Liao Table 3 (problem 5) exactly: 1.4519006 (N=10), 1.5325863 (100), 1.5347290 (500), 1.5349460 (1000).
- The 4h version with N = 50000 gives 5.389672119181, the MINLPLib value.
- The h version with N = 50000 gives about 1.53515.

**Prior global results**
- **MINOTAUR on the instance itself (QPLIB_8585).** Mittelmann's benchmark, 17 May 2026: MINOTAUR 0.4.1 reports "Optimal solution found", value 5.3897, in 1005 s.
  - It assumed default lower bounds for 99983 and default upper bounds for 99997 of the 99999 variables. The claim therefore concerns an artificially bounded box, and it is a floating-point claim. The master-source rule in `QuadHandler::addDefaultBounds` scales the largest applicable finite bound magnitude by 100 (or uses ±1000 when none exists). For QPLIB_8585's sole finite bound x50001 = 1, this gives [−100, 100]. Re-fetching the QPLIB reference point matched the r2 SHA-256 and confirmed max |x| = 8.057243524908399, within that box (`checks/dtoc5_reference_check.log`). The benchmarked revision v0.4-50-g456fd8cc may differ from the saved master source, so the inference does not prove which default values that run used. Its one-node closure is plausible because our convex Lagrangian relaxation is exact to the certified precision.
  - Its value agrees with our certified optimum to the printed digits.
  - No other solver in this benchmark or on MINLPLib closed the gap: BARON bound 2e-5, SCIP 2e-5, COPT 0.7619.
- **Waki, Kim, Kojima and Muramatsu on the source model (h·y²).** "Sums of squares and semidefinite program relaxations for polynomial optimization problems with structured sparsity", SIAM J. Optim. 17(1) (2006) 218–242, doi:10.1137/050623802. Preprint: Research Report B-411, Tokyo Tech, Oct 2004, rev. Feb 2005, https://optimization-online.org/wp-content/uploads/2004/10/988.pdf. Locations below are printed pages of the preprint.
  - Problem (39), p. 30: "the second problem (5 of [3])", with [3] = Coleman–Liao. It reads min (1/M)·Σ_{i=1}^{M−1}(y_i² + x_i²) s.t. y_{i+1} = y_i + (1/M)(y_i² − x_i), y_1 = 1. This is Coleman–Liao problem 5 with N = M.
  - Table 12, p. 31: the sparse SDP relaxation of order 1 gives approximate optimal solutions for M = 600, 700, 800, 900 and 1000 (n = 1198 to 1998).
    - ε_obj values: 3.4e-8, 2.5e-8, 5.9e-8, 1.4e-7, 6.3e-8.
    - ε_feas values: −2.2e-10, −8.1e-10, −1.6e-10, −6.8e-10 and −2.7e-10; the range is −1.6e-10 to −8.1e-10.
    - CPU times: 3.3–5.0 s.
  - The authors state (p. 31) that for this problem the sparse relaxation is guaranteed to give bounds of the same quality as the dense one.
  - **Caveats.**
    - These are SeDuMi floating-point results. The objective carries a random perturbation pᵀx with |p_j| < 1e-5 (pp. 21–22).
    - ε_obj is the relative difference between the SDP value and the perturbed objective at the extracted point.
    - Table 12 prints no objective values.
    - Section 6.2 (p. 26) describes added variable bounds and a κ = 1e-5 relaxation of equalities for the problems of Tables 7–8. Whether these were also used for problem (39) is not stated.
  - **Relevance.**
    - For a quadratic problem, the order-1 relaxation is the Shor SDP relaxation, which is closely related to the Lagrangian dual bound.
    - Waki et al.'s result is therefore numerical evidence of a zero relaxation gap on the h variant for M = 600–1000. That is the same phenomenon our certificate ("Lagrangian convex at the costate") proves for the 4h variant at N = 50000.
    - The paper should cite it as prior global work on the source model.
- **Local values for the h variant:** Coleman–Liao Table 3 and Smith 2011 (1.535111532 for N=5000, matching our Newton run).
- **DTOC5.SIF SOLUTION lines.** Each lies below the converged local value of the h model:
  - N=10: 1.451893900588 vs 1.4519006 (6.7e-6 below);
  - N=100: 1.532552633518 vs 1.5325863 (3.4e-5 below);
  - N=500: 1.530860973890 vs 1.5347290 (3.9e-3 below);
  - N=1000: 1.527434119271 vs 1.5349460 (7.5e-3 below);
  - N=5000: 1.531611890390 vs 1.5351115 (3.5e-3 below).

  At N=1000 Waki et al.'s results indicate that the local value is the global value, so these lines are not valid optimal values for exactly feasible points. They are tolerance artifacts or come from a different version of the model.
- **QPLIB** gives only the solution value 5.38967212. QPLIB's selection (Furini et al. 2019, preprint §3.2, p. 18) has two steps:
  - First, it discarded instances solved by at least 30% of the complete solvers within 30 s.
  - Then it discarded instances that one complete solver solved to proven optimality within 120 s.
- **MINLPLib bounds:** BARON 0.00243, COUENNE 0.00238, SCIP 0.00063, GUROBI −175.2.
- **The SIF header** says "The problem is convex." This is unproved and not literally true (the equality rows are nonconvex). DTOC1L, DTOC3 and DTOC6 carry the same remark, while DTOC4 says "not convex". The remark refers to the h variant.

**Consequence: partly known (floating point); ours is the first rigorous certificate.**
- MINOTAUR's claim on the identical QPLIB_8585 depends on assumed default bounds.
- Waki et al.'s global SDP evidence concerns the h variant at M = 600–1000.
- Describe the instance as the MINLPLib/QPLIB variant.

### camshape100/200/400/800

**Provenance**
- COPS 2.0 §4 (after Anitescu and Serban 1998):
  - maximize (π/n)·Σr_i;
  - convexity rows for i = 0..n+1;
  - curvature rows |r_{i+1} − r_i| ≤ αθ for i = 0..n;
  - θ = 2π/(5(n+1)), r ∈ [1, 2], α = 1.5.
- GAMS camshape.gms encodes the end rows as bounds on r_1 and r_n. It bounds rdiff only for i ≥ 2, so it **omits the curvature row on (r_1, r_2)** (d_1 is free). MINLPLib (minimizing −area) is this GAMS model, so it is a one-row relaxation of COPS 2.0.
- At our exact optimizer the omitted row is slack: |r_2 − r_1| = 3.1e-4, 7.8e-5, 2.0e-5 and 4.9e-6, against αθ = 1.87e-2, 9.4e-3, 4.7e-3 and 2.4e-3. This is a floating-point check on open-instances/logs/camshape*_envelope.npy, independently reproduced by the round-1 reviewer.
- Hence our optima are also the COPS 2.0 discrete optima, up to decimal rounding of the constants.
- QPLIB_2738, 2480, 2703 and 3177 are the MINLPLib models with constants rounded to 8–10 digits (see the Mittelmann section above).

**Local values**
- COPS 2.0 Table 4.2, LOQO: 4.28414, 4.27850, 4.27568, 4.27427 (violations ≤ 2e-12). Our areas are 4.2841471, 4.2785002, 4.2756885 and 4.2742741: agreement to the printed digits.
- LANCELOT (flagged): 4.30178, 4.35538, 4.45009, 4.85693, at violations 3–5e-6. These exceed the exact optima by 0.018 to 0.58. COPS itself says the n=800 point "violates the problem constraints to an extent obvious in a graph". This is early evidence of the ill-conditioning we documented.
- COPS 3.0 Table 3.2 (p. 8): n=800 gives 4.27427 for all five solvers.
- COCONUT and Smith 2011 values are not below our optima.
- QPLIB reference values (`=best=`): −4.28414627, −4.27849041, −4.27565887, −4.27421987. Each is at or above our MINLPLib optima, which is consistent with our certificates.

**Solver bounds**
- SCIP 8.0 suite report (arXiv:2112.08872, App. A, pp. 94–95), SCIP 7/8 gaps: 7.3%/6.1%, 14.8%/13.3%, 18.6%/18.4%, 21.4%/21.6%.
- Mattick–Mutschler 2023 (arXiv:2310.00112, Table 8, after 45 s): SCIP baseline gaps ("Gap Base") 0.074–0.226; their method ("Gap Ours") 0.076–0.222.
- Mittelmann MINLP benchmark (26 Feb 2026): BARON, SHOT, LINDO and SCIP all exceed 7200 s on camshape100.
- Mittelmann QPLIB benchmark, 2025–2026 logs (rounded copies):
  - no solver except ANTIGONE (camshape100) and MINOTAUR (camshape800) claims optimality;
  - final dual bounds are no better than −4.385 (COPT, camshape100), −4.602 (ANTIGONE, camshape200), −4.970 (ANTIGONE, camshape400) and −5.170 (ANTIGONE, camshape800).

**camshape100**
- Bestuzheva et al., arXiv:2301.00587v1, App. B.1 (pp. 36–37): Octeract 4.5.1 solved it in 19.40 s, and its four permutations in 110.89, 97.31, 111.83 and 113.55 s. With gap limit 1e-4: 19.42 s (App. B.2, p. 49).
- In the same table, BARON (9.2–11.1%), Lindo (9.2–9.6%) and SCIP (5.2–5.6%) did not solve it in 2 h.
- Settings (§3.2, pp. 22–23): 1e-6 relative and absolute gap limits for Octeract; 1e-6 feasibility tolerance; missing bounds set to ±1e12.
- Correctness checks (§3.3, p. 23): runs inconsistent with the MINLPLib bounds were marked "nonopt"; camshape100 was not flagged. §3.3 also states that an instance entered the test set only if some solver solved it.
- Mittelmann's QPLIB benchmark (QPLIB_2738):
  - Octeract 3.6.0, 4.5.1 and 4.7.1 solved it in 37, 8 and 17 s (Dec 2021, Jan 2023, Mar 2024); values unknown.
  - ANTIGONE is listed from 2021 to 2026. Its 2026 log claims "Global minimum" at −4.284302, which is 1.55e-4 below the exact optimum, with CONOPT's input point having aggregate Infeasibility 8.7007237331E-06. The log does not explicitly identify the input as ANTIGONE's incumbent. This is a tolerance artifact; after CONOPT polishing the value is −4.28414626579.
- Octeract's dual value is not published. MINLPLib does not list Octeract bounds and still shows ANTIGONE −4.28415233 (rel. gap 1.2e-6).
- **Consequence: already solved globally in floating point.** The exact optimum (−4.28414712174675…, attained by an exactly feasible point and verified in rational arithmetic) is new as far as found.
- Caveat: a 1e-6-feasible incumbent can lie below the exact optimum here. Examples: SCIP's 1e-8-feasible incumbent lies 5.3e-5 below, and ANTIGONE's lies 1.55e-4 below. Octeract's claim and our result therefore concern slightly different feasibility notions.

**camshape200**
- Best listed MINLPLib bound: ANTIGONE −4.63229055 (8.3% gap). COPS LOQO 4.27850 (local).
- Octeract 4.5.1 was listed as solving QPLIB_2480 (rounded copy) in 6853 s in Mittelmann's table of 7 Jan 2023. No log or value survives, and no other version of the table lists this instance as solved. Octeract 4.7.1 does not appear for it in the Mar 2024 table.
- **Partly known:** an unverifiable floating-point claim exists. Our certified optimum is the first published value with proof.

**camshape400**
- Listed ANTIGONE −4.97265746 (16.3%); COPS 4.27568 (local); MINLPLib p2 is a tolerance artifact.
- No solver is listed as solving QPLIB_2703 in any version of Mittelmann's table.
- **New as far as found.**

**camshape800**
- Listed GUROBI −5.12584096 (19.9%); COPS 2.0/3.0 4.27427 (local); p2 is a tolerance artifact.
- MINOTAUR has claimed optimality for QPLIB_3177 in every version of Mittelmann's table (2021–2026). The 2026 value −4.2774 is 3.13e-3 below our certified optimum. Values of the older runs are unknown.
- **Prior global claim false; ours is the first correct global result as far as found.** For the rounded QPLIB copy this rests on evidence, as discussed in the Mittelmann section above.

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

- The SIF value is therefore consistent with a 1e-6-feasible local point; its true origin is undocumented.
- MINLPLib points p1–p5 (2017–2022) are local. From the SIF start, IPOPT gives 353.12245 (= p1); CONOPT failed.
- Bounds: SCIP 351.223393 (2025), LINDO 2.11, BARON 0.051, COUENNE 6.7e-5, ANTIGONE 0. The SCIP 8 suite report shows gap ∞.
- lukvle10 is not quadratic, so it is not in QPLIB or Mittelmann's QPLIB benchmark.

**Consequence: new as far as found.** Mention the SIF SOLTN value in the paper as a tolerance artifact.

### optcdeg2

**Provenance: the MINLPLib model is a variant**
- MINLPLib: Murtagh–Saunders 1982 Ex. 5.11; source QPLIB 8803 (Gould), CUTEr OPTCDEG2; added 18 Aug 2018; T = 50000, Δt = 4e-4. The MINLPLib .gms file is identical to QPLIB_8803.gms up to the solve statement and one redundant declaration (revision 1 check).
- MINLPLib/QPLIB dynamics: v' = Δt(u − 0.02y − 0.2v²). The OSIL coefficient is 8e-5; the QPLIB Hessian is 1.6e-4.
- OPTCDEG2.SIF and Benson's AMPL version use damping 0.05 (C2 = 0.05·DT). So does OPTCNTRL.SIF, CUTEst's encoding of the Murtagh–Saunders example (Δt = 0.2, damping 0.01 = 0.05·0.2, spring 0.004 = 0.02·0.2).
- The objective is correct (Δt/2). Murtagh–Saunders 1982 itself was not read.

**Floating-point confirmation** (IPOPT, checks/optcdeg2_coef_check.gms)
- Damping 0.05 reproduces the SIF SOLTN values: 340.6053 (T=10), 253.2756 (40), 237.2764 (100), 229.573 (400).
- Damping 0.2 at T = 50000 gives 293.8762 (MINLPLib primal 293.8760751).
- Damping 0.05 at T = 50000 gives 227.044.

**Prior results**
- Local SIF values (damping 0.05). QPLIB solution value 293.8760751, with infeasibility 1.75e-15.
- **Mittelmann's QPLIB benchmark.** MINOTAUR 0.2.1 is listed as solving QPLIB_8803 in 1641 s in the table of 3 Dec 2021.
  - The log is not archived, so the value and the basis of the claim cannot be checked.
  - No later version of the table lists it as solved.
  - In 2026, MINOTAUR 0.4.1 stops in presolve with "Detected infeasibility". That is false: the identical MINLPLib model has a rigorously feasible point with value ≤ 293.87607509587509328 (open-instances-summary.md).
  - BARON's 2026 incumbent 293.876075074557 is 2.1e-8 below our certified value, so it is a tolerance artifact.
  - COPT's bound is 283.41.
- **MINLPLib, 2023-04-11:** the GUROBI dual bound 292.41713458 was added together with point p2 of the same value, which has infeasibility 1e-6.
  - This is Gurobi's tolerance-level "optimal" claim. It is false under exact feasibility.
  - The exact optimum is 293.876075…, bracketed by us to 9e-16, which is 1.46 (0.50%) higher.
  - The 292.417 bound itself is valid but weak.
- Other bounds: SCIP 264.42, BARON 4.40, COUENNE 0.42. SCIP 8 suite report: SCIP 7 gap 76.3%, SCIP 8 ∞.

**Consequence: partly known; ours is the first rigorous certificate.**
- An unverifiable floating-point claim exists (MINOTAUR 0.2.1, 2021).
- The only claim with a visible value (Gurobi's 292.417) is a tolerance artifact that our certificate refutes for exact feasibility.
- Describe the instance as "MINLPLib optcdeg2 (QPLIB 8803; damping 4 times that of CUTEst OPTCDEG2)".

### chain50/100/200/400 (hanging chain)

**Provenance**
- COPS 2.0 §3 (suggested by Mittelmann; Cesari 1983, pp. 126–127): minimize ∫x√(1+u²) subject to x' = u, ∫√(1+u²) = 4, x(0) = 1, x(1) = 3; trapezoidal rule; 2nh free variables; nh+1 rows.
- GAMS chain.gms is this model, and MINLPLib (2nh+2 variables) is its conversion. Same model.
- COPS 3.0 §4 reformulates it with auxiliary states (an equivalent model); its values agree.

**Local values**
- COPS 2.0 Table 3.2, LOQO/MINOS/SNOPT: 5.07226, 5.06978, 5.06891, 5.06862. Our optima 5.0722615, 5.0697846, 5.0689173 and 5.0686217 agree to the printed (truncated) digits.
- LANCELOT: 5.07230, 5.07005, 5.06903, 5.06788, at violations 2e-6 to 9.6e-6. The nh=400 value lies 7.4e-4 below the exact optimum (tolerance artifact).
- COPS 3.0 Table 4.2 (p. 10): 5.06891 and 5.06862.
- COCONUT and Smith 2011 agree.

**Structural context**
- Griva–Vanderbei (Optim. Eng. 6 (2005) 463–482, doi:10.1007/s11081-005-2068-0; preprint §2.3) use LOQO and midpoint rules. They write that "it is apparently not possible to make a convex model when parameterizing along x", which is exactly the COPS parameterization. Relaxing the length equality gives an inequivalent model.
- Gabrys–Sremac (arXiv:2510.20917, Oct 2025): convex reformulation of the fixed-link-length chain, a different model.
- MINLPLib bounds: ANTIGONE 0.1745, 0.0937, 0.0826, 0.0956; all other solvers negative. SCIP 8 suite report: gap ∞. Müller et al. 2019: surrogate bounds are negative.
- chain50–400 are in the ANTIGONE 1.0 test suite (2013); no per-instance results were found.
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
- COPS 2.0 Table 14.2, LOQO: −4.80694e-02, −4.80591e-02, −4.80565e-02, −4.80559e-02 (violations 1.2e-8 to 7e-8). Our optima −0.0480694320, −0.0480591456, −0.0480565478 and −0.0480559013 agree to the printed digits.
- MINOS, SNOPT and LANCELOT found worse points.
- COPS notes that the value "fluctuates … probably due to the bang-singular-bang nature" and that the singular controls are non-unique (Fig. 14.1). This is consistent with the chattering we observed.
- COCONUT −0.0481; Smith 2011 catmix800 −0.048055605 (worse than our optimum).

**Solver bounds**
- MINLPLib lists only LINDO: −0.0666, −0.0725, −0.658, −1.489. The last is below the trivial bound −1.
- SCIP 8 suite report and Mattick–Mutschler: gap ∞.
- catmix100–800 are in the ANTIGONE 1.0 test suite (2013); no per-instance results were found. No catmix copy was found in QPLIB.
- Global optimal-control methods (Esposito–Floudas; branch-and-lift, whose case study is a bioreactor; occupation measures) were not found applied to catalyst mixing or its discretization.

**Per instance:** catmix100, 200, 400 and 800 are all **new as far as found**. COPS gives only local values, and the listed bounds are LINDO's.

## 4. Cross-cutting points for the paper

1. **Name the models precisely.**
   - dtoc5 and optcdeg2 are QPLIB/MINLPLib variants with a 4× coefficient on the quadratic dynamics term. The MINLPLib files are identical to QPLIB_8585 and QPLIB_8803.
   - The COPS instances are COPS 2.0 discretizations:
     - camshape and lnts: the same discretized models as in COPS 3.0, as described there and with agreeing values;
     - chain: an equivalent reformulation (COPS 3.0 adds auxiliary states);
     - catmix: a different discretization.
   - MINLPLib camshape drops one curvature row, which is slack at the optimum. QPLIB_2738/2480/2703/3177 are MINLPLib camshape with constants rounded at about 1e-10.
2. **Cite the floating-point predecessors.** For these instances the contribution is rigor and exactness, not first closure; for camshape800 it is also the correction of a false claim.
   - camshape100: Octeract in Bestuzheva et al., arXiv:2301.00587 App. B (whether the JOGO version includes the appendix was not checked); Octeract and ANTIGONE in Mittelmann's QPLIB benchmark.
   - camshape200: Octeract in Mittelmann's QPLIB benchmark (7 Jan 2023 version).
   - camshape800: MINOTAUR in Mittelmann's QPLIB benchmark (2021–2026), whose claim is false.
   - dtoc5: MINOTAUR in Mittelmann's QPLIB benchmark (17 May 2026); Waki, Kim, Kojima and Muramatsu (2006) for the source model.
   - optcdeg2: MINOTAUR 0.2.1 in Mittelmann's QPLIB benchmark (3 Dec 2021).
   - lnts: Göß–Burlacu–Martín (JOGO 2026) and Göß (arXiv 2026).
3. **Published tolerance artifacts support the exact-feasibility framing.** Each of these lies below our certified optimum. The Mittelmann values come from logs on the QPLIB copies (identical for dtoc5/optcdeg2, rounded at about 1e-10 for camshape).
   - LANCELOT values in COPS 2.0 (camshape, chain400, lnts100/400).
   - The LUKVLE10 SOLTN value.
   - Gurobi's optcdeg2 point (1.46 below).
   - The DTOC5.SIF SOLUTION lines, for the h variant, relative to the converged local values, which are global per Waki et al.
   - From Mittelmann's logs:
     - MINOTAUR camshape800 "optimum" (3.1e-3 below);
     - ANTIGONE camshape100 "global minimum" (1.55e-4 below);
     - BARON dtoc5 (5.2e-6 below), optcdeg2 (2.1e-8 below) and camshape800 (0.24 below);
     - COPT camshape100/200/400/800 (4.3e-5, 1.8e-4, 7.4e-4, 3.1e-3 below);
     - SCIP 9.2.1 camshape400 (5.5e-2 below).
   - Also, MINOTAUR 0.4.1 declares the feasible optcdeg2 infeasible.
4. **Incidental notes for other tracks** (not checked): Göß 2026 Table 4 also lists powerflow0039p; JOGO 2026 Table 17 lists eg_int_s, eg_disc_s and eg_disc2_s.

## 5. Caveats

- **Novelty statements are bounded by the searches in Section 2.** Main gaps: paywalled originals; ANTIGONE 2014 and GloMIQO 2013 per-instance results; COCONUT per-model tables; Google Scholar full text.
- **Octeract (camshape100, camshape200):** the results are table entries; Octeract's values and logs were not seen. Mittelmann's Octeract logs and the MINOTAUR 0.2.1–0.4.0 logs are no longer online or archived.
- **camshape800 refutation:** rigorous for the MINLPLib model; for the rounded QPLIB_3177 copy it is strong evidence, not proof.
- **MINOTAUR dtoc5 claim:** the log does not state the default values. Saved master source implies [−100, 100] from x50001 = 1, containing the reference point (max |x| = 8.06); the exact benchmark revision may differ.
- **Waki et al.:** floating-point SDP results on a randomly perturbed objective, with no printed objective values. It is not stated whether the κ = 1e-5 equality relaxation of §6.2 applies to problem (39). The locations given are in the preprint; the published SIAM version was not checked.
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
- Furini et al. QPLIB: a library of quadratic programming instances. Math. Program. Comput. 11 (2019) 237–265, doi:10.1007/s12532-018-0147-4. Preprint https://optimization-online.org/wp-content/uploads/2017/02/5846.pdf, §3.2, p. 18.
- QPLIB pages and files for 8585, 8803, 2738, 2480, 2703 and 3177; qplib.solu (https://qplib.zib.de, fetched 2026-10-01/02).
- Gabrys, Sremac. arXiv:2510.20917v1 (2025).
- GAMS Model Library: camshape (SEQ=232), chain (231), catmix (242), lnts (237). GLOBALLib archive: github.com/GAMS-dev/gamsworld.
- Göß. Clash of MINLP relaxations: piecewise linear vs. global parabolic. arXiv:2603.16505v1, §4.2 (p. 17) and App. B Table 4 (p. 32).
- Göß, Burlacu, Martín. Parabolic approximation & relaxation for MINLP. JOGO 94 (2026) 951–996, doi:10.1007/s10898-026-01591-z (Table 11 p. 972, Table 17 p. 992).
- Griva, Vanderbei. Case studies in optimization: catenary problem. Optim. Eng. 6 (2005) 463–482, doi:10.1007/s11081-005-2068-0.
- Houska, Chachuat. Branch-and-lift. JOTA (2014); optimization-online preprint 3594 (case study only).
- Lukšan, Vlček. TR V-767 (1999), https://invenio.nusl.cz/record/33842 (problem 5.10, p. 25).
- Mattick, Mutschler. arXiv:2310.00112 (Table 8).
- Mevissen, Lasserre, Henrion. arXiv:1003.4608 (examples are not our problems).
- MINLPLib: instance pages (cached 2026-09-29), bounddates.html (2026-10-01), and .gms files for camshape100–800, dtoc5 and optcdeg2 (2026-10-02).
- Misener, Floudas. ANTIGONE 1.0 Test Suite (1 May 2013), Table 4, PDF p. 21; Wayback copy of http://helios.princeton.edu/ANTIGONE/ANTIGONE_TestSuite.pdf. GloMIQO 2.0 Test Set (8 Jul 2012); Wayback copy of http://helios.princeton.edu/GloMIQO/MisenerFloudas_GloMIQO_TestSet.pdf.
- Misener, Floudas. GloMIQO: Global mixed-integer quadratic optimizer. JOGO 57 (2013) 3–50, doi:10.1007/s10898-012-9874-7 (not read).
- Misener, Floudas. ANTIGONE: Algorithms for coNTinuous / Integer Global Optimization of Nonlinear Equations. JOGO 59 (2014) 503–526, doi:10.1007/s10898-014-0166-2 (not read).
- Mittelmann. MINLP benchmark, plato.asu.edu/ftp/minlp.html (26 Feb 2026), and compare.txt.
- Mittelmann. Continuous Non-Convex QPLIB Benchmark, https://plato.asu.edu/ftp/cnconv.html (17 May 2026) and logs at plato.asu.edu/ftp/cnconv_logs/; Wayback snapshots 20211220190650, 20230127150157, 20240411093434, 20240921192253, 20250413104831, 20250819054739 and 20251231152213.
- Müller, Muñoz, Gasse, Gleixner, Lodi, Serrano. On generalized surrogate duality in mixed-integer nonlinear programming. arXiv:1912.00356v1 (2019), appendix tables (PDF pp. 40–41, 46, 58).
- Neumaier, Shcherbina, Huyer, Vinkó. Math. Program. 103 (2005) 335–356, doi:10.1007/s10107-005-0585-4. COCONUT benchmark pages.
- Smith. PhD thesis, Carleton University (2011), doi:10.22215/etd/2011-09468 (Table A.1).
- Waki, Kim, Kojima, Muramatsu. Sums of squares and semidefinite program relaxations for polynomial optimization problems with structured sparsity. SIAM J. Optim. 17(1) (2006) 218–242, doi:10.1137/050623802. Preprint B-411 (rev. Feb 2005), https://optimization-online.org/wp-content/uploads/2004/10/988.pdf: problem (39) p. 30, Table 12 p. 31, ε_obj definition pp. 21–22, §6.2 p. 26.
- CUTEst SIF files (bitbucket.org/optrove/sif) and Benson's AMPL files (vanderbei.princeton.edu/ampl/nlmodels/cute/).

Cited but not read: Anitescu–Serban 1998; Betts–Eldersveld–Huffman 1993; Bryson–Ho 1975; Cesari 1983; Gunn–Thomas 1965; von Stryk 1999; Murtagh–Saunders 1982; Lukšan–Vlček 1998 (NLAA 5:219–247); Andrei 2013; GloMIQO 2013 and ANTIGONE 2014 papers.

## 7. Revision after review round 1 (2026-10-02)

I re-fetched every new source myself into `sources/` (listed in `MANIFEST.md`, last table) and wrote my own checks (`checks/qplib_camshape_compare.py`, `checks/qplib_dtoc5_optcdeg2_identity.log`, `checks/mittelmann_values_vs_certified.py`).

**M1 (major): missed Mittelmann's Continuous Non-Convex QPLIB Benchmark and the QPLIB camshape copies. Fixed.**
- Added a new subsection in Section 3, rewrote the bottom line and the summary table, and revised the dtoc5, optcdeg2, camshape100, camshape200 and camshape800 sections.
- New labels:
  - dtoc5, optcdeg2, camshape200: partly known;
  - camshape800: prior global claim false; first correct result as far as found;
  - camshape100: already solved globally in floating point, with the Mittelmann results added.
- I confirmed the reviewer's facts from my own fetches, with these refinements:
  - (a) I showed that QPLIB_8585 and QPLIB_8803 are textually identical to MINLPLib dtoc5 and optcdeg2. Hence MINOTAUR's optcdeg2 "infeasible" verdict is provably false, given the project's verified feasible point.
  - (b) The stored SCIP logs are SCIP 9.2.1 (dated 4 Apr 2025), not 10.0.1. The camshape400 primal −4.33024 is SCIP 9.2.1's.
  - (c) COPT's optcdeg2 bound 283.41 is weaker than MINLPLib's GUROBI 292.417. Only COPT's dtoc5 bound (0.7619) exceeds MINLPLib's best bound.
  - (d) The reviewer's remark that the 8-digit rounding "probably moves the optimum by about 8.5e-7" is not established. QPLIB's reference point is feasible in the MINLPLib model to 1e-14 and may just be slightly suboptimal. BARON's QPLIB_2738 incumbent is within 1.9e-8 of our optimum. This does not change any conclusion.
  - (e) The sentence "All problems were solved GLOBALLY" appears from the 7 Jan 2023 version on; the 3 Dec 2021 version says only "succeeded".
  - (f) ANTIGONE's camshape100 "Global minimum" is followed by a CONOPT input point with aggregate Infeasibility 8.7007237331E-06; identifying the input with ANTIGONE's incumbent is an inference.
- On the camshape200 label I differ from the reviewer, who suggested "already solved in floating point". I used "partly known (unverifiable claim)" because the value is unpublished, the log is lost and the result was never repeated.

**M2 (major): missed Waki, Kim, Kojima and Muramatsu (2006). Fixed.**
- Added to the dtoc5 section, the summary table, the bottom line, cross-cutting point 2 and the references. Locations were checked in the preprint: problem (39) p. 30, Table 12 p. 31.
- Added caveats: perturbed objective, no printed values, possible κ = 1e-5 equality relaxation (§6.2, p. 26), floating point.
- The instance label is "partly known" because of MINOTAUR's claim on the identical model. The Waki result concerns the h variant at M = 600–1000.

**Minor 1 (QPLIB filter): fixed.** The filter now reads: discard instances that at least 30% of the complete solvers solve within 30 s; then discard instances that one complete solver solves to proven optimality within 120 s (preprint §3.2, p. 18).

**Minor 2 (optcdeg2 "original source"): fixed.** The bottom line now names OPTCDEG2.SIF and OPTCNTRL.SIF and says that Murtagh–Saunders 1982 was not read.

**Minor 3 ("identical to COPS 3.0"): fixed.** Cross-cutting point 1 now says "equivalent reformulation" for chain.

**Minor 4 (Mattick–Mutschler gaps): fixed.** "Gap Base" 0.074–0.226 and "Gap Ours" 0.076–0.222 (Table 8) are now quoted separately.

**Minor 5 (GloMIQO): fixed, and extended.**
- The GloMIQO paper is listed as not read: closed access; OpenAlex reports no OA copy; CORE returned a Cloudflare challenge.
- I found the archived GloMIQO 2.0 Test Set (2012). It does not list GLOBALLib instances by name.
- I also found the ANTIGONE 1.0 Test Suite (2013). It lists camshape, catmix and chain (Table 4, PDF p. 21) but gives no results.

**Minor 6 (more tolerance artifacts): fixed.**
- Added to cross-cutting point 3 and the instance sections, with the differences recomputed in `checks/mittelmann_values_vs_certified.log`.
- Also added the ANTIGONE camshape200/400 bounds on the QPLIB copies, which are stronger than MINLPLib's listed bounds.

**Minor 7 (DTOC5.SIF SOLUTION lines): fixed.** I listed each line and its distance below the converged local value. With Waki et al.'s evidence, these lines are not valid optimal values.

**Minor 8 (out-of-date open issue): fixed.** I removed "report.md was NOT written".

**Minor 9 (Müller et al. 2019): added** as an optional citation (weak surrogate bounds). Its "best primal" for camshape800, −4.27431, is noted as another value below our certified optimum.

## Commands run

**Original round (2026-10-01; from the first agent's structured return)**
- Read research files: open-instances-summary.md, open-instances/open-instances-report.md, open-instances-wave2/cops/report.md, reviews/catmix-recheck.md, prior novelty sections in reviews/open-instances-verification and reviews/cops-verification, closing-research-results.md excerpts, and bound-audit/pages/*.html for the 19 instances.
- `curl -sSL` downloads, sequential with ≥ 1 s spacing:
  - COPS 3.0 pdf and index; COPS 2.0 HTML report pages;
  - arXiv 2301.00587, 2112.08872, 2603.16505, 2310.00112, 2510.20917, 2202.06017, 2312.16216, 1003.4608, 2511.18580;
  - optimization-online 7065, 3594 and the FICO paper;
  - LV V-767 pdf; Coleman–Liao report .ps (ecommons API);
  - CUTEst SIF files DTOC5, OPTCDEG2, LUKVLE10, OPTCNTRL, DTOC1L, DTOC3, DTOC4, DTOC6; Benson AMPL dtoc5/optcdeg2;
  - QPLIB 8585/8803 pages and .qplib files;
  - COCONUT benchmark pages, Library 1/2 tables and .res files; Neumaier et al. comparison pdf;
  - GAMS-dev/gamsworld GlobalLib files (GitHub API/raw);
  - Mittelmann minlp.html and compare.txt; MINLPLib bounddates.html and dates.html; mittelmann-plots repo pages;
  - Griva–Vanderbei preprint; Smith 2011 thesis; GAMS presentations.

  Outcome: all succeeded except the COPS 3.0 zip (404) and IBM RC25385 (connection refused). Wayback CDX was offline at first; wayback/available later returned a snapshot.
- WebSearch (about 20 queries) and WebFetch (Wikipedia Octeract page, CONICET item); OpenAlex fulltext.search queries for all instance names and related terms; Crossref API for DOI verification; arXiv API (timed out).
- Semantic Scholar snippet search: background job PID 181314 (python3 /tmp/ctl_s2/s2.py, log /tmp/ctl_s2/s2.log). All queries were rate-limited (HTTP 429); the job was killed and no results were used.
- `pdftotext -layout`, `ps2pdf` and `pypdf` for page location; grep for instance names in all fetched papers.
- `python3 checks/dtoc5_coef_check.py` (damped Newton; a first L-BFGS-B version timed out, exit 143) → checks/dtoc5_coef_check.log. Outcome: the h version reproduces Coleman–Liao Table 3 exactly; the 4h version with N=50000 gives 5.389672119181.
- `gams checks/optcdeg2_coef_check.gms --T={10,40,100,400,50000} --damp={0.05,0.2} --solver=ipopt` (and conopt for T=40), `lo=0 threads=1` → checks/optcdeg2_coef_check.log. Outcome: damping 0.05 reproduces the SIF SOLTN values; damping 0.2 at T=50000 gives 293.8762; damping 0.05 at T=50000 gives 227.044.
- `gams checks/lukvle10_local_check.gms --N=1000 --solver={ipopt,conopt}` → IPOPT 353.12245 (= MINLPLib p1); CONOPT failed (model status 6).
- `gams checks/lukvle10_tolerance_check.gms --tol={0,1e-8,1e-7,1e-6,1e-5} --solver=ipopt` (start point MINLPLib p5) → 352.23803, 352.23802, 352.23799, 352.23762, 352.23396.
- `python3` floating-point read of open-instances/logs/camshape{100,200,400,800}_envelope.npy: the omitted COPS curvature row (r1, r2) is slack by a factor of about 60 to 480.
- `sha256sum` of all stored sources → sources/MANIFEST.md; wrote checks/README.md.

**Revision 1 (2026-10-02, this agent).** All commands ran in the foreground, with no background jobs.
- Read report.md, the review, the reviewer's PROGRESS.json and the list of the reviewer's fetched files (the reviewer's files themselves were not used as sources).
- Mittelmann's benchmark (`curl -sSL`, sequential, ≥ 1 s apart):
  - https://plato.asu.edu/ftp/cnconv.html;
  - log directory listings for ant/bar/cop/mnt/sci;
  - 30 logs `cnconv_logs/{ant,bar,cop,mnt,sci}_results/QPLIB_{2738,2480,2703,3177,8585,8803}.*`;
  - Wayback CDX for cnconv.html and cnconv_logs/*;
  - 7 Wayback snapshots (`id_`), gunzipped.

  Outcome: all succeeded.
- QPLIB:
  - pages, .gms and .sol files for 2738, 2480, 2703 and 3177; qplib.solu; instances.html;
  - QPLIB_8585.gms and QPLIB_8803.gms, plus MINLPLib camshape100–800.gms, dtoc5.gms and optcdeg2.gms;
  - HEAD requests for the file sizes.

  Outcome: all succeeded.
- Papers:
  - optimization-online 988.pdf (Waki et al.) and 5846.pdf (QPLIB);
  - arXiv 1912.00356v1, 2603.09864, 2410.03720 and 2106.13721;
  - Wayback CDX for helios.princeton.edu/GloMIQO/* and /ANTIGONE/*, then the archived GloMIQO 2.0 Test Set and ANTIGONE 1.0 Test Suite PDFs;
  - core.ac.uk/works/34453073 (Cloudflare challenge: failed);
  - plato.asu.edu/bench.html.

  Outcome: all succeeded except CORE.
- APIs:
  - OpenAlex: work record for doi:10.1007/s10898-012-9874-7 (closed access); full-text search for QPLIB_2738/_2480/_2703/_3177/_8585/_8803 with and without the underscore (0 hits each).
  - Crossref: 10.1137/050623802, 10.1007/s10898-012-9874-7, 10.1007/s10898-014-0166-2 (metadata match the citations); also 10.1007/s10898-013-0059-9, a wrong guess that resolved to a different paper and was not used.
- WebSearch, 2 queries: GloMIQO with camshape/catmix; QPLIB_3177/2738/8585/8803 with global solver results.
- `pdftotext -layout` and grep/page location on Waki et al., the QPLIB paper, the ANTIGONE and GloMIQO test-suite PDFs, Müller et al., Mattick–Mutschler (Table 8 columns), the three arXiv papers above, and the Coleman–Liao report (problem 5). I also read the DTOC5.SIF SOLUTION lines and the QPLIB_8803 excerpt.
- grep of the 30 Mittelmann logs and 7 snapshots for termination status, incumbents, bounds and solver versions.
- `python3 checks/qplib_camshape_compare.py <camshapeN.gms> <QPLIB_q.gms> <camshapeN.p1.sol> <QPLIB_q.sol>` for (100, 2738), (200, 2480), (400, 2703) and (800, 3177). Three earlier runs failed or gave misleading output and were fixed:
  - a KeyError, because .sol files omit zero values;
  - a version that counted the objective-defining row as a violation;
  - a run on /tmp copies before the files were stored.

  The final run on the stored copies → checks/qplib_camshape_compare.log: all rows matched; maximum relative coefficient difference ≤ 2.3e-10.
- `diff` of the MINLPLib and QPLIB .gms files with comment lines removed, plus `sha256sum` → checks/qplib_dtoc5_optcdeg2_identity.log: identical up to the solve statement and one redundant declaration.
- `python3 checks/mittelmann_values_vs_certified.py` → .log.
- `python3` scans: a size scan of the QPLIB listing for catmix copies (none), and PDF page location of key lines.
- `python3` to append 62 new rows with sha256 to sources/MANIFEST.md; appended a revision-1 section to checks/README.md; updated PROGRESS.json.
- `ps` check: no processes of mine remain. The running GAMS jobs, under driver.py PID 819808, belong to the solver-campaign track and were not touched.
- No project-wide checks, no CI inspection, no git operations.

## Open issues

- **Novelty is limited to what was searched.** Not accessed:
  - Google Scholar full text;
  - paywalled originals (Murtagh–Saunders 1982, Lukšan–Vlček 1998 NLAA, Anitescu–Serban 1998, Betts et al. 1993, Gunn–Thomas 1965, von Stryk 1999, Andrei 2013);
  - the GloMIQO (2013) and ANTIGONE (2014) papers and their per-instance results;
  - the COCONUT per-model solver tables.

  Semantic Scholar was rate-limited and IBM RC25385 was unreachable.
- **Lost logs.** Octeract's camshape100/200 values and MINOTAUR 0.2.1's optcdeg2 value (Mittelmann 2021–2024) are unknown, because the logs are neither online nor archived. Bestuzheva et al.'s Octeract dual value is not published, and it is unknown whether the JOGO (2025) version contains the appendix.
- **camshape800 for the QPLIB copy.** The refutation of MINOTAUR's claim is rigorous for MINLPLib camshape800 but only evidence for QPLIB_3177 (constants rounded at about 2e-10). Running our camshape certificate on the QPLIB constants would make it rigorous; this was not done.
- **MINOTAUR dtoc5 run.** Master source implies [−100, 100] from x50001 = 1, but its log does not state the values and the exact benchmark revision may differ.
- **Waki et al.** The published SIAM version was not checked; the locations are in the preprint. Whether §6.2's κ = 1e-5 equality relaxation was used for problem (39) is not stated in the paper.
- **lnts.** The Göß 2026 PARA dual bounds are printed to 2 significant digits, with gaps to 2 decimals in percent. The PARA under-estimators are validated numerically; their validity for exact feasibility was not assessed.
- **Factor-4 discrepancy (dtoc5, optcdeg2).** Shown only for QPLIB 8585/8803. Where it arose was not determined, other CUTEst-derived QPLIB/MINLPLib instances were not checked, and no public erratum was found.
- **LUKVLE10 SOLTN value.** Its origin (352.237) is inferred from the 1e-6 tolerance experiment, not documented.
- **camshape and COPS 2.0.** The claim that our camshape optima equal the COPS 2.0 discrete optima rests on a floating-point slack check and on COPS's verbal description, not on the COPS AMPL file (the COPS 3.0 zip returned 404).
- **For other tracks (not checked).** Göß 2026 Table 4 lists powerflow0039p; JOGO 2026 Table 17 lists eg_int_s, eg_disc_s and eg_disc2_s.
## Response to review

Review: `../../reviews/lit-control-review-r2.md`. Checked and resolved on 2026-10-03. Round-1 resolutions remain in the report.

| issue | resolution and evidence |
|---|---|
| 2.1. Missed upper bounds | Dropped only the regex start anchor in `qplib_camshape_compare.py`. Rechecked every bound in all four pairs; corrected the largest reported difference to 4.7e-10. Added the two reference-point r1 upper-bound violations. |
| 2.2. Waki Table 12 range and tested sizes | Read Table 12 (printed p. 31, PDF p. 33): feasibility range −1.6e-10 to −8.1e-10 and tested M = 600,700,800,900,1000. Corrected every M ≤ 1000 statement. |
| 2.3. Müller camshape100 page | Checked PDF p. 40 and corrected both the body and bibliography page location; camshape200–800 remain on p. 41. |
| 2.4. Evidence for spurious camshape800 closure | Read all four MINOTAUR logs. Added root-only closure/+∞ bound versus smaller-copy timeouts, defined false under exact feasibility, and retained the QPLIB-copy caveat. |
| 2.5. MINOTAUR dtoc5 default bounds | Read the saved master `QuadHandler.cpp` rule; explained inference [−100,100], re-fetched the reference point and confirmed its scale 8.06, revision caveat and plausible root-only convex closure (`checks/dtoc5_reference_check.log`). |
| 2.6. MINLPLib optimizer wording | Changed to MINLPLib point p1 and stated its own 3.9e-10 MINLPLib row violation; p1 is not the exactly feasible optimizer. |
| 2.7. CONOPT aggregate measure | Reworded every 8.7e-6 discussion as CONOPT's aggregate Infeasibility for its input; incumbent identity is an inference, not explicit log evidence. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/minor_review_check.py > research-20260929/publication/literature/control/checks/minor_review_check.log` (from the repository root). All checks pass. Additional source-copy, metadata and text-extraction commands are recorded in `publication/reviews/minor-fixes/commands.md`. No solver, main certificate computation, project-wide verification or CI check was run for this revision.
