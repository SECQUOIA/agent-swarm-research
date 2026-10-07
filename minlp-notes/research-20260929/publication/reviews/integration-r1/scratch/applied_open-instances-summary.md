# Certificates for open MINLPLib instances: consolidated summary

Date: 2026-09-30 (round-4 results added 2026-10-01). This page collects the rigorous dual bounds computed in
the September 29 continuation for MINLPLib instances listed as open, with
their independent verification status. A dual bound here is valid for every
*exactly* feasible point of the OSIL model (not for points feasible only up
to a tolerance). "Best listed dual" is the best single-solver bound on the
MINLPLib instance page (fetched 2026-09-29; site updated 2026-09-14), not the
three-solver metadata value. Gaps use absolute differences unless marked.
Displayed dual bounds are truncated or rounded outward, so each displayed
value is itself a valid bound. Numeric primal bounds are rounded upward for
minimization and downward for maximization. A point objective enclosure
can give a tighter gap than subtraction of the two displayed bounds.

## Instances closed (31)

| instance | best listed dual | our rigorous dual | our or listed primal | gap after | mechanism | verification |
|---|---|---|---|---|---|---|
| lnts50 | 0.55464755 | 0.5546687649381 | 0.5546687649387 | 5.79e-13 | chain Lagrangian, linear-tangent law, monotone in h | [verified](reviews/open-instances-verification/verification-report.md) |
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011670 | 6.12e-13 | same | verified |
| lnts200 | 0.55219867 | 0.5545770161025 | 0.5545770161031 | 5.84e-13 | same | verified |
| lnts400 | 0.55204395 | 0.5545724137001 | 0.5545724137007 | 5.88e-13 | same | verified |
| dtoc5 | 0.00243096 | 5.38967211918114 | 5.389672119181141 | < 1e-14 | Lagrangian convex at the costate (Mangasarian/Arrow-type) | verified |
| camshape100 | −4.28415233 | −4.28414712174675 (exact optimum, rounded down) | exact optimum, attained | 0 | discrete Sturm comparison in u = 1/r; envelope point exactly feasible | verified (rational) |
| camshape200 | −4.63229055 | −4.27850023299273 (exact optimum, rounded down) | exact optimum, attained | 0 | same | verified (rational) |
| camshape400 | −4.97265746 | −4.27568847892555 (exact optimum, rounded down) | exact optimum, attained | 0 | same | verified (rational) |
| camshape800 | −5.12584096 | −4.27427414195420 (exact optimum, rounded down) | exact optimum, attained | 0 | same | verified (rational) |
| lukvle10 | 351.223393 | 352.2380254050784 | 352.2380254064961 | 1.4e-9 | partial chain Lagrangian + 2-D interval B&B on an end window | verified |
| optcdeg2 | 292.41713458 | 293.87607509587509 (exact value of the certificate) | ≤ 293.87607509587509328 (rigorously feasible) | 9.0e-16 | one quadratic calibration whose curvature vanishes at both switches ([bang-bang note](theory-bangbang/report.md)); earlier: chain Lagrangian + exact head block, 2.1e-5 rel. | [verified](reviews/bangbang-verification/verification-report.md) (exact rational) |
| hvycrash | −2.185e8 | −0.2185 (exact) | −0.2185 | 0 | objective constant on the feasible set; explicit feasible point | [verified](reviews/wave2-small-verification/verification-report.md) |
| ex6_2_7 | −1.06726714 | −0.16084761546364905 | −0.16084761546360086 | 4.8e-14 | mass-balance Lagrangian, tangent-plane test (an ε-global method, McDonald–Floudas 1997, very likely solved it; not confirmed) | verified |
| ex6_2_5 | −111.4201713 | −70.75207783344770759 | −70.752077833447705 | 2.0e-15 | same | verified |
| etamac | −15.40567054 | −15.294675643368093 | exactly feasible point | 2.6e-15 | convex relaxation (hidden convexity) + KKT tangent plane | verified |
| pricing050 (max) | −1534.3281 | −1813.8290784519730577 (upper) | −1813.8290784519731 | 1.0e-17 | Lagrangian over 5 rows, certified 1-D minimizations | verified |
| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | exact-point objectives within 1.01e-14 of the duals | ≤ 1.01e-14 | discrete catenary calibration + 2-D end-window B&B | [verified](reviews/cops-verification/verification-report.md) |
| catmix100–800 | −0.0666 … −1.489 | −0.04806944 … −0.04805591 | improved primal points | 1.65e-13 (100) … 1.5e-10 (800, verifier) | exact DP on a 1-D projective separator; concave value functions | verified (all four recomputed independently; [recheck](reviews/catmix-recheck.md)) |
| powerflow0030p | 572.8395847 | 576.8934122988004 | 576.8934134704 | 2.0e-9 rel. | SDP/Lagrangian dual, exact rational evaluation, exact LDLᵀ PSD proof | verified |
| powerflow0039p | 41818.27916 | 41869.05148485014 | 41869.0515113203 | 6.3e-10 rel. | SDP dual + exact leaf-bus identity (bus 29) + exact vertex cuts, B&B on 3 leaf coordinates ([extension](open-instances-wave3/powerflow/extension-report.md)) | [verified](reviews/powerflow0039-review.md) |
| powerflow0039r | 41804.88153 | 41869.05148327243 | 41869.0515113210 | 6.7e-10 rel. | same | verified |
| pindyck | −1437.941134 (SCIP) | −1170.4862854360886163932 | −1170.486285436088562 | 5.44e-14 | reduced objective proved concave on a polytope containing the feasible set; tangent-plane bound ([extension](open-instances-wave2/small/pindyck-extension.md)) | [verified](reviews/pindyck-review.md) (independent rebuild) |
| eg_int_s | 6.32629896 (SCIP) | 6.4531031529331155 | 6.4531031593842275 (exactly feasible) | 1.0e-9 rel. | second-order Taylor models keeping the signed cancellation of the Gaussian-kernel rows, per-box LP over the 24 minimax rows, domain reduction, exact integer splits ([note](open-instances-wave3/eg/retry.md)); SCIP 8.1 had solved it in floating point (Göß–Burlacu–Martin) | [verified](reviews/eg-retry-review.md) (all leaves re-certified independently) |
| eg_disc_s | 3.36596129 (SCIP) | 5.760539610694994 | 5.7605396164535107 (exactly feasible) | 1.0e-9 rel. | same | verified (all leaves) |
| eg_disc2_s | 0 (SHOT) | 5.642100574331458 | 5.6421005799711068 (exactly feasible) | 1.0e-9 rel. | same | verified on all 1,114,361 leaves under A1/A2; separate outward-rounded interval sample: 10,404 leaves of parts 0 and 2–7 |

For lnts50–400, dtoc5, lukvle10, chain50–400 and
powerflow0030p/0039p/0039r, exactly feasible points have now been constructed
and independently reviewed in publication/primal/. The gaps use the upper
ends of their objective enclosures. The lnts gap cells use the displayed
summary duals; against the certified verifier N·h2 bounds the gaps are at
most 5.55e-13. The lukvle10 KKT agreement is numerical and does not prove
global optimality; attributing its remaining gap to the dual requires that
additional assumption.

## Relaxation certified; OSIL models exactly infeasible

| instances | best listed dual | our result | primal | gap | mechanism | verification |
|---|---|---|---|---|---|---|
| kan_r3_h1_n4/n5/n9, kan_r5_h1_n3/n5/n8 | 0.0003908 … −789.74 (GUROBI) | optimum of the network relaxation R certified to ~1e-10 (e.g. kan_r5_h1_n8: 0.0693278605…) | improved primal values for r5_n3, r5_n5, r5_n8 (listed 0.3606 → 0.0693 for n8) | ~1e-10 | reduced-space interval B&B over the inputs | [verified](reviews/wave3-verification/verification-report.md); **the OSIL models have no exactly feasible point** (proved), so the claim concerns R |

## Instances substantially improved but not closed

| instance | best listed dual | our rigorous dual | best primal | gap after | verification |
|---|---|---|---|---|---|
| waterno2_06 | 165.19 | **278.230573** (separator branching: 272.584700; wave 2: 263.735099) | 282.888038 (exactly feasible) | 1.68% (3.78%; 7.26%) | wave 2 [verified](reviews/waterno2-verification/verification-report.md); separator branching [verified](reviews/waterno2-sepbranch-review.md); cell-dependent slopes [verified](reviews/waterno2-cellslopes-review.md) (all 49,315 pair bounds re-bounded independently) |
| waterno2_09 | 273.90 | 824.834692 | 914.012 (exactly feasible) | 10.82% | [verified](reviews/waterno2-recheck.md) (all periods) |
| waterno2_12 | 479.51 | 2089.754565 | 2233.821346 (exactly feasible) | 6.90% | verified (all periods) |
| waterno2_18 | 770.74 | 4790.820715 | 5023.983 (exactly feasible) | 4.87% | verified (all periods) |
| waterno2_24 | 1095.13 | 6576.151388 | 6963.795181 (exactly feasible) | 5.90% | verified (all periods) |
| ann_cumene_tanh | none | **−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point) | −3379.9823940 (exactly feasible) | 0.194% (wave 3: 19%) | wave 3 verified with caveats; extension [independently re-certified](reviews/ann-extension-review.md) |

Percent gaps: (primal − dual)/|dual| for waterno2; (primal − dual)/|primal|
for ann_cumene_tanh (under the waterno2 convention its wave-3 gap would be
16.0%; the new 0.194% is the same under both).

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
exact slope correction, and refined further: 278.230573774 (gap 1.67%).
waterno2_09–24 were not attempted with separator branching or cell slopes. Mechanism (ann_cumene_tanh): a reduced-space branch and bound
over the 5 inputs with affine arithmetic (one noise symbol per tanh
neuron), a per-box LP dual evaluated rigorously, and domain reduction
([note](open-instances-wave3/ann/extension.md)); the remaining gap sits
along a nearly flat constraint surface.

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
  difference is at least 1.42e-5 absolute, 1.4e-6 relative).
- "A solver reported a local optimum as a bound" is an inference, not
  verified.

Earlier individual findings:

- **Listed LINDO dual bounds that are not valid bounds** (interval Krawczyk
  existence proofs of exactly feasible points below them): methanol50 (by
  1.2%), rocket100, rocket200, rocket400 (by 1.1e-7, 4.7e-8, 1.9e-7, about
  1e-7 relative, below MINLPLib's 1e-6 tolerance; MINLPLib already marks
  these unsolved, and they are not among the audit's 19 pairs, which
  include methanol50).
- **SCIP 10.0.2 wrong optimal values** on three waterno2 period subproblems
  (exactly feasible points 1.0–2.4 below SCIP's claimed optima; cause: an
  invalid in-tree bound reduction, most likely in the nonlinear constraint
  handler's propagation; a debug build would be needed to pin it down).
  Reproducer: `open-instances-wave2/waterno2/scip_unreliable.py`. Not
  reported upstream. The separator-branching run found a further
  inconsistency: on a single cell-pair subproblem SCIP claimed "optimal" at
  55.69 or at 65.12 depending on the random seed; SCIP's own points, feasible
  within its tolerances (row violations up to 1.5e-8, bound and integrality
  violations up to 9.6e-7), lie 9.4 below the
  higher claim (not exactly feasible; no exactly feasible point near them
  was constructed; no cause established;
  `open-instances-wave2/waterno2/sepbranch/`, reproduced by the review).
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
candidates (plus the 11 first-wave instances, which the scout excluded);
the tables cover 31 instances closed for the model as written (all
independently verified, eg_disc2_s on every leaf under A1/A2 with a separate interval sample; camshape100 and lnts50 were already within 1.2e-6
and 3.8e-5 relative of closure by single-solver bounds; exactly feasible primal points now also cover the 13 formerly tolerance-only instances, see the note below the first
table), 6 KAN instances whose OSIL models are exactly infeasible but whose
intended network relaxation is certified to about 1e-10, 5 waterno2
instances substantially improved (waterno2_06 three times, now within
1.67%), and a finite dual for ann_cumene_tanh, now within 0.194% of the
primal. The three eg_* instances were closed in round 4 (in wave 3,
eg_int_s and eg_disc2_s stayed below the listed bounds and eg_disc_s was
not run; eg_int_s had been solved in floating point in the literature).
