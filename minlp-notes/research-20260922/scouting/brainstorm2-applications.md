# Brainstorm 2: application classes where a specific theoretical advance could unlock global solving

Date: 2026-09-23. Author: application-lens scouting agent. No repository file other
than this report was changed. Probe scripts and logs are in `/tmp/b2probe/`
(temporary): `water_disagg.py` (per-pipe disaggregation of waternd GAMS models),
`pole.py` (heatexch_gen1 pole point, checked with the repository's `osil_eval.py`),
`grb_run.py`, `scip_run.py`, and `run_*/out.txt` logs. The formulas needed to
reproduce the probes are given below.

Scope. For each target: the theorem or algorithm to prove, why the application
matters, evidence that global solving is stuck, what is known (bounded literature
searches, 2022–2026 emphasis), a validation plan, and risks. "Known" statements are
from papers found in this session or that I am confident about; items marked
*(verify)* were not checked. A failed search does not establish novelty.

Probe tools: SCIP 10 through GAMS 54.3 (one thread) and through PySCIPOpt 6.2.1;
Gurobi 13.0.3 through the repository's OSiL builder
(`benchmark-observations/code/grb_build.py`). All probe bounds are floating-point
solver claims, not certified bounds. Gurobi incumbents were not re-evaluated with
`osil_eval.py`.

## 0. Ranking

| Rank | Target | Evidence of being stuck | Probe result | Novelty risk | Impact |
|---|---|---|---|---|---|
| 1 | Heat exchanger networks: exact hull of the exchanger unit (LMTD, area, on/off, concave area cost) | heatexch_gen1–3 listed gaps 9–54%, but part of this is a modeling artifact (see Section 1); physical gen3 gap stays about 21% with known cuts | For the physical model (exact LMTD), LMTD tangent cuts give gen1 a dual bound of 153,206 against primal 154,896 (1.1%); gen3 does not improve. The literal MINLPLib gen1 model has poles: a point with objective 115,749 < listed primal 154,896 exists | medium: tangent planes are Zamora–Grossmann (1997–1998); the unit hull with shared temperatures and concave cost is the open part | high (process design, energy) |
| 2 | Multiperiod blending: hull of the tank-epoch (charge/discharge) quality recursion | 20 mpbp instances listed with no bounds at all | Gurobi 13: 2 of 9 solved; 7 have gaps 2.5–47% after 300–600 s | medium: single-period pooling hulls are known; the time-chained set is not, as far as found | high (refining, crude scheduling, produced water) |
| 3 | Water network design: network-level (cycle/flow-space) bounds | Modena 16% (BARON, days), Pescara 8%; Tasseff et al.'s exact MICP leaves 34–42% / 5% | Per-pipe disaggregated (hull-type) formulation: +2.0% root bound on Modena, none on Pescara, so the missing strength is network-level | high: Eiger–Shamir–Ben-Tal (1994) flow-space duality is the precedent | high (utilities) |
| 4 | Kinetic parameter estimation (discretized ODEs): exactness of reduced-space bounds | gasoil, methanol, pinene (11 instances) have dual bound 0 or none | SCIP 600 s on gasoil50: no primal and no finite dual bound | medium: reduced-space global dynamic optimization is known; the collocation-root theorem is not, as far as found | medium-high (chemical kinetics, systems biology) |
| 5 | Location–inventory with square-root risk pooling: recognition of concave-of-modular terms | supplychainp1 gap 26% (reformulated twin supplychainr1: 1.1%) | not probed | low novelty (Atamtürk–Berenguer–Shen 2012) | medium; cheap solver win |
| 6 | AC transmission switching and OPF: on/off QC/SOC hulls recognized in generic QCQP form | transswitch/powerflow: dual bound 0 on most instances in MINLPLib | not probed (scout: SCIP dual 0 in 60 s) | crowded | high, but mostly implementation |
| 7 | Sparse regression with indicators: rank-one hulls with box (big-M) bounds for n ≥ 3 | certified best subset stalls at high correlation / low SNR | not probed | crowded | medium |
| 8 | D-optimal design and maximum-entropy sampling | n = 124 MESP cases still take days | not probed | very crowded | medium |

Considered and rejected (Section 9): gas nomination (now solved on GasLib-582),
tree ensembles and neural networks (crowded; repository lesson 1), unit commitment
(MINLPLib gaps below 0.2%), hydro scheduling (gaps 1–2%), chance-constrained
facility location sfacloc (large gaps, structure not assessed).

---

## 1. Heat exchanger network synthesis: the exchanger-unit hull

**Target.**
- (A) *Known ingredient, missing in solvers.* The log mean temperature difference
  `L(a,b) = (a−b)/ln(a/b)` is concave and positively 1-homogeneous on `R^2_{++}`.
  Hence its hypograph is exactly the intersection of the half-spaces through the
  origin `L(a,b) <= L_a(1,t)·a + L_b(1,t)·b`, `t > 0`, with
  `L_a(1,t) = (ℓ − (1−t))/ℓ^2`, `L_b(1,t) = ((1−t)/t − ℓ)/ℓ^2`, `ℓ = −ln t`
  (at `t = 1` the cut is `L <= (a+b)/2`). Also `sqrt(ab) <= L(a,b)`. Generic
  solvers see `(a−b)/log(a/b)`, whose interval evaluation is unbounded because of
  the removable singularity at `a = b`; the area bound `A >= Q/(U·L)` then relaxes to
  `A >= 0`.
- (B) *Main theorem to prove.* The closed convex hull of the exchanger unit
  `X = {(Q, A, T, z) : z = 1 ⇒ Q <= U·A·L(ΔT1(T), ΔT2(T)), ΔT_i >= ΔT_min,
  0 <= Q <= Q_max; z = 0 ⇒ Q = A = 0}`, where `ΔT_i` are affine in stage temperatures
  `T` that are shared with other units (they are not switched off). Homogeneity
  gives `A·L(d1,d2) = L(A·d1, A·d2)`, so the `z = 1` piece is a convex constraint in
  `(Q, w1, w2)` with `w_i = A·d_i`. The target is an explicit description (or an
  exact separation oracle) that replaces the big-M approach-temperature rows, in the
  spirit of the repository's hulls with shared intensive variables
  (`results/scaling-disjunctions-hull.md`).
- (C) *Concave area cost.* With cost `c·A^β` (β ≈ 0.6–0.83) and area
  `A = Q/(U·L(d))`, the cost is `g(Q/L(d))` with `g(s) = c·(s/U)^β`. The function is
  0-homogeneous in `(Q, d1, d2)`, so it is constant on rays. Target: the convex
  envelope of `g(Q/L(d))` on a box (with the on/off disjunction), reduced to a
  one-dimensional problem in the ratio `Q/L(d)`, with a closed form or `O(1)`
  separation.

**Why it matters.** Heat integration is part of almost every chemical process
design and retrofit, and the Yee–Grossmann stage-wise superstructure is the standard
MINLP model. Industrial-size problems (10–40 streams) are solved heuristically or
sequentially (pinch analysis, then MINLP). Certified bounds would show how far these
designs are from optimal.

**Evidence stuck.** MINLPLib lists heatexch_gen1 with dual 100,552 against primal
154,896 (gap 54%), gen2 9%, gen3 16%. In the probe, default SCIP kept the gen1 dual
bound at 100,500 for 300 s and 49,000 nodes. The literature reports global solutions
only for small problems (Björk–Westerlund 2002; Faria–Kim–Bagajewicz 2015–2017).

**Benchmark artifact found in the probe (important).** The MINLPLib rows are
`L = (a − b)/log(a/(1e-6 + b))`, not the LMTD. This expression has a pole at
`a = b + 1e-6`. The approach temperatures `a, b` are only bounded above by the
stream temperature differences, so the model may choose `a = b + 1e-6 + ε`. Then
`L` is huge and the area `2Q/(0.01 + L)` is nearly zero. The utility rows have the
same defect, because `log(0.0142857140816327·x)` uses a rounded `1/70` and has a pole
at `x = 70.000001`. Starting from the best known configuration (binaries fixed,
continuous values re-solved by SCIP, objective 154,895.93), I moved the approach
temperatures of the active exchangers onto the poles and recomputed the defined
variables. In 60-digit arithmetic the resulting point has objective **115,748.7**
(with `ε = 1e-30`; 115,816.1 with `ε = 1e-9`). Its maximum row and bound residuals,
9.0e-7 and 1.0e-7, are those of SCIP's own incumbent. In double precision the pole
rows cannot be evaluated reliably (residual 0.28 on one row with `ε = 1e-9`). Hence
the listed primal 154,896 is not optimal for the literal gen1 model, and SCIP's dual
bound 100,500 may be close to the literal infimum. gen2 and gen3 contain the same
`1e-6 + x` and rounded-coefficient terms (not checked for exploitability). For
research, use the physical model (exact LMTD or Chen's approximation), and report
this to the MINLPLib maintainers.

**Known.**
- Zamora & Grossmann (1997–1998): "approximating planes that bound the LMTD from above",
  which are the tangent planes in (A), plus convex underestimators of area.
- Mistry & Misener (Comput. Chem. Eng. 94, 2016): convexity of `LMTD^β` for `β < 0`,
  shape for `β <= 1`, and an MILP approximation.
- Envelopes of functions that are concave in some variables and linear in others:
  Tawarmalani–Sahinidis convex extensions; Khajavirad–Sahinidis (2012–2013). These
  give tools for (B) but, as far as found, not the exchanger unit with shared
  temperatures and on/off.
- Recent HENS work (2022–2025, e.g., enhanced stage-wise superstructures) is mostly
  modeling or heuristic.

**Probe (done).** I added the 9 tangent cuts `t ∈ {1/16, …, 16}` for each LMTD row
(validity for the exact LMTD checked on 10^5 random points) and ran SCIP for 300 s,
one thread. The cuts are valid for the exact LMTD but cut off the pole points of the
literal rows, so the last two columns are bounds for the physical model (up to the
1e-6 perturbation away from the poles), not for the MINLPLib instance:

| Instance | Listed dual / primal | SCIP default | + 12 AM cuts (`t = 1`) | + 9 tangents per LMTD row |
|---|---|---|---|---|
| heatexch_gen1 | 100,552 / 154,896 | 100,500 | 147,088 (146,123 already at 30 s) | 153,206 (152,224 already at 24 s) |
| heatexch_gen3 | 56,003 / 64,844 | 55,858 | 55,229 | 53,378 |

All values are dual bounds at the 300 s limit. For the physical gen1 model the gap to
the best known primal is 1.1% (the listed primal is a physical point). On gen3 the
cuts do not help, and the physical gap stays about 21% against the listed primal
64,844: the model has the concave area cost `146·(0.01 + A)^0.6` and larger
split-mixing bilinear systems, which (B) and (C) address. The gen1 result comes from
a known inequality; the research contribution is (B)–(C).

**Validation.** MINLPLib heatexch_gen1–3, heatexch_spec1–3, synheat and ex1233;
the minlp.org HENS library; the Yee–Grossmann and Escobar–Trierweiler (2013) test
sets. Compare root and 1-hour dual bounds with SCIP, Gurobi 13 and BARON, with and
without the hull cuts; count instances solved.

**Risk.** (A) is known, so the headline cannot be the tangent cuts. (B) may reduce to
a known disjunctive-programming corollary; its value then lies in an explicit
description that avoids lifting. Stream-split bilinear energy balances may dominate
the gap on larger instances (gen3 suggests this).

---

## 2. Multiperiod blending: the tank-epoch hull

**Target.** In multiperiod blending (Lotero et al. 2016; mpbp and crudeoil families),
a tank either charges or discharges in each period (exclusivity binaries). Write
the component inventory `M_t = I_t·C_t`. Charging is then linear
(`M_{t+1} = M_t + F·c_in`). Discharging is the only nonlinear event: the outflow
composition equals the tank composition, `G = F·M/I`.
- (A) Between two charging events the tank composition is constant. Introduce one
  composition vector per charge epoch; every discharge in that epoch is then a
  product `(epoch composition) × (flow)`. Prove that the convex hull of a single tank
  over the horizon, for a fixed charge/discharge pattern, is described by the
  single-pool pooling hulls applied per epoch plus linear epoch-transition rows.
- (B) Describe the hull of the union over patterns, with the exclusivity binaries,
  or give an exact separation oracle that is polynomial in the horizon.
- (C) Show when the epoch formulation dominates the standard source- and
  concentration-based formulations, and bound the number of epochs that can be
  active in some optimal solution.

**Why it matters.** Refinery crude scheduling, gasoline blending, water and
produced-water storage, and lithium recovery from produced water (2023 study). It is
the scheduling generalization of pooling, which is a solver benchmark class.

**Evidence stuck.** MINLPLib added 20 mpbp instances on 2026-03-18 with no listed
primal or dual bounds. The earlier scout found that SCIP in 120 s solved 1 of 20 and
found no feasible point on 12. Crude-oil families crudeoil_li* and
crudeoil_pooling_ct1 (gap 21%) remain open.

**Probe (done).** Gurobi 13, NonConvex=2, 2–4 threads, 300–600 s (all mpbp are
maximization problems):

| Instance | Primal | Dual | Gap |
|---|---|---|---|
| mpbp_06 | 337.155 | 337.155 | solved, 25 s |
| mpbp_19 | 1203.22 | 1203.29 | solved to tolerance, 85 s |
| mpbp_31 | 1808.12 | 1854.19 | 2.5% |
| mpbp_03 | 2040.27 | 2127.49 | 4.3% |
| mpbp_22 | 4313.25 | 4521.18 | 4.8% |
| mpbp_47 | 5047.06 | 5369.71 | 6.4% |
| mpbp_46 | 5963.45 | 6498.49 | 9.0% |
| mpbp_04 | 705.91 | 817.43 | 15.8% |
| mpbp_36 | −2031.16 | −1384.58 | 47% (MINLPLib convention) |

These are first bounds for instances listed with none. The family is not uniformly
stuck, because small instances solve, but most remain open at 5–10 minutes.

**Known.**
- Chen & Maravelias: preprocessing and tightening (JOGO 2020), variable-bound
  tightening and valid constraints (INFORMS J. Comput. 2022), and LP-based
  preprocessing (Ind. Eng. Chem. Res. 2024).
- Ovalle, Bhatia, Laird & Grossmann (Ind. Eng. Chem. Res. 65(7), 2026): logic-based
  decomposition with symmetry-breaking cuts.
- Single-pool hulls: Luedtke, D'Ambrosio, Linderoth & Schweiger (SIAM J. Optim.
  2020); Jalilian & Kocuk (rank-one nonnegative matrices with bounded sums, SOC
  representable, arXiv 2306.10810); Castro (2015) multiperiod pooling formulations.
- Repository: many pooling complexity results, but no multiperiod hull.

**Validation.** All 20 mpbp, crudeoil_li01–21, crudeoil_pooling_ct/dt, and the
Lotero and Chen–Maravelias instance sets. Gurobi 13 and SCIP with the epoch
formulation or cuts against the MINLPLib formulation, 1 hour.

**Risk.** Medium. The epoch structure may already be implicit in source-based
formulations. Symmetric patterns may dominate the difficulty (Ovalle et al. target
symmetry), in which case hulls help less than branching rules.

---

## 3. Water network design: network-level bounds

**Target.** The MINLPLib waternd models (Bragalli et al. 2012) link the diameter
choice to the head loss through a continuous area variable:
`signpower(q, 1.852) = k·(c·A)^{2.435}·(h_i − h_j)` with `A = Σ_d a_d b_d`. The probe
below shows that replacing this by the per-pipe disjunctive (hull-type) formulation
closes little. The missing strength is network-level. Targets:
- (A) For fixed flows, the LP relaxation of one-hot diameters is the split-pipe LP
  (known identity). Its value `F(q)` equals `min_h Σ_a C_a((h_i − h_j)/φ(q_a))`,
  where `C_a` is the convex decreasing lower hull of the catalogue points
  (resistance, cost). If the catalogue has a power-law minorant
  `C̃_a(r) = κ r^{−α}` with `1.852·α < 1`, then `F̃(q)` is concave in `q` on each
  flow-direction orthant, because it is a minimum over `h` of functions concave in
  `q`. Therefore a valid lower bound is a concave minimization over the flow
  polytope, attained at a vertex. Prove this with an explicit error term for
  catalogue kinks (at kinks, `F` itself is not concave), and give a simplicial
  branch-and-bound in the cycle space (dimension about 30 for Pescara and 45–50 for
  Modena).
- (B) Monotonicity: decide whether, with a single source and fixed demands,
  increasing any pipe's conductance cannot lower any node head. For linear
  networks, the sign of `(L_s^{-1} b_e)_v` suggests it can fail. If it holds for the
  instances, feasible designs form an up-set and lifted cover cuts from
  infeasibility certificates are exact. If it fails, give the counterexample
  (a Braess-type pressure paradox).

**Why it matters.** Water distribution design is a large capital-investment problem
for utilities. The benchmark networks are real (Modena, Pescara, Foss, Balerma).

**Evidence stuck.**
- Tasseff, Bent, Epelman, Pasqualini & Van Hentenryck (arXiv 2010.03422): an exact
  MICP reformulation; gaps after days: foss_poly_1 about 4–5%, Pescara 5.3%, Modena
  34–42%.
- Choudhary, Dey & Sahinidis (preprint, about 2024–2025): new best primal values
  (Pescara 1,812,564; Modena 2,539,446); BARON lower bounds give gaps of 8.2% and
  16.1%.
- MINLPLib listed gaps: Modena 24%, Pescara 17%, fosspoly1 1162%.

**Probe (done).** SCIP 600 s, one thread; disaggregated model =
`q = Σ_d q_d`, `h_i − h_j = Σ_d Δh_d`, `signpower(q_d, 1.852) = R_d·Δh_d`,
`|q_d| <= v·a_d·b_d`, `|Δh_d| <= min(H, (v a_d)^{1.852}/R_d)·b_d`:

| Instance | Listed dual | BARON LB (Choudhary et al.) | SCIP original, 600 s | SCIP disaggregated | Best primal |
|---|---|---|---|---|---|
| waternd_pescara | 1,570,816 | 1,663,840 | 1,639,167 | 1,637,436 (600 s) | 1,812,564 |
| waternd_modena | 2,082,121 | 2,130,040 | 2,120,741 | 2,163,336 (600 s, still at the root) | 2,539,446 |

The per-pipe hull closes about 2% of the Modena bound and nothing on Pescara. About
15% (Modena) and 9–10% (Pescara) remains. This supports a network-level target.

**Known.** Eiger, Shamir & Ben-Tal (Water Resour. Res. 1994): split-pipe inner LP,
flows as outer variables, semi-infinite dual, and global branch-and-bound;
Sherali, Subramanian & Loganathan (2001) RLT; Raghunathan (SIAM J. Optim. 2013);
Tasseff et al.; the repository's potential-flow results (cactus cycle thresholds
that are linear in resistances, `results/potential-flow-cycle-polytope-resistance-design.md`).

**Validation.** waternd_* (MINLPLib), the Tasseff instance set, and Balerma and
New York; compare against the BARON and Tasseff bounds above.

**Risk.** High. The concavity route may give weak bounds, because the power-law
minorant loses catalogue detail. Eiger et al. may already contain much of (A).
Solving a 45-dimensional concave minimization is itself hard.

---

## 4. Kinetic parameter estimation with discretized ODEs: exact reduced-space bounds

**Target.** COPS instances in MINLPLib (gasoil: 3 parameters; methanol and
pinene: 5) are full-space collocation models with no state bounds. The parameters
are few, so branching only on parameters is natural. That is exact for the MINLPLib
model only if every real solution of the collocation equations is accounted for.
Implicit schemes have spurious real roots: implicit Euler for `y' = −k y^2` has the
root `y ≈ −1/(hk)` in addition to the physical one. Targets:
- (A) For polynomial mass-action kinetics with positive parameters in a box and a
  given collocation scheme (Radau IIA as in COPS), characterize all real solutions
  of the stage equations: the physical branch is unique in an explicit region
  (step-size condition via one-sided Lipschitz or M-matrix arguments), and spurious
  branches have states outside an explicit box.
- (B) A lower bound on the least-squares objective on every spurious branch (they
  cannot fit data in `[0,1]` within the incumbent value), so the instance's global
  optimum is on the physical branch.
- (C) With (A)–(B), a parameter-space branch-and-bound with interval or McCormick
  enclosures of the implicit states (Stuber–Scott–Barton 2015) gives certified bounds.
  The repository's cluster-free theorem for reduced-space schemes applies to its node
  count.

**Why it matters.** Parameter estimation of reaction kinetics is routine in chemical
engineering and systems biology, and local fits are known to land in poor local
minima.

**Evidence stuck.** MINLPLib: gasoil50–400 dual bounds about 1e-8 against primal
0.0052; methanol50–400 and pinene dual bound 0; catmix has none. Probe: SCIP 600 s on
gasoil50 found no feasible point and no finite dual bound. Fernández de Dios et al.
(arXiv 2405.01989, 2024) report that deterministic methods handle about five states
and five parameters at most.

**Known.** Esposito & Floudas (2000); Singer & Barton (2006); Mitsos, Chachuat &
Barton (2009); Stuber, Scott & Barton (2015); full-discretization with piecewise
McCormick and outer approximation (Miró et al., BMC Bioinformatics 2012). None that I
found addresses spurious collocation roots of the full-space model.

**Validation.** gasoil, methanol and pinene families (11 instances), plus the
Fernández de Dios et al. set. Metric: first finite certified dual bounds; time to a
1% gap.

**Risk.** Medium. (A) may need step sizes smaller than those in the instances. If
spurious branches can fit the data, the MINLPLib optimum is non-physical; that would
itself be a publishable benchmark fact.

---

## 5. Location–inventory with square-root risk pooling: recognize concave-of-modular terms

**Target.** Terms `sqrt(Σ_j σ_j^2 y_ij)` (and EOQ terms `sqrt(Σ_j d_j y_ij)`) with
binary assignments are concave functions of modular functions. Their sum is
submodular, so the convex envelope on the binary cube is the Lovász extension, which
can be separated exactly by a greedy sort (extended polymatroid cuts). Research
target: the hull with a single-facility capacity knapsack (submodular cost plus
knapsack), where no exact description is known *(verify)*, and an automatic
detector for generic solvers.

**Evidence.** supplychainp1_053050: listed gap 26%; the reformulated twin
supplychainr1: 1.1%. Known: Atamtürk, Berenguer & Shen (Oper. Res. 60(2), 2012);
Atamtürk & Narayanan (2008). Low theoretical novelty for the uncapacitated case;
high certainty of a benchmark gain.

**Risk.** Low; mostly a known-theory transfer.

---

## 6. AC transmission switching and OPF: on/off QC/SOC hulls in generic form

**Target.** A theorem stating which moment/minor cuts derivable from a generic
QCQP (e.g., 2×2 minors of the `(e_i, f_i, e_j, f_j)` moment matrix plus switching
perspectives) imply the Jabr SOC and on/off QC relaxations, so generic solvers can
derive them without power-flow knowledge.

**Evidence.** transswitch*/powerflow*: dual bound 0 on most instances in MINLPLib.
**Known and crowded:** Kocuk, Dey & Sun (2017); Bestuzheva, Hijazi & Coffrin (on/off
quadratic constraints, INFORMS J. Comput. 2020); IJOC 2023 "AC OPF with discrete
decisions to global optimality"; QC branch-and-bound on PGLib-OPF (arXiv 2505.18435,
2025); tightened QC envelopes (arXiv 2310.14463). The gap is implementation; the
new theory would be thin.

---

## 7. Sparse regression and MIQP with indicators: rank-one hulls with bounds

**Target.** The convex hull of `{(x, z, t) : t >= (a^T x)^2, l_i z_i <= x_i <= u_i z_i,
z ∈ {0,1}^n}` for `n >= 3` with finite bounds (big-M), and with a cardinality row.

**Known and crowded.** Atamtürk & Gómez (rank-one convexification); Wei, Gómez &
Küçükyavuz (2022); Shafiee & Kılınç-Karzan (rank-one with constraints on `z`, 2024);
Han & Gómez (low-rank extended formulations); De Rosa & Khajavirad (Math. Program.
2024: bivariate case with bounds); Hazimeh, Mazumder & Saab (L0BnB, 2022); step
function penalties (arXiv 2504.16330, 2025). The bounded n-variate case seems open
*(verify)*, but the expected solver gain is small because big-M bounds are usually
loose in practice.

---

## 8. D-optimal design and maximum-entropy sampling

**Known and very crowded.** Fampa & Lee survey (arXiv 2507.05066, 2025–2026),
augmented factorization bound, generalized scaling (Math. Program. 2024),
hyper-scaled NLP bound (arXiv 2601.20970), majorization to scaling
(arXiv 2604.10363), relations between MESP and 0/1 D-Opt (arXiv 2511.04350), and
exact design by column generation (Math. Program. Comput. 2026). The n = 124
benchmark still takes days for some `s`, but a new bound would compete with five
active groups. Not recommended.

---

## 9. Considered and rejected

- **Gas network nomination and design.** No longer stuck on GasLib-582: LANL's
  relaxations prove optimality on 4203 of 4222 nominations (LA-UR-23-29790), and an
  improved MINLP formulation solves all 100 test instances within 143 s (arXiv
  2501.11608, 2025). MINLPLib gasnet (9%) is small.
- **Tree ensembles and neural networks.** Crowded (Mišić 2020; Mistry et al. 2021;
  prescriptive-tree formulations 2025). The repository's NN study found valid but
  slow cuts. MINLPLib ann_*_tanh have no dual bound, probably from missing input
  bounds *(not checked)*.
- **Unit commitment.** MINLPLib unitcommit gaps are 0.02–0.16%.
- **Hydro scheduling.** hydroenergy2/3 gaps 1–2%.
- **Chance-constrained facility location (sfacloc, Lejeune & Margot, Oper. Res.
  2016).** Gaps from 20% to 30×, trilinear rows. The structure was not assessed; it
  could deserve a separate scout.

## 10. Recommendation

1. Record the heatexch_gen pole artifact as a benchmark fact after an independent
   check (a second agent should rebuild the pole point from the OSiL file and extend
   the check to gen2 and gen3).
2. Start with target 1, parts (B)–(C), on the physical model. On gen1 the bottleneck
   was a structural fact that generic solvers cannot see (concavity and homogeneity
   of the LMTD behind a removable singularity). gen3 shows what the known cuts leave
   open (about 21%).
3. Target 2 is next: 20 instances without listed bounds, 7 of 9 still open after
   5–10 minutes of Gurobi, and a clear structural hypothesis (charge epochs).
4. Target 3 has the largest application value but the highest risk. Spend one day on
   the concavity lemma (A) and the monotonicity question (B) on Pescara before
   committing.
5. Target 4 needs first a check for spurious collocation roots on gasoil50 (cheap:
   solve the stage equations at the known optimal parameters from many starting
   points).

## Sources

- Tasseff et al., exact MICP for water network design: https://arxiv.org/abs/2010.03422
- Choudhary, Dey & Sahinidis, water network design and operation: https://www2.isye.gatech.edu/~sdey30/WaterPWL1.pdf
- Eiger, Shamir & Ben-Tal (1994): https://agupubs.onlinelibrary.wiley.com/doi/10.1029/94WR00623
- Sherali et al. global water design: https://link.springer.com/article/10.1023/A:1008207817095
- Chen & Maravelias, multiperiod blending: https://pubsonline.informs.org/doi/10.1287/ijoc.2021.1140 ; https://link.springer.com/article/10.1007/s10898-020-00882-3 ; https://pubs.acs.org/doi/abs/10.1021/acs.iecr.3c03166
- Ovalle et al. (2026): https://pubs.acs.org/doi/10.1021/acs.iecr.5c02853
- Jalilian & Kocuk, pooling rank-one relaxations: https://arxiv.org/html/2306.10810
- Mistry & Misener (2016), LMTD convexity: https://www.sciencedirect.com/science/article/pii/S0098135416302216
- Global HENS (Zamora–Grossmann planes, Björk–Westerlund): https://www.sciencedirect.com/science/article/abs/pii/S0098135402001291
- Fernández de Dios et al., ODE parameter estimation solvers: https://arxiv.org/abs/2405.01989
- Atamtürk, Berenguer & Shen (2012): https://pubsonline.informs.org/doi/10.1287/opre.1110.1037
- AC OPF / OTS: https://arxiv.org/pdf/2505.18435 ; https://arxiv.org/pdf/2310.14463 ; https://dl.acm.org/doi/abs/10.1287/ijoc.2023.1270 ; https://arxiv.org/pdf/2212.12097
- Sparse regression: https://arxiv.org/pdf/2303.18158 ; https://arxiv.org/pdf/2504.16330 ; https://link.springer.com/article/10.1007/s10107-024-02173-1
- MESP / D-opt: https://arxiv.org/abs/2507.05066 ; https://arxiv.org/pdf/2601.20970 ; https://arxiv.org/pdf/2604.10363 ; https://link.springer.com/article/10.1007/s12532-026-00326-1
- Gas networks: https://www.osti.gov/pages/servlets/purl/3017804 ; https://arxiv.org/pdf/2501.11608
- sfacloc: https://www.minlplib.org/sfacloc1_4_80.html ; ndcc: https://www.minlplib.org/ndcc12.html
