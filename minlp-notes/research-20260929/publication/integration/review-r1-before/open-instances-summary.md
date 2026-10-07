# Certificates for open MINLPLib instances: consolidated summary

Updated 2026-10-03: publication-track integration, exact primal points,
upward gap displays, literature context, refreshed MINLPLib status, solver
comparisons, and the independently checked SCIP finding. This page collects
the rigorous dual bounds computed in the September 29 continuation for MINLPLib instances listed as open, with
their independent verification status. A dual bound here is valid for every
*exactly* feasible point of the OSIL model (not for points feasible only up
to a tolerance). "Best listed dual" is the best single-solver bound on the
MINLPLib instance page (fetched 2026-09-29; site updated 2026-09-14), not the
three-solver metadata value. The [status refresh](publication/minlplib-status/report.md)
found the relevant pages, solved marks, points, bounds and OSIL models unchanged
on 2026-10-02; this is the refresh date, not a claim about a later live state.
Gaps are absolute unless marked relative or percent. Every displayed gap cell is
rounded upward and is an upper bound on the gap under the stated proof
assumptions. Relative gaps in the closed table divide by the absolute
certified dual. Gap calculations and exact source fractions are recorded in
[publication/integration/gap-values.json](publication/integration/gap-values.json).
Displayed dual bounds are truncated or rounded outward, so each displayed
value is itself a valid bound. Numeric primal bounds are rounded upward for
minimization and downward for maximization. A point objective enclosure
can give a tighter gap than subtraction of the two displayed bounds.

## Instances closed to the stated gaps (31)

| instance | best listed dual | our rigorous dual | our or listed primal | gap after | mechanism | verification |
|---|---|---|---|---|---|---|
| lnts50 | 0.55464755 | 0.5546687649381 | 0.5546687649387 | ≤ 5.79e-13 | chain Lagrangian, linear-tangent law, monotone in h | [dual verified](reviews/open-instances-verification/verification-report.md); [exact primal verified](publication/primal/lnts/report.md) |
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011670 | ≤ 6.12e-13 | same | dual and exact primal verified (same reports) |
| lnts200 | 0.55219867 | 0.5545770161025 | 0.5545770161031 | ≤ 5.84e-13 | same | dual and exact primal verified (same reports) |
| lnts400 | 0.55204395 | 0.5545724137001 | 0.5545724137007 | ≤ 5.88e-13 | same | dual and exact primal verified (same reports) |
| dtoc5 | 0.00243096 | 5.38967211918114 | 5.389672119181141 | ≤ 4.7e-16 | Lagrangian convex at the costate (Mangasarian/Arrow-type) | dual verified; [exact primal verified](publication/primal/dtoc5-lukvle10/report.md) |
| camshape100 | −4.28415233 | −4.28414712174675 (exact optimum, rounded down) | exact optimum, attained | ≤ 0 | discrete Sturm comparison in u = 1/r; envelope point exactly feasible | verified (rational) |
| camshape200 | −4.63229055 | −4.27850023299273 (exact optimum, rounded down) | exact optimum, attained | ≤ 0 | same | verified (rational) |
| camshape400 | −4.97265746 | −4.27568847892555 (exact optimum, rounded down) | exact optimum, attained | ≤ 0 | same | verified (rational) |
| camshape800 | −5.12584096 | −4.27427414195420 (exact optimum, rounded down) | exact optimum, attained | ≤ 0 | same | verified (rational) |
| lukvle10 | 351.223393 | 352.2380254050784 | 352.2380254064961 | ≤ 1.5e-9 | partial chain Lagrangian + 2-D interval B&B on an end window | dual verified; [exact primal verified](publication/primal/dtoc5-lukvle10/report.md) |
| optcdeg2 | 292.41713458 | 293.87607509587509 (certificate value rounded down) | ≤ 293.87607509587509328 (rigorously feasible) | ≤ 9e-16 | one quadratic calibration whose curvature vanishes at both switches ([bang-bang note](theory-bangbang/report.md)); earlier: chain Lagrangian + exact head block, 2.1e-5 rel. | [verified](reviews/bangbang-verification/verification-report.md) (exact rational) |
| hvycrash | −2.185e8 | −0.2185 (exact) | −0.2185 | ≤ 0 | objective constant on the feasible set; explicit feasible point | [verified](reviews/wave2-small-verification/verification-report.md) |
| ex6_2_7 | −1.06726714 | −0.16084761546364905 | −0.16084761546360086 | ≤ 4.9e-14 | mass-balance Lagrangian, tangent-plane test (an ε-global method, McDonald–Floudas 1997, very likely solved it; not confirmed) | verified |
| ex6_2_5 | −111.4201713 | −70.75207783344770759 | −70.752077833447705 | ≤ 2.1e-15 | same | verified |
| etamac | −15.40567054 | −15.294675643368093 | exactly feasible point | ≤ 2.6e-15 | convex relaxation (hidden convexity) + KKT tangent plane | verified |
| pricing050 (max) | −1534.3281 | −1813.8290784519730577 (upper) | −1813.8290784519731 | ≤ 4.23e-14 | Lagrangian over 5 rows, certified 1-D minimizations | verified |
| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | exact-point objectives within 1.01e-14 of the duals | ≤ 1.01e-14 | discrete catenary calibration + 2-D end-window B&B | [dual verified](reviews/cops-verification/verification-report.md); [exact primal verified](publication/primal/chain/report.md) |
| catmix100–800 | −0.0666 … −1.489 | −0.04806944 … −0.04805591 | improved primal points | ≤ 1.85e-13 / 1.90e-11 / 6.81e-11 / 1.49e-10 (100/200/400/800) | exact DP on a 1-D projective separator; concave value functions | verified (all four recomputed independently; [recheck](reviews/catmix-recheck.md)) |
| powerflow0030p | 572.8395847 | 576.8934122988004 | 576.8934134704 | ≤ 2.1e-9 rel. | SDP/Lagrangian dual, exact rational evaluation, exact LDLᵀ PSD proof | verified; [exact primal verified](publication/primal/powerflow/report.md) |
| powerflow0039p | 41818.27916 | 41869.05148485014 | 41869.0515113203 | ≤ 6.4e-10 rel. | SDP dual + exact leaf-bus identity (bus 29) + exact vertex cuts, B&B on 3 leaf coordinates ([extension](open-instances-wave3/powerflow/extension-report.md)) | [verified](reviews/powerflow0039-review.md); [exact primal verified](publication/primal/powerflow/report.md) |
| powerflow0039r | 41804.88153 | 41869.05148327243 | 41869.0515113210 | ≤ 6.7e-10 rel. | same | verified; [exact primal verified](publication/primal/powerflow/report.md) |
| pindyck | −1437.941134 (SCIP) | −1170.4862854360886163932 | −1170.486285436088562 | ≤ 5.44e-14 | reduced objective proved concave on a polytope containing the feasible set; tangent-plane bound ([extension](open-instances-wave2/small/pindyck-extension.md)) | [verified](reviews/pindyck-review.md) (independent rebuild) |
| eg_int_s | 6.32629896 (SCIP) | 6.4531031529331155 | 6.4531031593842275 (exactly feasible) | ≤ 1e-9 rel. | second-order Taylor models keeping the signed cancellation of the Gaussian-kernel rows, per-box LP over the 24 minimax rows, domain reduction, exact integer splits ([note](open-instances-wave3/eg/retry.md)); SCIP 8.1 had solved it in floating point (Göß–Burlacu–Martin) | [verified](reviews/eg-retry-review.md) (all leaves, under A1/A2) |
| eg_disc_s | 3.36596129 (SCIP) | 5.760539610694994 | 5.7605396164535107 (exactly feasible) | ≤ 1e-9 rel. | same | verified (all leaves, under A1/A2) |
| eg_disc2_s | 0 (SHOT) | 5.642100574331458 | 5.6421005799711068 (exactly feasible) | ≤ 1e-9 rel. | same | verified on all 1,114,361 leaves under A1/A2; separate outward-rounded interval sample: 10,404 leaves of parts 0 and 2–7 |

For lnts50–400, dtoc5, lukvle10, chain50–400 and
powerflow0030p/0039p/0039r, exactly feasible points have now been constructed
and independently reviewed in publication/primal/. The gaps use the upper
ends of their objective enclosures. The lnts gap cells use the displayed
summary duals; against the certified verifier N·h2 bounds the gaps are at
most 5.55e-13. The lukvle10 KKT agreement is numerical and does not prove
global optimality; attributing its remaining gap to the dual requires that
additional assumption.

Gaps use saved objective enclosure endpoints and certificate values, except
lnts (the displayed summary duals), chain (the safe individual dual displays),
and pricing050 (subtraction of its safe displayed upper and lower bounds).
The pricing gap is deliberately conservative: the saved verifier log reports
a smaller gap, but does not retain enough objective digits to reconstruct it
exactly by subtraction. The catmix gaps use the stronger independently
verified duals, the saved exactly feasible author points for 100/200/400,
and the verifier's exact DP-policy point for 800; the compact dual range is
only a display. See the [catmix recheck](reviews/catmix-recheck.md) and
[exact display record](publication/reproduction/cops/logs/exact_display_checks.json).
For optcdeg2 the gap uses the exact rational certificate, rather than its
rounded-down table display. Zero for camshape and hvycrash means an attained
exact optimum proved analytically, rather than subtraction of displays.

For all three eg_* certificates, **A1** assumes that the certifier's
hand-checked floating-point padding analysis bounds every rounding error;
**A2** assumes numpy's exp has relative error at most 1e-14. A2 is supported
by sampling, not a uniform proof. The final rational certificate tests do
not remove these assumptions about their input enclosures. The
[eg recheck](publication/eg-recheck/report.md) certified all 1,114,361 leaves
of run G for eg_disc2_s, with zero failures. The earlier 1,152,830 count is
processed boxes, not leaves. Independent review also supplied an exact
coverage proof and outward-rounded interval certificates for a separate
10,404-leaf sample in parts 0 and 2–7; that sample does not replace A1/A2
for the remaining leaves.

## Relaxation certified; OSIL models exactly infeasible

| instances | best listed dual | our result | primal | gap | mechanism | verification |
|---|---|---|---|---|---|---|
| kan_r3_h1_n4/n5/n9, kan_r5_h1_n3/n5/n8 | 0.0003908 … −789.74 (GUROBI) | optimum of the network relaxation R enclosed with absolute gap ≤ 2.42e-8 (e.g. kan_r5_h1_n8: 0.0693278605…) | improved primal values for r5_n3, r5_n5, r5_n8 (listed 0.3606 → 0.0694 for n8) | ≤ 2.42e-8 absolute (per-instance gaps below) | reduced-space interval B&B over the inputs | [verified](reviews/wave3-verification/verification-report.md); **the OSIL models have no exactly feasible point** (proved), so the claim concerns R |

The [exact primal track](publication/primal/water-ann-kan/report.md) now
provides points satisfying every retained row of R and all variable bounds.
Their enclosure proof assumes outward rounding by mpmath iv. The original
partition-of-unity rows remain exactly inconsistent; no OSIL-feasible KAN
point or OSIL optimum is claimed.

| instance | absolute gap for R (rounded up) |
|---|---|
| kan_r3_h1_n4 | ≤ 6.9e-11 |
| kan_r3_h1_n5 | ≤ 1.08e-10 |
| kan_r3_h1_n9 | ≤ 9e-11 |
| kan_r5_h1_n3 | ≤ 2.42e-8 |
| kan_r5_h1_n5 | ≤ 1.02e-10 |
| kan_r5_h1_n8 | ≤ 9.6e-11 |

## Instances substantially improved but not closed

| instance | best listed dual | our rigorous dual | best primal | gap after | verification |
|---|---|---|---|---|---|
| waterno2_06 | 165.19 | **278.230573** (separator branching: 272.584700; wave 2: 263.735099) | 282.888038 (exactly feasible) | ≤ 1.68% (≤ 3.78%; ≤ 7.27%) | wave 2 [verified](reviews/waterno2-verification/verification-report.md); separator branching [verified](reviews/waterno2-sepbranch-review.md); cell-dependent slopes [verified](reviews/waterno2-cellslopes-review.md) (all 49,315 pair bounds re-bounded independently) |
| waterno2_09 | 273.90 | 824.834692 | 914.012 (exactly feasible) | ≤ 10.82% | [verified](reviews/waterno2-recheck.md) (all periods) |
| waterno2_12 | 479.51 | 2089.754565 | 2233.821346 (exactly feasible) | ≤ 6.90% | verified (all periods) |
| waterno2_18 | 770.74 | 4790.820715 | 5023.983 (exactly feasible) | ≤ 4.87% | verified (all periods) |
| waterno2_24 | 1095.13 | 6576.151388 | 6963.795181 (exactly feasible) | ≤ 5.90% | verified (all periods) |
| ann_cumene_tanh | none | **−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point) | −3379.9823940 (exactly feasible) | ≤ 0.195% (wave 3: ≤ 20%) | wave 3 verified with caveats; extension [independently re-certified](reviews/ann-extension-review.md) |

Percent gaps: (primal − dual)/|dual| for waterno2; (primal − dual)/|primal|
for ann_cumene_tanh (under the waterno2 convention its wave-3 gap would be
16.1%; the new gap rounds upward to 0.195% under the primal denominator
and 0.194% under the dual denominator).

Mechanism (waterno2): exact period decomposition (T periods linked by
3(T−1) tank-level copies and one horizon row), bundle-tuned Lagrangian,
rigorous per-period branch and bound. For waterno2_06 the bound was then
raised by branching on the separators: the tank-level links are split into
cells (113–162 per link), each (entry cell, exit cell) pair of each period
is bounded rigorously, the horizon row is replaced by an exactly derived
terminal-volume row, and the bound is the exact shortest path over the cell
pairs ([note](open-instances-wave2/waterno2/separator-branching.md)); this
is the decomposition-certificate scheme of Section 2 of the synthesis,
with one fixed Lagrangian slope per link. Round 4 then gave each cell its
own slope vector, used for both periods that share the link (the validity
condition; [note](open-instances-wave2/waterno2/cell-slopes.md)), chose
the slopes cell by cell with small LPs, re-used old pair bounds through an
exact slope correction, and refined further: 278.230573774 (gap 1.68%).
waterno2_09–24 were not attempted with separator branching or cell slopes. Mechanism (ann_cumene_tanh): a reduced-space branch and bound
over the 5 inputs with affine arithmetic (one noise symbol per tanh
neuron), a per-box LP dual evaluated rigorously, and domain reduction
([note](open-instances-wave3/ann/extension.md)); the remaining gap sits
along a nearly flat constraint surface.

The water and ANN primal columns now bound exactly feasible points; see the
[exact primal report](publication/primal/water-ann-kan/report.md). Water
feasibility uses exact algebraic arithmetic. ANN feasibility uses a forward
construction and outward-rounded enclosures, assuming mpmath iv is correct.

## Prior literature and scope of novelty

The tables describe certificates for the stored MINLPLib OSIL models.
"New as far as found" records the search result; it does not establish
priority against unread or undiscovered sources. Floating-point closure and
rigorous certification are distinct claims. Sources, model comparisons,
unread sources and review responses are in the three literature reports.

| instance | prior result and consequence | report |
|---|---|---|


| lnts50 | Göß–Burlacu–Martín: Gurobi tolerance-level closure; Göß 2026 PARA result. Partly known; rigorous closure new as far as found. | [control](publication/literature/control/report.md) |
| lnts100 | Göß 2026 PARA displays a zero percentage gap. Partly known in floating point; rigorous closure new as far as found. | [control](publication/literature/control/report.md) |
| lnts200 | Göß 2026 PARA displays a zero percentage gap. Partly known in floating point; rigorous closure new as far as found. | [control](publication/literature/control/report.md) |
| lnts400 | Göß 2026 PARA displays a small nonzero gap. Partly known in floating point; rigorous closure new as far as found. | [control](publication/literature/control/report.md) |
| dtoc5 | MINOTAUR floating-point closure on identical QPLIB_8585, with assumed default variable bounds. Waki et al. 2006 found a numerically tight sparse SDP on the DTOC5 source. MINLPLib dynamics multiply the CUTEst quadratic coefficient by 4. Partly known; rigorous certificate new as far as found. | [control](publication/literature/control/report.md) |
| camshape100 | Octeract solved it globally in floating point; Mittelmann lists Octeract and ANTIGONE on the rounded QPLIB copy. Exact optimum is the new result; ANTIGONE’s reported value is a tolerance artifact. | [control](publication/literature/control/report.md) |
| camshape200 | Octeract was listed as solving the rounded QPLIB copy; value and log unavailable. Partly known; exact optimum new as far as found. | [control](publication/literature/control/report.md) |
| camshape400 | No prior global closure found. New as far as found. | [control](publication/literature/control/report.md) |
| camshape800 | MINOTAUR claimed global closure of the rounded QPLIB copy at a conflicting value. Our exact MINLPLib result is new as far as found; transport of the contradiction to the rounded QPLIB model is strong evidence, not proof. | [control](publication/literature/control/report.md) |
| lukvle10 | Local CUTEst value and nonclosing solver bounds only. New as far as found. | [control](publication/literature/control/report.md) |
| optcdeg2 | Older MINOTAUR closure listing on identical QPLIB_8803 lacks the value/log; later infeasibility claim is false. The CUTEst damping coefficient differs by a factor of 4. Partly known; rigorous certificate new as far as found. | [control](publication/literature/control/report.md) |
| chain50 | COPS local values; no prior global closure found. New as far as found. | [control](publication/literature/control/report.md) |
| chain100 | COPS local values; no prior global closure found. New as far as found. | [control](publication/literature/control/report.md) |
| chain200 | COPS local values; no prior global closure found. New as far as found. | [control](publication/literature/control/report.md) |
| chain400 | COPS local values; no prior global closure found. New as far as found. | [control](publication/literature/control/report.md) |
| catmix100 | COPS 2.0 local values; COPS 3.0 uses a different discretization. New as far as found. OSIL coefficients differ slightly from GAMS coefficients. | [control](publication/literature/control/report.md) |
| catmix200 | COPS 2.0 local values; COPS 3.0 uses a different discretization. New as far as found. OSIL coefficients differ slightly from GAMS coefficients. | [control](publication/literature/control/report.md) |
| catmix400 | COPS 2.0 local values; COPS 3.0 uses a different discretization. New as far as found. OSIL coefficients differ slightly from GAMS coefficients. | [control](publication/literature/control/report.md) |
| catmix800 | COPS 2.0 local values; COPS 3.0 uses a different discretization. New as far as found. OSIL coefficients differ slightly from GAMS coefficients. | [control](publication/literature/control/report.md) |
| hvycrash | Same CUTE HVYCRASH at N=50; the solution value was already listed. Partly known; exact constant-objective identity and feasible witness new as far as found. | [small](publication/literature/small/report.md) |
| ex6_2_5 | McDonald–Floudas ε-global result likely, but key source not read; later BARON global labels are not certificates. Partly known; rigorous certificate new as far as found. | [small](publication/literature/small/report.md) |
| ex6_2_7 | McDonald–Floudas ε-global result likely, but key source not read; later BARON global labels are not certificates. Partly known; rigorous certificate new as far as found. | [small](publication/literature/small/report.md) |
| etamac | Local values or nonclosing bounds only. New as far as found; source-model and scaling limits are stated in the report. | [small](publication/literature/small/report.md) |
| pricing050 | Local values or nonclosing bounds only. New as far as found; source-model and scaling limits are stated in the report. | [small](publication/literature/small/report.md) |
| pindyck | Local values or nonclosing bounds only. New as far as found; source-model and scaling limits are stated in the report. | [small](publication/literature/small/report.md) |
| eg_int_s | SCIP 8.1 solved it globally in floating point (Göß–Burlacu–Martin). Our assumption-qualified certificate is new as far as found. CAMINO’s Gurobi optimality claim is refuted by a feasible point. | [small](publication/literature/small/report.md) |
| eg_disc_s | No valid prior closure found. New as far as found. CAMINO’s Gurobi optimality claims are refuted; recorded termination status and cause are unknown. | [small](publication/literature/small/report.md) |
| eg_disc2_s | No valid prior closure found. New as far as found. CAMINO’s Gurobi optimality claims are refuted; recorded termination status and cause are unknown. | [small](publication/literature/small/report.md) |
| powerflow0030p | Partly known: tolerance-level closure via rectangular twin. MATPOWER case30 loses its two shunts in MINLPLib; polar/rectangular coefficient rounding prevents unproved exact bound transport. Prior rigorous ACOPF work (Oustry et al.) concerns different models. | [network](publication/literature/network/report.md) |
| powerflow0039p | Prior moment/SDP results solve tapped MATPOWER case39; MINLPLib drops transformer taps. New as far as found for these stored models. | [network](publication/literature/network/report.md) |
| powerflow0039r | Prior moment/SDP results solve tapped MATPOWER case39; MINLPLib drops transformer taps. New as far as found for these stored models. | [network](publication/literature/network/report.md) |
| waterno2_06 | Huang’s related multi-period models remain unclosed; the cited MSc thesis was not obtained. New as far as found. | [network](publication/literature/network/report.md) |
| waterno2_09 | Huang’s related multi-period models remain unclosed; the cited MSc thesis was not obtained. New as far as found. | [network](publication/literature/network/report.md) |
| waterno2_12 | Huang’s related multi-period models remain unclosed; the cited MSc thesis was not obtained. New as far as found. | [network](publication/literature/network/report.md) |
| waterno2_18 | Huang’s related multi-period models remain unclosed; the cited MSc thesis was not obtained. New as far as found. | [network](publication/literature/network/report.md) |
| waterno2_24 | Huang’s related multi-period models remain unclosed; the cited MSc thesis was not obtained. New as far as found. | [network](publication/literature/network/report.md) |
| ann_cumene_tanh | Partly known: the exactly identical ann_cumene_exp twin was closed in floating point by SCIP/LINDO. Our rigorous finite bound is new as far as found and weaker than those floating-point claims. | [network](publication/literature/network/report.md) |
| kan_r3_h1_n4 | Published SCIP zero-gap claims conflict with the certified minimum of R; exact network evaluation exposes feasibility-tolerance artifacts. Prior claim contradicted; rigorous R result new as far as found. | [network](publication/literature/network/report.md) |
| kan_r3_h1_n5 | Published SCIP zero-gap claims conflict with the certified minimum of R; exact network evaluation exposes feasibility-tolerance artifacts. Prior claim contradicted; rigorous R result new as far as found. | [network](publication/literature/network/report.md) |
| kan_r3_h1_n9 | Prior solver runs did not close the gap. New as far as found for R; exact OSIL infeasibility remains separate. | [network](publication/literature/network/report.md) |
| kan_r5_h1_n3 | Prior solver runs did not close the gap. New as far as found for R; exact OSIL infeasibility remains separate. | [network](publication/literature/network/report.md) |
| kan_r5_h1_n5 | Prior solver runs did not close the gap. New as far as found for R; exact OSIL infeasibility remains separate. | [network](publication/literature/network/report.md) |
| kan_r5_h1_n8 | Prior solver runs did not close the gap. New as far as found for R; exact OSIL infeasibility remains separate. | [network](publication/literature/network/report.md) |

## One-hour solver comparison

The [final campaign](publication/solver-runs/report.md) and
[per-run table](publication/solver-runs/results_table.md) compare BARON
26.5.27, GUROBI 13.0.2 and SCIP 10.0.3 on the paper instances with a
3600-second solver limit, one thread, and absolute/relative gap requests of
1e-9. There are 129 kept outcomes, including three SCIP memory-limit stops;
126 pass the measurement rule. Certificate-consistent closures are zero
for every solver. BARON’s two optimality claims (camshape100/200) contradict
the proved optimum intervals and return infeasible points.

All 109 finite final solver dual values are weaker than our corresponding
certificates. Six BARON values (catmix100/200/400/800, dtoc5, optcdeg2) carry
BARON’s warning that globality is not guaranteed, leaving 103 without that
warning. Six SCIP values concern slightly tightened log/power argument
bounds. KAN comparisons concern R. The first batch of ten runs suffered
overload and memory pressure; it passes the stated measurement rule but is
not an isolated speed benchmark. BARON’s limit is CPU time; GUROBI/SCIP use
wall time. The report discloses actual solver times, interrupts, capability
failures and shared-machine conditions. These runs establish neither
performance rankings nor failure under other settings or larger budgets.

## Invalid bounds and solver errors found

**Systematic audit** ([report](bound-audit/audit-report.md);
[verification](reviews/bound-audit-verification/verification-report.md)).
Across all 1633 MINLPLib instances (2816 listed points, 11086 per-solver
bounds), 19 listed solver dual bounds on 15 instances are proven invalid:
an exactly feasible point was shown to exist (exact rational arithmetic,
interval Krawczyk test, or an exact duality certificate) with objective
strictly better than the bound. All 19, and the two-sided optimum
enclosures of the four emfl instances, have been confirmed with code
independent of the audit's: 14 pairs and emfl050_3_3 by the
[first verification](reviews/bound-audit-verification/verification-report.md),
the other 5 pairs and three emfl instances by the
[recheck](reviews/bound-audit-recheck.md).

- **Gross errors (11 pairs, 1.2e-5 of |d| up to a factor of about 784;
  7 of the 11 are between 1.2e-5 and 7.3e-5 of |d|, below common 1e-4 gap
  tolerances, so "gross" means only "beyond MINLPLib's 1e-6 convention"):**
  glider100 (COUENNE, LINDO; the exactly feasible point is a spurious but
  valid solution of the discretized model), topopt-cantilever_60x40_50,
  methanol50, sssd20-04/22-08/25-04/25-08persp, nuclear14 (LINDO), and
  ghg_3veh (ANTIGONE, BARON).
- **Tolerance-scale violations (8 pairs, 1.9e-9 to 3.3e-7 of |d|):**
  nd_netgen-2000-3-4-b-a-ns_7 (CPLEX, GUROBI), watercontamination0303
  (BONMIN, LINDO), four smallinvDAX instances (LINDO). All instances marked
  solved whose closing bound is invalid are in this group; the audit does
  not contradict their solved marks under MINLPLib's 1e-6 rule.
- **Tolerance effects in listed primal values:** for the emfl family every
  listed bound is valid, but listed primal values lie below the exact
  optimum (by up to about 4e-4 relative; for the solved emfl050_3_3 the
  difference is at least 1.42e-5 absolute, 1.36e-6 relative).
- **Rounding-scale audit results:** all 12 class (i-r) pairs were
  independently re-proved in [audit-ir](publication/audit-ir/report.md),
  including a global optimum proof for spring. They refute the displayed
  numbers taken literally; rounding can explain the conflicts and the
  underlying solver bounds are unknown. Page parsing and screening were
  independently checked.
- The [model-history check](publication/minlplib-status/report.md) found
  unchanged audited models except for rounding of three ghg_3veh constants;
  the contradiction also holds on that older text. Missing archive windows
  and GAMS/OSIL coefficient differences remain stated limits.
- "A solver reported a local optimum as a bound" is an inference, not
  verified.

Earlier individual findings:

- **Listed LINDO dual bounds that are not valid bounds** (interval Krawczyk
  existence proofs of exactly feasible points below them): methanol50 (by
  1.2%), rocket100, rocket200, rocket400 (by 1.1e-7, 4.7e-8, 1.9e-7, about
  1e-7 relative, below MINLPLib's 1e-6 tolerance; MINLPLib already marks
  these unsolved, and they are not among the audit's 19 pairs, which
  include methanol50).
- **SCIP wrong optimal values on waterno2 subproblems.** The
  [SCIP bug track](publication/scip-bug/report.md) and its
  [independent review](publication/reviews/scip-bug-review-r1.md) supply
  exact rational witnesses for the period problems and the seed-dependent
  cell-pair problem. The higher cell-pair claim is now refuted by an exactly
  feasible witness; the low claim is not refuted. The finding reproduces
  on SCIP 10.0.2/10.0.3/10.1.0 and the tested master commit. In the
  instrumented wrong runs, reverse propagation by the default nonlinear
  handler cuts off a feasible point because of a binary64 residual in a
  cubic equality at fixed bounds. That mechanism is established for those
  traced runs; it is not a diagnosis of every SCIP bound. A minimized
  reproducer and an upstream report are prepared. **The upstream report
  is drafted and has NOT been submitted; filing is the user’s decision.**
- **Tolerance artifacts in listed primal values:** camshape400/800 (points
  violating rows by 3e-10 lie 8e-6 and 3e-5 below the exact optimum, because
  the chain amplifies violations up to about 600-fold); hvycrash p1/p2
  (large r_k artifacts). Not a listed value: SCIP 10's camshape100
  incumbent from our own run (row violation 1e-8) lies 5.3e-5 below the
  exact optimum (not independently checked).

## What the pattern shows

In our reading of every closed case (an interpretation, not tested
experimentally), the obstacle for single-tree solvers was the relaxation,
not the amount of branching: free variables without bounds, long chains of
nonconvex equalities, or hidden convexity or monotonicity invisible to
termwise relaxations. Most certificates (lnts, dtoc5, lukvle10, optcdeg2,
chain, catmix, and the waterno2 improvements) combine a decomposition along
the model's chain or period structure, an affine or state-dependent split
(Lagrangian, calibration, or dynamic programming), and exact treatment of a
few low-dimensional windows. The others use comparison (camshape), an exact
identity (hvycrash), a Gibbs tangent-plane test (ex6_2_*), hidden convexity
(etamac), a Lagrangian over five rows (pricing050), concavity on a polytope
(pindyck) or an SDP dual (powerflow). The eg_* closures (round 4) used a
reduced-space branch and bound whose second-order Taylor models keep the
signed cancellation among the 97 Gaussian terms of each row, combined with
a per-box LP over the 24 minimax rows (essential near the optimum in the
ablation); the wave-3 enclosures, which summed term ranges, were 15–19
times looser at medium box sizes (3–7 times at others) and failed. The chain pattern is the one described
by the [consistency-relaxation theory](theory-consistency/consistency-relaxations.md)
(affine splits plus full consistency on short windows; reviewed, rechecked
and confirmed). The mechanisms themselves are classical (Lagrangian and SDP
duality, Mangasarian-type sufficiency, Sturm comparison, tangent-plane
tests, calibration, concavity certificates); the contribution is the
certificates and the interpretation.

Coverage: the scout found 146 open instances among 283 low-width nonconvex
candidates, in addition to the first-wave instances that the scout excluded.
The tables cover 31 OSIL instances closed to the stated gaps under the
stated proof assumptions. All three eg_* dual proofs use A1/A2; every leaf
of eg_disc2_s is now checked. Exactly feasible primal points cover the 13
formerly tolerance-only closures. Literature already contained
floating-point closure or near-closure for several cases, as the
per-instance table explains.

The other results are six exactly infeasible KAN OSIL models whose
relaxation R has absolute gap at most 2.42e-8, five waterno2 instances with
improved bounds (waterno2_06 now within 1.68%), and ann_cumene_tanh with a
rigorous finite bound within 0.195% of an exactly feasible primal. The
three eg_* closures were added in round 4. In wave 3, eg_int_s and
eg_disc2_s stayed below listed bounds and eg_disc_s was not run.

## Evidence and reproduction

The [reproduction guide](publication/reproduction/README.md) and
[package report](publication/reproduction/report.md) map the certificates,
primal definitions and audit classifications to saved inputs, scripts and
outputs. Follow their disposable-copy instructions: several scientific
scripts write logs or certificates when imported or run. The topopt p5
numbers in the audit rest on the committed certificate; a one-BLAS-thread
regeneration selects a different point, as explained in the guide. Exact
replay of saved proofs and numerical regeneration are distinct operations.
Older detailed reports can contain unsafe rounded displays; the checked
bounds and gaps on this page are authoritative for the paper.

The [publication-readiness record](publication/READINESS.md) gives review
verdicts, proof assumptions, remaining decisions and packaging steps. This
integration reran no solver or scientific search, made no commit, and
contacted nobody.
