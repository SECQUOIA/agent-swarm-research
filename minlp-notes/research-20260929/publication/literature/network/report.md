<!-- Written to disk by the root from the structured return value of agent 'fix:lit-network:r1' (the harness blocks subagents from writing report files). Status: complete. -->

# Literature check: power flow, water network and neural-network instances

Track: lit-network. First version: 2026-10-01. Revised after review round 1: 2026-10-02 (Section 11), and round 2: 2026-10-03 (Response to review).

Scope: the 15 instances powerflow0030p, powerflow0039p, powerflow0039r, kan_r3_h1_n4, kan_r3_h1_n5, kan_r3_h1_n9, kan_r5_h1_n3, kan_r5_h1_n5, kan_r5_h1_n8, waterno2_06, waterno2_09, waterno2_12, waterno2_18, waterno2_24 and ann_cumene_tanh. Our claims are the ones in `open-instances-summary.md` and the linked notes (`open-instances-wave3/report.md`, `open-instances-wave3/powerflow/extension-report.md`, `open-instances-wave2/waterno2/report.md`, `open-instances-wave3/ann/extension.md`).

Status: research is complete for every source that could be reached. Three sources remain unobtained, besides the publisher versions of papers that were read as preprints (Section 8). Copies of the sources are in `publication/literature/network/sources/`; `sources/MANIFEST.md` gives the URL, date and sha256 of each file. The targeted checks are in `publication/literature/network/checks/` (Section 7).

The full report is now on disk, including all per-instance sections, assumptions, source limits and commands. Section 11 records round-1 resolutions; Response to review records the remaining round-2 issues. Historical failed-write entries in Section 12 describe the earlier workflow only.

FP = floating-point solver result. Rigorous = exact rational or outward-rounded interval arithmetic.

## 1. Main findings

1. **kan_r3_h1_n4 and kan_r3_h1_n5: a published "global optimum" exists, and it contradicts our certified bound.**
   - **Published claim.** The source paper (Karia, Lastrucci, Schweidtmann 2025, arXiv:2503.02807) reports that SCIP 9.0.1 solved these exact networks to gap 0. Its supplementary logs (Zenodo 14961066) give optimal values 1.08116412e-3 and −1.30809959e-2 for the "Default" formulation. That formulation has exactly the MINLPLib variable and constraint counts.
   - **Conflict.** Both values are **below** our certified minimum of the network relaxation R (0.0027812371525814 and −0.011042679521782).
   - **Network value at SCIP's points.** At SCIP's own reported inputs, the exact network evaluates to 0.0028684784 and −0.0108512435. This is a high-precision evaluation; the reviewer's independent code confirms it.
   - **Cause.** The published optima are artifacts of SCIP's feasibility tolerance. The output is scaled by about 970, so row violations of about 1e-6 shift the objective by about 1e-3. They are floating-point claims, not optimal values of the exact network.
   - **Supporting evidence.** The other formulations in the same supplement give five (n4) and four (n5) further "optimal" values. They all differ from each other and all lie below our bound.
   - **Direct demonstration on the MINLPLib model (reviewer).** With the inputs fixed at SCIP 9's point, SCIP 10.0 returns "optimal" values 0.0026959 (n4) and −0.0113203 (n5). Both are again below our bounds, with row violations up to 1e-6.
   - The paper must mention this conflict.
2. **powerflow0030p: closed in floating point through its rectangular twin. The MINLPLib model is MATPOWER case30 without its two bus shunts.**
   - **Shunts dropped.** The MINLPLib balance rows have no shunt terms. case30's Bs = 0.19 MVAr at bus 5 and 0.04 MVAr at bus 24 are missing (checked in Section 3.1). The reviewer's local AC OPF gives 576.8934134 without shunts, which equals the MINLPLib primal, against 576.8923368 for case30 with shunts.
   - **Other data match**, including loads.
   - **FP closure via the twin.** MINLPLib lists ANTIGONE's dual 576.8934129 for the rectangular twin powerflow0030r (primal 576.8934135). The models have the same data up to coefficient rounding in the 15th–16th significant digit, with additional angle-difference rows in 0030p (r2 check, Section 3.2). This supports FP closure via the twin at solver tolerance. It does not establish exact transport of rigorous dual bounds between the two stored models.
   - **Close relative.** NESTA (Table 1), Bingane et al. 2018 (Table I) and the source report of Hijazi, Coffrin and Van Hentenryck (June 2014 revision, Table 3) give a 0.00% SDP gap for MATPOWER case30. They use the case with shunts, so they concern a close relative.
   - **Our result.** Our exact-arithmetic certificate is the first rigorous one found for this MINLPLib model. Certified ACOPF bounds on different PGLib models predate it (Oustry et al. 2022, Section 8). It is also the first bound that closes the gap on the polar instance as listed.
   - Status: "partly known".
3. **powerflow0039p/r: the MINLPLib model is not MATPOWER case39.**
   - **Taps dropped.** The MINLPLib rows drop the off-nominal transformer tap ratios. For 11 of the 12 tapped branches, the GAMS file contains the untapped admittance and none of the tapped values. The twelfth has τ = 1.
   - **Other data match.** case39 has no bus shunts, and the loads and all other checked data match.
   - **Different optimum.** The optimum of the MINLPLib model (41869.05) therefore differs from MATPOWER case39's (41864.18).
   - **Tapped case solved in FP.** Ghaddar, Mareček and Mevissen (2016, Table 4) solved MATPOWER case39 with taps globally in floating point: their second-order moment bound, 41864.18, equals the local value. NESTA (Table 1, SDP gap 0.00%), Bingane et al. (Table I, 41864.18 / 41862.03) and the 2014 Hijazi et al. report (Table 3) also treat the tapped case.
   - None of these results applies to the MINLPLib instance. We found no prior closure of the tap-free model.
   - Status: "new as far as found", with this close relative noted.
4. **waterno2_06–24: no prior closure found. The source network is now identified.**
   - **Identification.** waterno2 is the Tsinghua University network n9p3a11 from Huang's 2019 TU Darmstadt dissertation (1 reservoir, 3 tanks, 9 variable-speed pumps). The pump-cost polynomial of the dissertation's Example 5.41 appears in every waterno2 file, twice per period. Its 1- and 2-period optima (19.46, 39.57) equal those of waterno2_01/02.
   - **Prior multi-period runs.** Table 5.2 of the dissertation reports SCIP 5.0.1 runs (1 h each) on versions with 1 to 24 periods. From 3 periods on, its optimal values differ from MINLPLib's (215 against 115.0045 for 3 periods). These are therefore related models, not the instances as written. None of the runs with 5 or more periods closed the gap. The extended-model gap is 0.000470589 at 5 periods (above the 1e-5 stopping limit); the range 0.18–1.14 applies to 6–24 periods.
   - **Other sources.** The cited NACO 2012 paper solves only stationary models of two other networks. D'Ambrosio et al. (2015) state that the multi-period problem had not been solved in the literature.
   - **Gap.** Huang's 2011 master's thesis, which MINLPLib cites, was not obtained.
   - Status: "new as far as found".
5. **ann_cumene_tanh: closed in floating point through an identical MINLPLib twin.**
   - **Twin.** MINLPLib's ann_cumene_exp is the same problem, with −tanh(v) written as 2/(exp(2v)+1) − 1. We proved this with exact arithmetic (`checks/cumene_twin_exact.py`); the reviewer's independent check agrees.
   - **FP closure.** For ann_cumene_exp, MINLPLib lists the duals −3379.982394 (SCIP), −3379.982394 (LINDO) and −3379.985774 (BARON), against the primal −3379.982394. SCIP and LINDO therefore closed the problem in floating point.
   - **Source paper (2018).** In arXiv:1801.07114v2 by Schweidtmann & Mitsos (Table 4, Fig. 6), the same 794-variable full-space problem was not closed in 1e5 s. BARON gave no useful lower bound (absolute gap 1e20), and MAiNGO's best reduced-space run ended with an absolute gap of 1e5. The 2021 dissertation's Table 2.8 instead gives MAiNGO gaps 2930, 444 and 328; neither version converged, and the JOTA full-text table remains unchecked.
   - **Our result.** Our rigorous −3386.5403 (gap 0.194%) is the first rigorous bound found, but it is weaker than the floating-point claims.
   - Status: "partly known". The phrase "the first finite dual" in `open-instances-summary.md` needs the same correction.
6. **kan_r3_h1_n9 and kan_r5_h1_n3/n5/n8: new as far as found.**
   - All SCIP runs in the source paper hit the 7200 s limit. The best dual bounds over its six formulations are −11.376, −1587.43, 0.18669 and −122.67.
   - **Another tolerance artifact.** For kan_r5_h1_n5, the ConvexHull formulation reports a primal value of 0.2725188, below our certified minimum of R (0.27258325). The exact network at that input gives 0.2729243.
   - For all six KAN instances, our claim concerns R, because the OSIL models have no exactly feasible point (proved in wave 3).

## 2. Summary table

| instance | provenance (model as written) | strongest prior result found | consequence for our claim |
|---|---|---|---|
| powerflow0030p | MATPOWER case30 (Alsac–Stott network, Ferrero et al. costs) **without its two bus shunts**; polar AC OPF from the Hijazi–Coffrin–Van Hentenryck models; plus 164 non-binding ±0.26 rad angle rows | FP: ANTIGONE dual 576.8934129 on the rectangular twin powerflow0030r (same data up to 15th–16th-significant-digit rounding, no angle rows), supporting tolerance-level closure of 0030p; exact bound transport is not proved. Close relative (case30 with shunts, 576.89): SDP gap 0.00% (NESTA Table 1; Bingane et al. 2018 Table I; Hijazi et al. 2014 Table 3) | partly known: closed in FP via the twin; ours is the first rigorous certificate found for this MINLPLib model and the first bound that closes the gap on 0030p as listed |
| powerflow0039p | MATPOWER case39 with transformer taps dropped; polar; 184 ±0.26 rad angle rows | FP on a different model: MATPOWER case39 with taps, solved by a moment relaxation at 41864.18 (Ghaddar et al. 2016 Table 4). SDP gaps: 0.00% (NESTA), 0.01% (Bingane SDR), 0.005% (Lavaei–Low SDP in Ghaddar et al.). Nonclosing FP benchmark: Göß 2026 lists 0039p dual 4.0e2 / gap 9.90, with an unexplained scale discrepancy (Section 3) | new as far as found (close relative solved in FP) |
| powerflow0039r | same data; rectangular; no angle rows | same tapped-model precedents as 0039p; nonclosing FP runs in SCIP suite 8.0 and Müller et al. 2020 (Section 3); MINLPLib best dual 41804.88 (GUROBI) | new as far as found (same caveat) |
| kan_r3_h1_n4 | KAN [3,4,1] surrogate of the 3-D Rosenbrock function (Karia et al. 2025), Default formulation (1129 vars / 1478 cons, exact match) | FP claim: SCIP 9.0.1 "optimal" 1.08116e-3, gap 0 (Zenodo logs; Table 5 of the paper) | prior FP claim contradicted (below our certified min of R, 0.0027812); ours new |
| kan_r3_h1_n5 | KAN [3,5,1], same source (1410/1847, exact match) | FP claim: SCIP "optimal" −1.30810e-2, gap 0 | prior FP claim contradicted (our min of R: −0.0110427); ours new |
| kan_r3_h1_n9 | KAN [3,9,1] (2534/3323, exact match) | SCIP time limit; best dual −11.376 (FP) | new as far as found |
| kan_r5_h1_n3 | KAN [5,3,1] surrogate of the 5-D Rosenbrock function (838/1121, exact match) | SCIP time limit; best dual −1587.43 (FP) | new as far as found |
| kan_r5_h1_n5 | KAN [5,5,1] (1392/1867, exact match) | SCIP time limit; best dual 0.18669 (FP; Table 9 of the paper: "DB 0.19") | new as far as found |
| kan_r5_h1_n8 | KAN [5,8,1] (2223/2986, exact match) | SCIP time limit; best dual −122.67 (FP); best primal 0.2141 | new as far as found (dual and primal) |
| waterno2_06 | multi-period pump operation of the Tsinghua network n9p3a11 (1 reservoir, 3 tanks, 9 variable-speed pumps; Huang 2019 Section 5.5), 6 periods; MINLPLib cites Huang 2011 (MSc) and Gleixner et al. 2012 | MINLPLib solver bounds (best 165.19, SCIP); heuristic primal 442.50 (Geißler et al. 2017); a related 6-period model in Huang 2019 Table 5.2, not closed (extended-model gap 0.18) | new as far as found (MSc thesis not seen) |
| waterno2_09 | same network, 9 periods | MINLPLib best dual 273.90 (SCIP); Huang 2019 related model not closed (extended-model gap 0.53) | new as far as found |
| waterno2_12 | same network, 12 periods | MINLPLib best dual 479.51 (GUROBI); Huang 2019 related model not closed (extended-model gap 0.84) | new as far as found |
| waterno2_18 | same network, 18 periods | MINLPLib best dual 770.74 (SCIP); Huang 2019 related model not closed (extended-model gap 0.90) | new as far as found |
| waterno2_24 | same network, 24 periods | MINLPLib best dual 1095.13 (SCIP); Huang 2019 related model not closed (extended-model gap 1.03) | new as far as found |
| ann_cumene_tanh | full-space version of the 14-MLP cumene model of Schweidtmann & Mitsos 2019 (794 variables, as in arXiv v2 Table 4); identical to MINLPLib ann_cumene_exp (proved exactly) | FP: ann_cumene_exp closed by SCIP and LINDO (dual −3379.982394 = primal); BARON dual −3379.985774. In arXiv v2 no method converged in 1e5 s | partly known: closed in FP via the exp twin; ours is the first rigorous bound found, weaker than the FP claims |

The gaps quoted for Huang 2019 are (primal − dual)/dual from Table 5.2, in the columns "with extended pump cost relaxation constraints". The original-model columns give 1.79, 3.67, 4.64, 10.72 and 17.43.

## 3. Power flow

### 3.1 Provenance (all three instances)

- **MINLPLib pages.** Fetched 2026-09-29 and again on 2026-10-01; unchanged. They cite Hijazi, Coffrin, Van Hentenryck, "Convex Quadratic Relaxations of Nonlinear Programs in Power Systems", Tech. Rep. 2013-09, Optimization Online. The instances were added on 18 Aug 2014.
- **Source report.**
  - Optimization Online now serves only the October 2016 revision. That revision became Math. Prog. Comp. 9(3):321–367 (2017) and uses NESTA v0.6.0.
  - The Internet Archive holds one earlier copy (snapshot 2015-12-24; PDF CreationDate 2014-06-03). This is the version that was current when MINLPLib added the instances. The September 2013 first version is not archived.
  - The June 2014 revision (`sources/hijazi2014_oo4057_wayback20151224.pdf`) states the following.
    - **p. 16, Section 6 setup and footnote 1:** "the phase angle bound θu was set to π/12". The models in the experiments are the "complete" power-flow equations, including "voltage transformers, line charging, and bus shunts". Thirteen MATPOWER benchmarks are used.
    - **p. 17, Table 1:** benchmarks 5, 6 and 7 have 30 buses and 41 lines; benchmark 8 has 39 buses and 46 lines.
    - **p. 18, Table 3:** for benchmarks 5 and 6, AC 576 with SDP gap 0.00% (QC-NLP gap 0.57%). For benchmark 8, AC 41864 (the tapped value) with SDP gap −0.06%. The authors explain the negative gaps: "due to numerical difficulties, on some instances, the SDP relaxation returns a non valid lower bound".
  - So the models solved in the source report include taps and shunts, while the MINLPLib GAMS models have neither. The angle limit π/12 ≈ 0.2618 appears in MINLPLib rounded to 0.26.
- **Data check.** The scripts `checks/powerflow_data_match.py` and `checks/powerflow_loads_shunts.py` (logs next to them) compare the MINLPLib GAMS files with MATPOWER `case30.m` and `case39.m` (GitHub master, fetched 2026-10-01).
  - **Costs, limits, line charging** (`powerflow_data_match.py`, coefficient multisets).
    - case30: costs match (per unit); all voltage and generator P/Q limits appear as single-variable rows; thermal-limit rows match rateA at both ends; all 9 line-charging values appear as b_s − b_c/2. case30 has no tapped transformers.
    - case39 (0039p and 0039r): costs (100p² + 30p, constant 2 = 10 × 0.2), limits, thermal limits and 34/34 line-charging values match.
  - **Taps (case39).** For 11 of the 12 transformer branches with ratio ≠ 0, the GAMS coefficients contain the untapped admittance and none of the tapped values (g/τ, g/τ², b/τ, b/τ²). The twelfth branch has τ = 1. Example: branch 2–30 (x = 0.0181, τ = 1.025) appears in row e156 of 0039r with the symmetric coefficient 55.2486187845304 = 1/0.0181.
  - **Loads and shunts** (`powerflow_loads_shunts.py`, exact rational arithmetic; added in the revision). The last 2 × nbus rows of each model are the bus balance rows. They come in four blocks: active rows of generator buses, reactive rows of generator buses, active rows of the other buses, and reactive rows of the other buses. The script asserts this layout and then checks the following.
    - Every right-hand side equals −Pd/100 or −Qd/100 of its bus, exactly. This holds for all 60 rows of 0030p and all 78 rows of 0039p and 0039r, and also as an order-free multiset.
    - No balance row has a nonlinear term, so no balance row has a V² shunt term.
    - case30's shunts (Bs/100 = 0.0019 at bus 5, 0.0004 at bus 24) appear nowhere in the 0030p file. The bus-5 rows are `e511.. x58 + x77 =E= 0` and `e535.. x140 + x159 =E= 0`. The bus-24 rows are `e527 … =E= -0.087` and `e551 … =E= -0.067`, with flow terms only.
    - Each of the 150 sqr(V) coefficients in the 164 branch-flow rows of 0030p equals a pure branch quantity (g, b or b − b_c/2), so no shunt was folded into a branch.
    - case39 has no bus shunts.
  - **Floating-point confirmation by the reviewer** (independent GAMS AC OPF with IPOPT and CONOPT, `reviews/lit-network-r1/opf/`):
    - case30 as in MATPOWER: 576.8923368;
    - case30 without shunts: 576.8934134, equal to MINLPLib's p1 (576.8934135);
    - case39 with taps: 41864.17779;
    - case39 without taps: 41869.05151, equal to MINLPLib's p1.
    - The ±0.26 rad rows change none of these values.
  - **Conclusion.** powerflow0030p is MATPOWER case30 without bus shunts. powerflow0039p/r are MATPOWER case39 without tap ratios. Both are close relatives of the MATPOWER cases, not the cases themselves.
- **Angle rows.** The polar MINLPLib models contain ±0.26 rad angle-difference rows, four per branch: one `=L= 0.26` row and one `=G= -0.26` row for each orientation. That gives 164 rows in 0030p and 184 in 0039p. MATPOWER case30 and case39 have none (angmin/angmax ±360°), and neither do the rectangular models. The p and r optima coincide, and the reviewer's OPF runs give the same values with and without these rows, so the rows are not binding at the optimum.
- **Optimal values.** The MATPOWER/MIPS local optima are 576.89 (case30) and 41864.18 (case39), per Bingane et al. Table I, NESTA Table 1 and Ghaddar et al. Table 4. MINLPLib lists 576.8934135 and 41869.05151. The rest of the family follows the same pattern:
  - powerflow0009 matches case9 (5296.69; no taps, no shunts);
  - powerflow0014 lists 8082.58 against case14's 8081.53. case14 has taps 0.978, 0.969 and 0.932 and a 19 MVAr shunt at bus 9. Which of these MINLPLib drops was not checked.

**Additional per-instance FP benchmarks, checked after review r2.** The SCIP Optimization Suite 8.0 report (arXiv:2112.08872v1, Appendix A, p. 105) gives SCIP 7 / SCIP 8 gaps ∞ / 0.54% for powerflow0030r and >1000% / 0.23% for powerflow0039r, at the time limit. Müller, Serrano, Gleixner 2020 (arXiv:1903.05521v2, Table 5, pp. 69 and 72) reports both rectangular instances at the 1800 s limit in every setting. Göß 2026 (arXiv:2603.16505v1, Appendix B Table 4, p. 32) reports powerflow0039p with PARA, ε = 1e-4, time limit, dual and reported dual 4.0e2, gap and reported gap 9.90%. That scale does not match MINLPLib's primal 41869.05 and best dual 41818.28; no explanation is established and it is not used as a bound for our stored model. None of these results closes our instances.

### 3.2 powerflow0030p

- **Our claim.** Rigorous dual 576.8934122988004 against p1 = 576.8934134704; relative gap 2.0e-9. p1 is only tolerance-feasible. Best listed dual: 572.8395847 (GUROBI).
- **Prior results on the model as written:**
  - **MINLPLib powerflow0030r page:** ANTIGONE dual 576.8934129, primal 576.8934135 (FP).
  - The rectangular twin 0030r has the same data up to rounding in the 15th–16th significant digit (checked by reviewer r2); its OSIL has no shunt terms or angle rows. Under u_i = V_i cos θ_i and w_i = −V_i sin θ_i, the objective agrees. At two random rational test points, 214 of 391 rectangular rows match exactly, 60 voltage rows match through V², and the reference row w_1 = 0 corresponds to θ_1 = 0. The other 116 rows differ by up to 1.03e-13. For example, branch 27–29 stores 1.86832740213523 in 0030p versus 2 × 0.934163701067616 in a 0030r coefficient. The row tests are evidence, not a symbolic identity proof. The ideal formulation map therefore does not prove exact transfer of a bound for the rounded files.
  - MINLPLib does not transfer bounds between instances, so 0030p stays listed as open.
  - Wave 3 also certified 0030r rigorously at 576.8934126255. This bound cannot be transferred to 0030p (certificate 576.8934122988) without a perturbation argument.
- **Prior results on the close relative (MATPOWER case30 with shunts):**
  - **NESTA** (arXiv:1411.0359v6), Table 1, p. 4: case30 AC (IPOPT, local) 576.89, SDP gap 0.00% (SDPT3, FP; two decimals).
  - **Bingane, Anjos, Le Digabel 2018,** IEEE TPS 33(6):7181–7188 (arXiv:1908.02319), Table I, p. 7: case30 576.89 / 576.89; STCR, CHR and SDR gaps 0.00% (MOSEK, FP).
  - **Hijazi, Coffrin, Van Hentenryck, June 2014 revision,** Table 3, p. 18: AC 576, SDP gap 0.00%.
  - **Lavaei & Low 2012,** IEEE TPS 27(1):92–107, Section V.A, p. 10: zero duality gap observed numerically for "IEEE 30-bus" from the MATPOWER library, after adding 1e-5 p.u. resistance to transformers. The file is not named. MERL's 2012 study lists IEEE30 at 8906.14 (case_ieee30), so Lavaei–Low probably did not use these data.
  - **Kocuk, Dey, Sun 2016** (Table 4, p. 16): radial modifications of case30, which are different models.
- **Our bound does not apply to MATPOWER case30 itself.** The first version of this report said it did, which was wrong. case30 with shunts has a local solution of value 576.8923368 (reviewer's IPOPT and CONOPT runs, FP), below our bound of 576.8934123.
- **Consequence: partly known.**
  - ANTIGONE established the optimum of the model as written in floating point, on the twin 0030r.
  - The close relative with shunts was shown to be SDP-exact in floating point.
  - We found no rigorous certificate.
  - Present ours as "the first rigorous certificate found for this MINLPLib model" and "the first bound that closes the gap on the polar instance as listed", not as the first solution of an open problem.

### 3.3 powerflow0039p

- **Our claim.** Rigorous dual 41869.05148485014 against p1 = 41869.0515113202 (6.3e-10 relative). Best listed dual: 41818.27916 (GUROBI).
- **Prior results** (all FP, all on MATPOWER case39 *with taps*):
  - **Ghaddar, Mareček, Mevissen 2016,** IEEE TPS 31(1):539–546 (arXiv:1404.3626), Table 4 and Conclusion, p. 11: MATPOWER 41864.18; Lavaei–Low SDP 41862.08; second-order sparse relaxation [OP4-SH1] 41864.18 (4359 s). They "provide globally optimal solutions for the first time".
  - **NESTA Table 1, p. 4:** case39 41864.18, SOC gap 0.02%, SDP gap 0.00%.
  - **Bingane et al., Table I, p. 7:** 41864.18 / 41862.03; SOCR gap 0.02%; TCR, STCR, CHR and SDR gaps 0.01%.
  - **Hijazi et al., June 2014 revision, Table 3, p. 18:** AC 41864, QC-NLP gap 0.02%, SDP gap −0.06% (a non-valid SDP bound, as the authors say).
  - **Gopalakrishnan, Raghunathan, Nikovski, Biegler,** Allerton 2012 (MERL TR2012-088), Table I, p. 9: "NE39" 41862.10, closed to 0.1% at the root. The paper adds apparent-power line limits.
  - **Molzahn & Hiskens 2015:** only the modified cases case39Q and case39L. Josz et al. 2015 do not treat case39.
  - No source reports results for the tap-free model or the value 41869.05.
- **Consequence: new as far as found** for the model as written. Caveats for the paper:
  - the instance is a tap-free variant of MATPOWER case39, whose unmodified version was solved globally in FP;
  - the published SDP gap of case39 (about 5e-5 relative) matches the plain-SDP gap we saw on the tap-free model (3e-5 relative).

### 3.4 powerflow0039r

- **Our claim.** Rigorous dual 41869.05148327243 against p1 = 41869.0515113208 (6.7e-10 relative). Best listed dual: 41804.88153 (GUROBI); BARON 41265.71 and SCIP 41793.40 are also listed.
- **Prior results:** as for 0039p. The rectangular model has no angle rows.
- **Consequence:** new as far as found, with the same caveats.

## 4. KAN family

### 4.1 Provenance (all six instances)

- **MINLPLib pages.** Description: "Optimization of a trained Kolmogorov-Arnold Network as a surrogate model of the 3-dimensional [5-dimensional] Rosenbrock function". They cite Karia, Lastrucci, Schweidtmann, Tech. Rep. 2025. Added on 07 May 2025.
- **Source.** arXiv:2503.02807 v1 (4 Mar 2025), the only version on 2026-10-01. The arXiv page shows no journal reference, and OpenAlex lists only the arXiv record. Supplement: Zenodo 14961066 (DOI 10.5281/zenodo.14961066).
- **Exact identification:**
  - Table 5 (p. 19) varies the number of hidden neurons n1 at a fixed grid: 12 points for n0 = 3 and 6 for n0 = 5 (Table 2, p. 16). This matches the 18 and 12 knot intervals found in wave 3.
  - In the Zenodo sheets "KAN-Default", the rows R3_H1_N4, R3_H1_N5, R3_H1_N9, R5_H1_N3, R5_H1_N5 and R5_H1_N8 have exactly the MINLPLib counts: 1129/1478, 1410/1847, 2534/3323, 838/1121, 1392/1867 and 2223/2986. The SCIP logs also give 288/360/648/216/360/576 integer variables (reviewer).
  - So each MINLPLib instance is the paper's Default-configuration model. The ConvexHull, ExploitSparsity, LocalSupport, Redundant and McCormick configurations are reformulations of the same networks. The best-KAN rows of Table 9 (p. 22) use ExploitSparsity.
  - MINLPLib has no other formulation of these six networks. The other KAN instances, kan_r3_h1_n3 and kan_peaks_*, are different networks.
- **Solver settings in the source** (p. 16): SCIP 9.0.1 via ASL/Pyomo, gap tolerance 0 and 2 h limit. The 1e-6 feasibility tolerance is inferred from the checked Default R3_H1_N4.log, not stated on p. 16: R3_H1_N4.log reads only limits/time = 7200 from scip.set, so the SCIP default applies. All results are FP.
- **Model scale.** The objective is A·y + B with A = 970.2192 (r3) or 1439.6299 (r5). Row violations at SCIP's tolerance can therefore move the objective by about 1e-3.
- **Other KAN-optimization papers checked:** Karia et al., ESCAPE 35, Syst. Control Trans. 4:1371–1376 (2025), DOI 10.69997/sct.195815 (auto-thermal reforming case); Li et al., arXiv:2604.03871 (2026), on polynomial KANs. Neither uses these networks.
- **Evaluation at SCIP's points.**
  - The values "at SCIP's input" below are 60-digit forward evaluations of the MINLPLib network at the reported input point.
  - The first author's script (`checks/kan_scip_points.py`) reuses the wave-3 code and assumes the input order.
  - The reviewer reproduced all values with an independent OSIL reader, and confirmed the input order by a permutation test (`reviews/lit-network-r1/kan_points.py`, `kan_points_perm.log`).
  - These are high-precision numerical evaluations, not proofs. The differences they show (4e-4 to 2e-3) are far above any rounding effect.

### 4.2 kan_r3_h1_n4

- **Our claim.** min over R ≥ 0.0027812371525814; a point reaches 0.0027812372214418. Listed: primal 0.00278124, dual 0.0003908 (GUROBI).
- **Prior result (FP claim).**
  - Table 5: n0 = 3, n1 = 4, solved in 3459 s.
  - Zenodo, sheet KAN-Default, row R3_H1_N4, and log `kan_effect_neurons/Default/R3_H1_N4.log`: "problem is solved [optimal solution found] … Primal Bound +1.08116412047821e-03 … Dual Bound +1.08116412047821e-03 … Gap 0.00 %". The reported input is x = (0.9906497023689892, 0.9811896067856135, 0.9633031313414224).
  - The other configurations report "optimal" values 7.98e-4 (ConvexHull), 9.10e-4 (ExploitSparsity; the "PB = DB = 0.00091" of Table 9), 1.006e-3, 1.049e-3 and 1.064e-3.
- **Checks.**
  - At SCIP's input, the MINLPLib model gives 0.0028684784; the non-partition rows hold to about 1e-60. This is 1.79e-3 above SCIP's claim.
  - At the ConvexHull run's input, it gives 0.0028269615 (reviewer).
  - With the inputs fixed at the Default point, SCIP 10.0 returns "optimal" 0.0026959290. 38 rows are violated by more than 1e-9, and the largest violation is 9.3e-7 (reviewer, `reviews/lit-network-r1/kan_scip_fixed.log`).
- **Consequence: prior FP claim contradicted.** Every published optimal value lies below a certified lower bound of R, and R contains every exactly feasible point and the intended network. Our certificate is new.

### 4.3 kan_r3_h1_n5

- **Our claim.** min over R ≥ −0.011042679521782; a point reaches −0.011042679414487. Listed: primal −0.01104268, dual −0.01302849 (GUROBI).
- **Prior result.**
  - Table 5: n1 = 5, solved in 5038 s.
  - Zenodo Default: "optimal", PB = DB = −1.30809958982354e-2.
  - Other configurations: −1.3104e-2, −1.3334e-2, −1.2561e-2 and −1.3476e-2 (all "optimal"). Redundant hit the time limit (PB −1.2882e-2, DB −2.6465e-2).
- **Checks.**
  - At SCIP's input, the exact network gives −0.0108512435, which is 2.23e-3 above the claim.
  - With the inputs fixed there, SCIP 10.0 returns "optimal" −0.0113202912. 90 rows are violated by more than 1e-9, and the largest violation is 1.0e-6 (reviewer).
- **Consequence:** prior FP claim contradicted; ours new.

### 4.4 kan_r3_h1_n9

- **Our claim.** min over R ≥ 0.012963659963475; a point reaches 0.012963660053039. Listed: primal 0.01296366, dual 0.0081425 (GUROBI).
- **Prior result.** All six configurations hit the time limit. Best dual −11.376 (Default); best primal 0.17527 (ExploitSparsity).
- **Consequence:** new as far as found.

### 4.5 kan_r5_h1_n3

- **Our claim.** min over R ≥ −262.86422590922; a point reaches −262.86422588507, better than the listed −262.3058993. Listed dual: −789.740197 (GUROBI).
- **Prior result.** Time limit. Best dual −1587.43 (ExploitSparsity); best primal −56.63. Default gave PB 513.31 and DB −2048.02.
- **Consequence:** new as far as found.

### 4.6 kan_r5_h1_n5

- **Our claim.** min over R ≥ 0.27258325385485; a point reaches 0.27258325395662. Listed: primal 0.27265451, dual 0.26787523 (GUROBI).
- **Prior result.**
  - Table 9: this is the best KAN for n0 = 5 (ExploitSparsity), with "PB 0.27, DB 0.19" at the time limit.
  - Zenodo: ExploitSparsity PB 0.273482, DB 0.186687 (the best dual); ConvexHull PB 0.272518774, DB 0.183360.
- **Tolerance artifact.** The ConvexHull primal is below our minimum of R. At its input, the exact network gives 0.2729243.
- **Consequence:** new as far as found. The published primal 0.27252 is not attainable exactly.

### 4.7 kan_r5_h1_n8

- **Our claim.** min over R ≥ 0.069327860510525; a point reaches 0.069327860606191. Listed: primal 0.36062128, dual −45.00462396 (GUROBI).
- **Prior result.** Time limit. Best dual −122.67 (ConvexHull); best primal 0.214075 (ConvexHull), which is consistent with our bound.
- **Consequence:** new as far as found (dual and primal).

## 5. Water network operation (waterno2)

### 5.1 Provenance (all five instances)

- **MINLPLib pages** (application "Water Network Operation"; added on 12 Aug 2014) cite two sources:
  - Huang W., "Operative Planning of Water Supply Networks by Mixed Integer Nonlinear Programming", MSc thesis, FU Berlin, 2011 (not obtained);
  - Gleixner, Held, Huang, Vigerske, NACO 2(4):695–711 (2012), DOI 10.3934/naco.2012.2.695 (ZIB-Report 12-25).
- **The NACO paper is stationary only** (ZIB-Report pp. 3–4, 7, 15–18).
  - It studies the problem "at a fixed point in time" on two Siemens networks: n25p22a18 (4 tanks, 12 pumps, 6 valves) and n88p64a64 (11 tanks, 55 pumps).
  - All pumps run at "a single fixed constant speed" (p. 7).
  - SCIP 2.1.1 solved all 16 scenarios to 1e-6 (Tables 3–4, p. 18).
  - waterno2 matches neither network.
- **Source network: Tsinghua n9p3a11.**
  - Source: Huang W., "Optimal Operation of Water Supply Networks by Mixed Integer Nonlinear Programming and Algebraic Methods", Dissertation, TU Darmstadt, 2019, urn:nbn:de:tuda-tuprints-86575, CC BY-SA 4.0. It was read from the Internet Archive copy, because tuprints is behind a bot check.
  - Section 5.5 (pp. 119–127), p. 122: The thesis describes n9p3a11, a Tsinghua University network with one reservoir, three tanks and five junctions, two consumers, three pipes, nine variable-speed pumps and two valves. It uses hourly demands over a day.. Pump power is a bivariate cubic in flow and speed (eq. 5.23).
  - p. 123, Example 5.41: one pump's power is 25.9267 ω³ + 18.1348 ω² Q + 22.1276 ω Q² − 42.6895 Q³ on [0.85, 1.0] × [0.4, 0.7].
  - **Match** (`checks/waterno2_huang_match.py`). The coefficients 25.92674585, 18.13482123, 22.12766012 and −42.68950769 occur in every waterno2 OSIL file exactly 2 × (number of periods) times. They agree with the printed values after truncation to four decimals.
  - The network (3 tanks, 9 variable-speed pumps, cubic pump power) also matches the wave-2 description of waterno2: station A with 3 pumps, stations B1 and B2 with 2 each, and station D with 2.
- **Multi-period results in Huang 2019** (Table 5.2, p. 126; SCIP 5.0.1, 1 h, gap limit 1e-5; P[0,i] = the first i hours; FP):

  | periods | MINLPLib primal (waterno2_xx) | Huang "original": primal / dual | Huang extended-model columns: primal / dual |
  |---|---|---|---|
  | 1 | 19.45668046 | 19.46 / 19.46 | 19.38 / 19.38 |
  | 2 | 39.57142193 | 39.57 / 39.57 | 39.5 / 39.5 |
  | 3 | 115.0045167 | 215 / 215 | 215 / 215 |
  | 4 | 145.4397918 | 247.63 / 247.63 | 247.63 / 247.63 |
  | 6 | 282.8880374 | 456 / 163.65 | 404.81 / 343.41 |
  | 9 | 922.5952898 | 1113.14 / 238.28 | 1115 / 727.98 |
  | 12 | 2263.358374 | 2603.85 / 461.55 | 2669.16 / 1451.5 |
  | 18 | 5269.638815 | 5909.72 / 504.07 | 5636.12 / 2970.92 |
  | 24 | 7332.721691 | 8380.79 / 454.64 | 8271.19 / 4070.3 |

  - The "original" column's 1- and 2-period optima agree with MINLPLib's to the printed digits. The extended-model column gives 19.38 and 39.5 instead, so its equivalence to the original model is not established.
  - From 3 periods on, they do not. Huang's 3-period optimum is 215 (gap 0), while waterno2_03's is 115.0045 (closed by several solvers on MINLPLib). So Huang's multi-period models differ from the MINLPLib instances.
  - The dissertation does not say why. It mentions model corrections (p. 129), and MINLPLib's instances predate it.
  - Huang's extended-model 6-period dual 343.41 is not used as evidence against the MINLPLib model: the relation between the extended and original feasible sets is not established. The original 3-period closed value 215 versus 115.0045 already establishes a model mismatch.
  - None of Huang's runs with 5 or more periods closed the gap. The dissertation states that for 24 periods "the dual gap cannot verify the solution quality" (abstract, p. v).
- **State of the problem.** D'Ambrosio, Lodi, Wiese, Bragalli, EJOR 243(3):774–788 (2015), Section 5.2 (preprint p. 13): "there is no successful solution for this complete [time-discretized] form in the literature". They add that the NACO authors found "two or three time periods ... troublesome" with SCIP (Gleixner, private communication, 2013).
- **Benchmarks.** Mittelmann's 200-instance MINLPLib benchmark and the JOGO SCIP 8 paper's test set contain only waterno2_02 and waterno2_03 from this family. The separate SCIP Optimization Suite 8.0 report does include 06/09/12/18/24; SCIP 7 / SCIP 8 time-limit gaps are 326% / 128%, >1000% / 321%, >1000% / 571%, >1000% / 638%, and >1000% / 750% (Appendix A, p. 112). Müller, Serrano, Gleixner 2020 also report waterno2_04–24 at the 1800 s limit in all tested settings (arXiv:1903.05521v2, Table 5, pp. 69 and 72). These are checked FP results with no closure.
- **Primal-only results.** Geißler, Morsi, Schewe, Schmidt, SIAM J. Optim. 27(3):1611–1636 (2017) (Optimization Online 2016/04/5399, Appendix B Table 2, pp. 47–48) give heuristic primal values. All are worse than the listed ones.

### 5.2–5.6 Per instance

All five are **new as far as found**. Huang's 2011 MSc thesis, which MINLPLib cites, was not seen. Huang's 2019 dissertation was read: its multi-period results concern related models and close none of them.

| instance | our rigorous dual | primal (gap) | best listed dual | prior results found |
|---|---|---|---|---|
| waterno2_06 | 278.230573 | 282.888038, listed (≤ 1.68%) | 165.1903 (SCIP) | MINLPLib solver bounds (ANTIGONE 89.07, BARON 107.95, COUENNE 94.21, GUROBI 162.19, LINDO 34.03, SCIP 165.19, SHOT 0, XPRESS 108.40); Geißler et al. primal 442.50; Huang 2019 extended related model: dual 343.41, gap 0.18 |
| waterno2_09 | 824.834692 | 914.012, ours (≤ 10.82%) | 273.8958 (SCIP) | Geißler et al. primal 1422.16; Huang 2019 related model: gap 0.53 |
| waterno2_12 | 2089.754565 | 2233.821346, ours (≤ 6.90%) | 479.5051 (GUROBI) | Geißler et al. primal 3119.55; Huang 2019 related model: gap 0.84 |
| waterno2_18 | 4790.820715 | 5023.983, ours (≤ 4.90%) | 770.7362 (SCIP) | Geißler et al. primal 7359.11; Huang 2019 related model: gap 0.90 |
| waterno2_24 | 6576.151388 | 6963.795181, ours (≤ 5.90%) | 1095.1265 (SCIP) | Geißler et al. primal 9711.81; Huang 2019 related model: gap 1.03 |

## 6. ann_cumene_tanh

- **Provenance.**
  - The MINLPLib page (added on 29 Nov 2021) cites Schweidtmann & Mitsos, JOTA 180(3):925–948 (2019), DOI 10.1007/s10957-018-1396-0. arXiv:1801.07114v2 (15 Oct 2018, comment "J Optim Theory Appl (2018)") was read; the JOTA page needs cookies.
  - Section 5.4 (pp. 20–21) describes 14 tanh MLPs from Schultz et al.'s Aspen model, 5 decision variables with box bounds, and one constraint, cumene purity ≥ 0.999. The full-space problem has "794 variables, 789 equality and 1 inequality constraints".
  - MINLPLib's instance has 794 variables, 790 constraints (789 E, 1 L), native tanh, 5 inputs and the 0.999 purity bound. It is that full-space problem written with tanh directly.
- **The twin ann_cumene_exp.** Its MINLPLib page (added on 29 Nov 2021) says: "In this variant of ann_cumene_tanh, the tanh(x) activation function has been replaced by 1-2/(exp(2x)+1) (form 3 in paper)".
  - **Identity, proved.** `checks/cumene_twin_exact.py` compares the two cached OSIL files:
    - the variables, bounds, objective, and linear and quadratic coefficients are byte-identical;
    - each of the 250 nonlinear rows is −tanh(v) in one file and 2/(exp(2v)+1) in the other, with the same v, and its row bounds are raised by exactly 1 (exact rationals);
    - all other rows are identical.

    Since −tanh(v) = 2/(exp(2v)+1) − 1 for every real v, the two problems have the same feasible set and objective. The reviewer's independent script (`reviews/lit-network-r1/cumene_twin.py`) reaches the same result.
  - **Listed bounds.** The page was fetched on 2026-10-01 and 2026-10-02, and matches the 2026-09-30 copy in `bound-audit/pages/`.
    - Primal: −3379.982394 (infeas 2e-10).
    - Duals: −3379.982394 (SCIP, last updated 15 Feb 2022); −3379.982394 (LINDO, 15 Feb 2022); −3379.985774 (BARON, 31 Jul 2025); −73920.54157 (ANTIGONE, 15 Feb 2022).
    - The ann_cumene_tanh page lists the same primal value and no dual. A likely reason is that not all solvers that MINLPLib runs accept tanh; this was not checked.
- **Results in arXiv:1801.07114v2 (FP).** Table 4 (p. 21) and Fig. 6 (p. 22); these figures are not attributed to the unchecked JOTA publisher table:
  - BARON 17.4.1 (full space, forms F1–F4, including the exp form F3 used by ann_cumene_exp) ran 1e5 s with absolute gap 1·10^20 for all four forms. The text says BARON "does not improve its initial lower bound on the objective at all", so it gave no useful lower bound.
  - MAiNGO (reduced space) ended with absolute gaps 1·10^11 (F3), 8·10^10 (envelope) and 1·10^5 (envelope*, a setting in which the upper bound comes from function evaluation). The F1, F2 and F4 runs crashed.
  - Fig. 6 shows the upper bound at about −3×10³ (read from the plot) and the best lower bound at about −10⁵ after 10⁵ s. The paper says "none of the tested solution approaches converge".
  - The 2021 dissertation, "Global Optimization of Processes through Machine Learning" (DOI 10.18154/RWTH-2021-05536), says Chapter 2 is based on the JOTA paper and reprints it with permission. Table 2.8 (printed p. 29, PDF p. 43) reports different MAiNGO results after 100000 s: F3 4,671,260 iterations / gap 2930; envelope 6,329,810 / 444; envelope* 10,033,800 / 328. BARON gaps remain 1e20. The arXiv iteration counts are 4,772,133 / 5,683,103 / 12,939,508. The publisher full text is still unchecked, so neither set is called "the JOTA result" here. Both sources report no convergence, so the status is unchanged.
  - In both checked versions no method closed the problem. The later floating-point closure is the one MINLPLib lists for the exp twin (SCIP and LINDO results last updated 15 Feb 2022).
- **Related but different model.** Izquierdo González, Adeogun, Yin, Charitopoulos, Syst. Control Trans. 5:1793–1800 (2026), DOI 10.69997/sct.139045, pp. 1796–1797, solve a cumene problem globally with a new ANN (7 inputs, five hidden layers 16→32→32→32→16).
- **Checked, not used here.** Wilhelm, Wang, Stuber (JOGO 2023) and Carrasco & Muñoz (2026) do not mention this instance or cumene.
- **Our claim.** Rigorous −3386.5403 (gap 0.194%) against −3379.9824.
- **Consequence: partly known.**
  - SCIP and LINDO closed the identical problem in floating point (dual equal to the primal −3379.982394), and BARON's dual is within 3.4e-3.
  - Our bound is the first rigorous one found, but it is weaker than these floating-point claims.
  - The paper and `open-instances-summary.md` (which says "the first finite dual") must say so.

## 7. Checks run by this track (targeted only)

All scripts are in `checks/`, each with a `.log` next to it. `minor_review_check.py` and its log record the saved-source checks added for the minor-fix revision. Results from GAMS, IPOPT, CONOPT or SCIP are floating-point evidence, not proofs.

- **`python3 checks/kan_scip_points.py`** (first author; 2.6 s). It uses the wave-3 functions `kan_model.decode` and `kan_check.full_point` with 60-digit mpmath.
  - Values at SCIP's inputs: r3_n4 0.0028684784 (claim 1.0812e-3); r3_n5 −0.0108512435 (claim −1.3081e-2); r5_n5 0.2729243 (ConvexHull primal 0.2725188).
  - **Not independent** of the wave-3 code. It also assumes that the paper's x_i map to the ±2.048-bounded input copies in increasing OSIL index order.
  - The reviewer's independent reproduction (own OSIL reader) gives the same values to all printed digits. Its permutation test shows that only this order matches SCIP's values at time-limited runs.
  - This is numerical evidence, not a proof; the proof is our verified certificate.
- **`python3 checks/powerflow_data_match.py`** (first author). Checks costs, limits, thermal limits, taps and line charging, as in Section 3.1. It is a coefficient-presence check and does not map branches one by one.
- **`python3 checks/powerflow_loads_shunts.py`** (revision; exact rationals; 0.2 s).
  - Results: loads match row by row for 0030p, 0039p and 0039r. No balance row has a nonlinear term. case30's two shunt values occur nowhere in the 0030p file. All 150 sqr(V) coefficients of the 0030p branch-flow rows are pure branch quantities.
  - The first run used a wrong assumption about the order of the balance rows and reported mismatches. After the layout was fixed (four blocks, see the script), every check passes. The order-free multiset comparison of loads passed in both runs.
- **`python3 checks/cumene_twin_exact.py`** (revision; exact; 0.5 s). Shows that ann_cumene_exp ≡ ann_cumene_tanh, as in Section 6.
- **`python3 checks/waterno2_huang_match.py`** (revision; 0.2 s). Huang's Example 5.41 coefficients occur 2 × T times in each waterno2_T file; produces the table in Section 5.1.
- **Other steps (first author):**
  - converted the Zenodo xlsx sheets to TSV (`sources/zenodo_kan/*.tsv`);
  - extracted the Default-configuration logs (`sources/zenodo_kan/ex/`);
  - re-fetched the 16 MINLPLib pages on 2026-10-01; all were unchanged against the cached pages;
  - ran pdftotext on every PDF;
  - spaced downloads at least 1 s apart.
- This track ran no solver and started no background jobs. The OPF and SCIP 10 runs quoted above are the reviewer's (`reviews/lit-network-r1/`).

## 8. Searches and limits

- **Web searches (first version):**
  - instance names: ann_cumene_tanh, the kan_* names, waterno2 and waterno2_06–24;
  - the KAN, water and ANN source papers, Huang's thesis and dissertation, and KAN optimization work from 2025–2026;
  - case values: "41864.18", "41869.05" and "576.89" with SDP;
  - Lavaei–Low, the 2013 Hijazi report, QPLIB powerflow, Octeract's MINLPLib claims, and rigorous (VSDP) SDP bounds for OPF.
- **Citation trails (OpenAlex):** works citing Schweidtmann–Mitsos that mention "cumene" (2 hits, 1 relevant); works citing Karia et al. (0 indexed).
- **Benchmarks:**
  - Mittelmann's MINLPLib benchmark: none of our 15;
  - the JOGO SCIP 8 paper's test set: none of our 15. The separate SCIP Optimization Suite 8.0 report includes the five water instances and powerflow0030r/0039r with time-limit gaps, so "SCIP 8 test set" without a source qualifier is too broad;
  - QPLIB: original names are not shown; r2 found no solution value near 576.89 or 41869.05 in qplib.solu. This is evidence only, not an identity proof;
  - Octeract: its claims concern other instances.
  - SCIP Optimization Suite 8.0 Appendix A, Müller–Serrano–Gleixner 2020 and Göß 2026 were checked for our instance names and added to the relevant power-flow and water sections above. All are time-limit FP results; none gives a closure. The inconsistent Göß powerflow0039p scale is explicitly retained as a caveat.
- **Added in the revision:**
  - **MINLPLib variants of our instances.** The cached OSIL list contains ann_cumene_exp (twin of ann_cumene_tanh, Section 6) and powerflow0030r (twin of 0030p, Section 3.2). There are no other formulations of the six KAN networks or of waterno2; the other waterno2_T instances are different horizons of the same network.
  - **Internet Archive.** Availability and CDX queries for Optimization Online 2013/09/4057 found one PDF snapshot (2015-12-24). Queries for tuprints 8657 found PDF snapshots from 2022-10-06 and 2024-04-14; the 2024 one was downloaded.
  - **Other searches.** Web searches for Huang 2019 and Huang 2011; an OpenAlex search (no record of the dissertation); the ZIB OPUS listing for author Wei Huang (only the NACO paper).
- **Not obtained:**
  - **Huang's 2011 MSc thesis** (FU Berlin), which MINLPLib cites for waterno2. It may hold multi-period results on the model as written. This is the remaining gap behind "new as far as found" for waterno2.
  - **The September 2013 first version of the Hijazi et al. report** (not archived). It could hold an FP bound for the tap-free or shunt-free models.
  - **The publisher versions of the JOTA, IEEE and NACO papers** (preprints were used instead). The Schweidtmann 2021 dissertation is obtained and checked, but its table does not settle which numbers the publisher version prints.
  - **The AIChE 2025 Annual Meeting abstract "Multi-layer perceptrons or Kolmogorov–Arnold networks…"** from the KAN source group (proceedings.aiche.org): the review encountered a Cloudflare check and found no Internet Archive copy. It may report further Rosenbrock-surrogate runs, so it remains an explicit search limitation.
- An unsuccessful search does not establish novelty.
- **Prior certified OPF work to cite.** Oustry, D'Ambrosio, Liberti, Ruiz, "Certified and accurate SDP bounds for the ACOPF problem", PSCC 2022 / Electr. Power Syst. Res. 212:108278, DOI 10.1016/j.epsr.2022.108278, HAL hal-03613385. It reports certified SDP lower bounds for PGLib-OPF v21.07 TYP cases. The [authors' result table](https://github.com/aoustry/dualACOPFsolver) gives certified lower bounds 803.127 (case30_as), 7896.87 (case30_ieee) and 137254 (case39_epri), different from MINLPLib's 576.89 / 41869.05 models. This is relevant prior certified-bound work, not a closure of these MINLPLib instances. We have not audited its control of rounding errors.
- **Method to cite.** VSDP (Jansson et al., https://www.tuhh.de/ti3/jansson/vsdp_cj.html) does rigorous interval post-processing of SDP solutions; our powerflow certificate follows the same idea. Not read in detail.

## 9. Recommendations for the paper

1. **KAN.** Report that the source paper's SCIP "optima" for r3_n4 and r3_n5 lie below the certified minimum of R. Explain the tolerance and scale mechanism and show the values at SCIP's points. The reviewer's SCIP 10 fixed-input runs can be added. Keep the claim about R.
2. **powerflow0030p.**
   - Call it "the first rigorous certificate found for this MINLPLib model" and "the first bound that closes the gap on the polar instance as listed".
   - Cite ANTIGONE on 0030r for FP closure via the nearly identical rounded twin; state the coefficient-rounding caveat and do not transfer a rigorous bound without a perturbation argument. Cite Oustry et al. 2022 for prior certified bounds on different PGLib models.
   - State that the MINLPLib model drops case30's two bus shunts, so NESTA Table 1, Bingane Table I and Hijazi et al. (2014) Table 3 concern a close relative.
   - Do not say that our bound applies to MATPOWER case30.
3. **powerflow0039p/r.**
   - State that MINLPLib drops MATPOWER's tap ratios.
   - Cite Ghaddar et al. 2016 Table 4 for the FP global solution of the unmodified case.
   - Cite NESTA Table 1, Bingane Table I and Hijazi et al. (2014) Table 3 for the FP SDP gaps. The last one reports a non-valid, negative gap, a useful example of why rigorous bounds matter.
4. **waterno2.**
   - Present it as new as far as found.
   - Cite D'Ambrosio et al. 2015 for the multi-period state of the art.
   - Cite Huang 2019 (Section 5.5, Table 5.2) as the source network, with unclosed multi-period results on related models.
   - Say that Huang's 2011 thesis was not accessible.
5. **ann_cumene_tanh.**
   - Present it as partly known: SCIP and LINDO closed the identical MINLPLib twin ann_cumene_exp in floating point; ours is the first rigorous bound, at gap 0.194%.
   - Do not call our bound "the first finite dual" without this context.
   - Cite Schweidtmann & Mitsos arXiv v2 (Table 4, Fig. 6) for that baseline, alongside the different 2021 dissertation Table 2.8. The publisher table remains unchecked.

## 10. Bibliography

- Bestuzheva, Chmiela, Müller, Serrano, Vigerske, Wegscheider, "Global Optimization of Mixed-Integer Nonlinear Programs with SCIP 8", J. Global Optim. 91:287–310 (2025); arXiv:2301.00587v1.
- Bestuzheva et al., "The SCIP Optimization Suite 8.0", ZIB-Report 21-41 (2021); arXiv:2112.08872v1, Appendix A.
- Bingane, Anjos, Le Digabel, "Tight-and-Cheap Conic Relaxation for the AC Optimal Power Flow Problem", IEEE TPS 33(6):7181–7188 (2018), DOI 10.1109/TPWRS.2018.2848965; arXiv:1908.02319.
- Carrasco, Muñoz, "Tightening convex relaxations of trained neural networks: a unified approach for convex and S-shaped activations", arXiv:2410.23362v2 (2026; first version 2024).
- Coffrin, Gordon, Scott, "NESTA, The NICTA Energy System Test Case Archive", arXiv:1411.0359v6.
- D'Ambrosio, Lodi, Wiese, Bragalli, "Mathematical Programming techniques in Water Network Optimization", EJOR 243(3):774–788 (2015), DOI 10.1016/j.ejor.2014.12.039.
- Geißler, Morsi, Schewe, Schmidt, "Penalty Alternating Direction Methods for Mixed-Integer Optimization: A New View on Feasibility Pumps", SIAM J. Optim. 27(3):1611–1636 (2017), DOI 10.1137/16M1069687.
- Ghaddar, Mareček, Mevissen, "Optimal Power Flow as a Polynomial Optimization Problem", IEEE TPS 31(1):539–546 (2016), DOI 10.1109/TPWRS.2015.2390037.
- Gleixner, Held, Huang, Vigerske, "Towards globally optimal operation of water supply networks", NACO 2(4):695–711 (2012), DOI 10.3934/naco.2012.2.695; ZIB-Report 12-25.
- Gopalakrishnan, Raghunathan, Nikovski, Biegler, "Global Optimization of Optimal Power Flow Using a Branch & Bound Algorithm", Allerton 2012, pp. 609–616, DOI 10.1109/Allerton.2012.6483274.
- Göß, "Clash of MINLP Relaxations: Piecewise Linear vs. Global Parabolic", arXiv:2603.16505v1 (17 March 2026).
- Hijazi, Coffrin, Van Hentenryck, "Convex Quadratic Relaxations for Mixed-Integer Nonlinear Programs in Power Systems", Optimization Online 2013/09/4057. June 2014 revision read from the Internet Archive (snapshot 2015-12-24). Published as Math. Prog. Comp. 9(3):321–367 (2017), DOI 10.1007/s12532-016-0112-z.
- Huang W., "Operative Planning of Water Supply Networks by Mixed Integer Nonlinear Programming", MSc thesis, FU Berlin, 2011 (not obtained).
- Huang W., "Optimal Operation of Water Supply Networks by Mixed Integer Nonlinear Programming and Algebraic Methods", Dissertation, TU Darmstadt, 2019, urn:nbn:de:tuda-tuprints-86575, https://tuprints.ulb.tu-darmstadt.de/8657/.
- Izquierdo González, Adeogun, Yin, Charitopoulos, "Nonconvex Robust Optimization for Process Design with Artificial Neural Networks Embedded", Syst. Control Trans. 5:1793–1800 (2026), DOI 10.69997/sct.139045.
- Jansson, "VSDP: Verified SemiDefinite Programming", User's Guide (2006), and Jansson, Chaykin, Keil, "Rigorous error bounds for the optimal value in semidefinite programming" (2007). Official package: https://www.tuhh.de/ti3/jansson/vsdp_cj.html; paper preprint: https://optimization-online.org/wp-content/uploads/2005/01/1047.pdf.
- Josz, Maeght, Panciatici, Gilbert, "Application of the Moment–SOS Approach to Global Optimization of the OPF Problem", IEEE TPS (2015); arXiv:1311.6370v2.
- Karia, Lastrucci, Schweidtmann, "Deterministic Global Optimization over trained Kolmogorov Arnold Networks", arXiv:2503.02807v1 (2025), supplement Zenodo 14961066.
- Karia, Lastrucci, Schweidtmann, "Kolmogorov Arnold Networks (KANs) as surrogate models for global process optimization", Syst. Control Trans. 4:1371–1376 (2025), DOI 10.69997/sct.195815.
- Kocuk, Dey, Sun, "Inexactness of SDP Relaxation and Valid Inequalities for Optimal Power Flow", IEEE TPS 31(1):642–651 (2016), DOI 10.1109/TPWRS.2015.2402640.
- Lavaei, Low, "Zero Duality Gap in Optimal Power Flow Problem", IEEE TPS 27(1):92–107 (2012), DOI 10.1109/TPWRS.2011.2160974.
- Li, Ovalle, Poczos, Laird, Grossmann, Peña, "Efficient Convexification of Kolmogorov-Arnold Networks with Polynomial Functional Forms Via a Continuous Graham Scan Approach", arXiv:2604.03871v1 (2026).
- MATPOWER case files (github.com/MATPOWER/matpower, master); Zimmerman, Murillo-Sánchez, Thomas, "MATPOWER: Steady-State Operations, Planning, and Analysis Tools for Power Systems Research and Education", IEEE TPS 26(1):12–19 (2011).
- MINLPLib instance pages for ann_cumene_exp, ann_cumene_tanh, powerflow0030r and the 15 instances of this track (https://www.minlplib.org/<name>.html; copies in `sources/`).
- Mittelmann, "Mixed Integer Nonlinear Programming Benchmark", https://plato.asu.edu/ftp/minlp.html (snapshot checked 26 February 2026).
- Molzahn, Hiskens, "Sparsity-Exploiting Moment-Based Relaxations of the Optimal Power Flow Problem", IEEE TPS 30(6):3168–3180 (2015), DOI 10.1109/TPWRS.2014.2372478.
- Müller, Serrano, Gleixner, "Using Two-Dimensional Projections for Stronger Separation and Propagation of Bilinear Terms", SIAM J. Optim. 30(2):1339–1365 (2020), DOI 10.1137/19M1249825; arXiv:1903.05521v2.
- Oustry, D'Ambrosio, Liberti, Ruiz, "Certified and accurate SDP bounds for the ACOPF problem", PSCC 2022 / Electr. Power Syst. Res. 212:108278 (2022), DOI 10.1016/j.epsr.2022.108278; HAL hal-03613385; https://github.com/aoustry/dualACOPFsolver.
- Schweidtmann, Mitsos, "Deterministic Global Optimization with Artificial Neural Networks Embedded", JOTA 180(3):925–948 (2019), DOI 10.1007/s10957-018-1396-0; arXiv:1801.07114v2. Numerical Table 4 and Fig. 6 readings here are from arXiv v2; the publisher table was not obtained.
- Schweidtmann, "Global Optimization of Processes through Machine Learning", Dissertation, RWTH Aachen, 2021, DOI 10.18154/RWTH-2021-05536; Table 2.8, printed p. 29 / PDF p. 43 (Internet Archive 2026-01-28 copy).
- Vigerske, "Decomposition in Multistage Stochastic Programming and a Constraint Integer Programming Approach to Mixed-Integer Nonlinear Programming", dissertation, HU Berlin (2013), DOI 10.18452/16704.
- Wilhelm, Wang, Stuber, "Convex and Concave Envelopes of Artificial Neural Network Activation Functions for Deterministic Global Optimization", JOGO 85(3):569–594 (2023), DOI 10.1007/s10898-022-01228-x.

## 11. Revision after review round 1 (2026-10-02)

Review: `publication/reviews/lit-network-review-r1.md` (3 major and 6 minor issues). Every issue was accepted; none is disputed.

| # | issue | what was done |
|---|---|---|
| M1 | ann_cumene_tanh: missed the identical twin ann_cumene_exp, which is closed in FP | Proved the identity again with independent exact code (`checks/cumene_twin_exact.py`) and re-ran the reviewer's script (same result). Saved the ann_cumene_exp page (same sha256 as the reviewer's copy). Changed the status to "partly known" in Sections 1, 2, 6 and 9. Recorded the solver dates, and that BARON's 2018 failure was on the same exp form. Flagged "the first finite dual" in `open-instances-summary.md` for correction (not edited here, because it is outside this track's folder). |
| M2 | powerflow0030p: MINLPLib drops case30's two bus shunts, and the data check had not compared loads or shunts | Wrote a new exact check, `checks/powerflow_loads_shunts.py`. Loads match row by row for all three instances; 0030p has no shunt terms anywhere, including folded into branch rows; case39 has no shunts. Corrected the provenance in Sections 1, 2, 3.1 and 3.2. "Partly known" now rests on ANTIGONE's dual for the twin 0030r, as tolerance-level evidence from the nearly identical rounded twin. Round 2 supersedes the exact bound-transport claim: the files differ in the 15th–16th significant digit, so rigorous transport needs a perturbation argument. NESTA, Bingane and Hijazi et al. are now cited as results on a close relative. Withdrew the first version's remark that our bound is also a bound for MATPOWER case30: case30 with shunts has a local solution at 576.8923368 (reviewer's FP OPF), below our bound. |
| M3 | report.md missing; the copy given to the reviewer was truncated | Recovered the first author's full text (29,061 characters) from the author's returned output and worked all corrections into it. The tool environment again rejected writing report.md, so the complete text, including the per-instance sections, search log, checks, limits and commands, is returned in full for the root to save exactly as given. |
| m1 | The source report of the powerflow models can be obtained (June 2014 revision, via the Internet Archive) | Downloaded it independently (sha256 equals the reviewer's copy) and cited it: the Section 6 setup and footnote 1 (taps, shunts, θu = π/12), Table 1 and Table 3. A CDX query confirmed that the Internet Archive has no copy of the September 2013 version. Updated the manifest. |
| m2 | Cite NESTA Table 1 and Bingane Table I for case39 | These were already in Section 3.3 of the first version. Re-checked the values in the sources, quoted Bingane's gaps per relaxation, and added Hijazi et al. 2014 Table 3. The summary table now quotes each SDP gap separately. |
| m3 | Wording on BARON and MAiNGO for cumene | Changed to "no useful lower bound (absolute gap 1e20)". Stated that the 1e5 MAiNGO gap is for the envelope* setting, and that the other runs ended at 8e10–1e11 or crashed. |
| m4 | `checks/kan_scip_points.py` is not independent and assumes the input order | Labelled it as such in Sections 4.1 and 7, and cited the reviewer's independent reproduction and permutation test as the verification. The script itself was left unchanged, because an independent reproduction already exists. |
| m5 | Huang 2019 unread; the gap for waterno2 must be named | Found an Internet Archive copy of the dissertation and read it; the live site's bot check was not circumvented. It identifies the waterno2 network: Tsinghua n9p3a11, with matching Example 5.41 coefficients (`checks/waterno2_huang_match.py`). It also reports unclosed multi-period SCIP results on related models (Table 5.2). The status stays "new as far as found". The remaining gap is now Huang's 2011 MSc thesis, named explicitly in Sections 5 and 8. |
| m6 | Ambiguous "first bound on the polar instance as listed" | Changed to "the first bound that closes the gap on the polar instance as listed", because MINLPLib lists a GUROBI dual of 572.84. |

Other corrections made during the revision:

- The first version said the 2013 report was not online and the Internet Archive was offline. This is superseded.
- The first version said the data check covered all data except loads and shunts. Loads and shunts are now covered.

## 12. Commands run

### First version (2026-10-01, first author; from the author's returned record)

| command | outcome |
|---|---|
| curl downloads (≥ 1 s spacing): arXiv PDFs 2503.02807, 1801.07114, 2604.03871, 1908.02319, 1903.09678, 1410.1004, 1404.3626, 1404.5071, 1311.6370 and 1411.0359; LAPSE 2025.0372 and 2026.0427; MERL TR2012-088; smart.caltech.edu zeroduality.pdf; Optimization Online 2016/04/5399; the cris.unibo.it D'Ambrosio preprint; the edoc.hu-berlin.de Vigerske dissertation; the UConn Wilhelm preprint; MATPOWER case14/30/39.m; MINLPLib GAMS files for powerflow0030p/0039p/0039r; Zenodo 14961066 files (xlsx, csv, r3.zip, r5.zip) | OK |
| WebFetch of the ZIB-Report 12-25 PDF (curl hit a bot check); tuprints 8657 and hebis; Springer JOTA; Internet Archive | ZIB report OK; tuprints and hebis blocked by a bot check (not circumvented); JOTA redirected for cookies; Internet Archive offline at that time |
| python3 /tmp/xlsx2csv_net.py on r3/r5-opt-overview.xlsx | `sources/zenodo_kan/*.tsv` |
| unzip of the Default-configuration logs for R3_H1_N4/N5/N9 and R5_H1_N3/N5/N8 | `sources/zenodo_kan/ex/` |
| python3 checks/kan_scip_points.py | log; values as in Section 7 (2.6 s) |
| python3 checks/powerflow_data_match.py | log; case30 data match (loads and shunts not compared); case39 matches except taps (11 untapped, 0 tapped, 1 with τ = 1); 34/34 line charging |
| re-fetch of 16 MINLPLib pages and comparison with the cached pages | all unchanged |
| pdftotext -layout on all PDFs, then grep for names and values; pdftoppm on p. 22 of the Schweidtmann arXiv PDF (Fig. 6) | facts as cited |
| curl of Mittelmann pages (plato.asu.edu/ftp/minlp.html, compare.txt, nontrivial.txt) | none of the 15 instances included |
| OpenAlex API queries; arXiv abs pages; doi.org resolution of 10.1109/TPWRS.2018.2848965 | as in Section 8 |
| python3 script writing `sources/MANIFEST.md` | OK |
| Write of report.md | rejected by the tool environment |

### Revision (2026-10-02)

| command | outcome |
|---|---|
| ls/cat of the track folder, the review, and `reviews/lit-network-r1/` (scripts, logs, sources) | report.md missing; review read |
| python3 extraction of the first author's returned output from the workflow transcript (`~/.claude/projects/.../wf_6b4c8c17-543/agent-af001c147848da3cf.jsonl`) to /tmp | full 29,061-character report text recovered |
| sed/grep on the 0030p, 0039p and 0039r GAMS files (balance rows, angle rows) | balance-row layout found; angle rows: 82 `=L= 0.26` + 82 `=G= -0.26` in 0030p, 92 + 92 in 0039p, none in 0039r |
| python3 checks/powerflow_loads_shunts.py (3 runs: wrong row-order assumption; fixed layout; added the branch-coefficient test) | final run: all checks pass (Section 7) |
| grep of the 0030p and 0030r OSIL files for 0.0019, 0.0004 and .26 | no shunt values in either; angle bounds only in 0030p |
| sed/grep of the Hijazi 2014 text (pp. 16–18) and page lookup | facts in Section 3.1 |
| curl of the archive.org availability API and CDX (4057.pdf, DB_HTML 4057) | one PDF snapshot, 2015-12-24 |
| curl of the Wayback PDF (id_ URL) and of minlplib.org/ann_cumene_exp.html | sha256 equal to the reviewer's copies; saved to `sources/` |
| cp of the 2016 revision from `reviews/lit-network-r1/sources/oo_4057.pdf`; pdftotext | saved to `sources/` |
| grep/sed on the NESTA, Bingane, Ghaddar and Schweidtmann text files | values as cited |
| python3 parsing of cached MINLPLib pages (ann_cumene_exp, ann_cumene_tanh, waterno1_*, waterno2_*) | bounds as cited |
| PYTHONDONTWRITEBYTECODE=1 python3 reviews/lit-network-r1/cumene_twin.py | same output as the reviewer's log |
| python3 checks/cumene_twin_exact.py (2 runs; the second adds a one-expression-per-row assertion) | the identity holds exactly |
| WebSearch: the Huang 2019 dissertation; its title with "pdf"; the Huang 2011 MSc thesis | tuprints 8657 record found; no copy of the MSc thesis |
| curl of the tuprints PDF URL | Anubis bot-check page (deleted; not circumvented) |
| curl of an OpenAlex search for the dissertation title; curl of the BASE API (response not used) | no OpenAlex record |
| curl of the Wayback CDX for tuprints 8657; curl of the 2024-04-14 snapshot (id_ URL); pdfinfo; pdftotext | dissertation obtained (157 pages) |
| grep/sed of the dissertation (abstract, Sections 3.3, 4.4 and 5.5, Tables 4.3 and 5.2, conclusion, bibliography) | facts in Section 5.1 |
| grep of the waterno2 OSIL files for the Example 5.41 coefficients | found |
| python3 checks/waterno2_huang_match.py (2 runs; the first used rounding and failed on 22.1276, so the check now uses truncation) | 2 × T occurrences in each file; table in Section 5.1 |
| curl of the ZIB OPUS BibTeX export for author Wei Huang | only the NACO 2012 paper |
| python3 edit of `sources/MANIFEST.md`; sha256sum and stat of the new files | manifest updated |
| Write of report.md (revision) | rejected by the tool environment ('Subagents should return findings as text') |

No solver was run in the revision, and no background jobs were started. At most one core was used at a time.

## Open issues (from the agent's structured return)

- The complete report is on disk; source-access limits below remain.
- Needs integration outside this track: open-instances-summary.md calls the ann_cumene_tanh bound 'the first finite dual', and the paper's ann_cumene_tanh claim must change. The identical twin ann_cumene_exp was closed in floating point by SCIP and LINDO (dual −3379.982394 = primal); our bound is the first rigorous one but is weaker. The bound audit may also want to note this twin.
- Needs integration: any text saying that our powerflow0030p bound applies to MATPOWER case30 is wrong. The MINLPLib model drops case30's bus shunts, and case30 with shunts has a local solution at 576.8923368, below our bound.
- Huang's 2011 MSc thesis (FU Berlin), which MINLPLib cites for waterno2, was not obtained. It may contain multi-period results on the model as written, so 'new as far as found' for waterno2_06–24 rests on its absence. The 2019 dissertation was read; its multi-period models differ from MINLPLib's from 3 periods on.
- The September 2013 first version of Hijazi–Coffrin–Van Hentenryck (Optimization Online 4057) is not archived; only the June 2014 revision was read. In principle it could report FP bounds for the tap-free or shunt-free models.
- It was not checked which data powerflow0014 drops (case14 has taps and a 19 MVAr shunt at bus 9); this is outside the 15 instances.
- The floating-point evidence for the shunt and tap conclusions (AC OPF values) and the SCIP 10 fixed-input KAN runs come from the reviewer's code in reviews/lit-network-r1/; this track ran no solver.
- Publisher versions (JOTA 2019, IEEE TPS papers, NACO 2012) were not accessed; preprints were used. The 2021 dissertation is now checked but the JOTA table is unresolved. The QPLIB objective-value scan is evidence only.

## Response to review

Integration review r1, item 15: rounded the waterno2_06 primal up to 282.888038 and its gap up to ≤ 1.68%; exact rational checks against the saved point and certificate pass (`../../reproduction/logs/integration-r1-displays.json`).

Review: `../../reviews/lit-network-review-r2.md`. Checked and resolved on 2026-10-03. Round-1 resolutions remain in the report.

| issue | resolution and evidence |
|---|---|
| 1. Cumene source versions | Attributed 1e11/8e10/1e5 and Fig. 6 to arXiv v2; added the dissertation's 2930/444/328 gaps and iteration counts from Table 2.8. The JOTA publisher table remains explicitly unchecked. |
| 2. Missing nonclosing benchmarks | Read the SCIP suite Appendix A, Müller–Serrano–Gleixner tables and Göß Table 4; added FP time-limit results in Sections 3,5,8 and qualified the JOGO SCIP 8 test-set statements. Preserved the inconsistent 0039p scale caveat. |
| 3. Prior certified OPF bounds | Read Oustry et al. and the authors' PGLib result table; added the paper next to VSDP and restricted first-rigorous claims to these MINLPLib models. |
| 4. 0030p/0030r rounding | Checked unequal exact decimal coefficients and r2's row-comparison evidence; corrected every exact bound-transport claim, including the r1 response history. FP closure via the twin remains tolerance-level evidence. |
| 5. Huang extended model and gap range | Read Table 5.2; labelled extended-model gaps, removed the 343.41 mismatch argument, retained the original 3-period mismatch, and distinguished the 5-period gap 0.000470589 from the 6–24 range 0.18–1.14. |
| 6. Incomplete bibliography | Added all missing titles and Li's six authors; added Josz, Carrasco–Muñoz, Mittelmann, SCIP 8, VSDP and new r2 sources. Checked paper headers and available DOI metadata; unavailable metadata requests are retained as such. |
| 7. KAN feasibility tolerance | Changed attribution: 1e-6 is inferred from the checked Default R3_H1_N4.log reading only limits/time = 7200, not stated on source p. 16. |
| 8. Stale report and duplicate commands | The complete report is on disk; replaced stale introduction/open-status text and removed the duplicate appended command list, retaining Section 12. |
| 9. Unobtained sources list | Marked Schweidtmann 2021 obtained; listed the AIChE 2025 KAN abstract as unobtained, alongside Huang 2011 and the original Hijazi report. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/network/checks/minor_review_check.py > research-20260929/publication/literature/network/checks/minor_review_check.log` (from the repository root). All checks pass. Additional source-copy, metadata and text-extraction commands are recorded in `publication/reviews/minor-fixes/commands.md`. No solver, main certificate computation, project-wide verification or CI check was run for this revision.

### Round 2: independent minor-fixes review (2026-10-03)

Review: [minor-fixes-review-r1.md](../../reviews/minor-fixes-review-r1.md). Issue numbers below refer to that review.

| issue | resolution |
|---|---|
| 15 | Scoped the remaining novelty claim to this MINLPLib model. |
| 16 | Checked and corrected Müller Table 5 pp. 69/72 and single-author Göß 2026. |
| 22 | Unified the VSDP URL, listed the checker, identified the checked Default log and clarified arXiv v2 Table 4. |

Own exact checks and saved-source evidence: [check_r2.log](../../reviews/minor-fixes/check_r2.log). The full response is [response-r2.md](../../reviews/minor-fixes/response-r2.md); exact commands and results are in [commands.md](../../reviews/minor-fixes/commands.md). Integration edits remain pending in the main summary and audit report. No main computation or solver campaign was repeated.
