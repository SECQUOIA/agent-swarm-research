# Scout report: recurring structures in open MINLPLib instances

Date: 2026-09-22. Author: research scout (automated). Scratch data and scripts: `/tmp/scout/`.

## 0. Data, definitions, caveats

- Metadata: `https://www.minlplib.org/instancedata.csv`, fetched 2026-09-22 (1,633 instances). OSiL files: `~/.cache/minlplib/minlplib/osil` (1,632 files).
- **Gap definition used by MINLPLib (checked on acopf_case1354pegase_qcqp):** `gap = |primal - dual| / min(|primal|, |dual|)`. It is `inf` when a bound is missing, when the dual bound is 0, or when the bounds have opposite signs. Gaps above 1 are therefore common and are not percentages of the primal value.
- **Open** = listed gap > 1e-4, including missing primal or dual bound. Proven infeasible instances (no primal, dual = +inf, gap 0: ball_mk3_10/20/30, ball_mk4_05/10, ex7_3_6, gastrans582_freezing27, gastrans582_freezing27_95) are excluded.
- **Result: 538 open instances** (of 1,633). Of these, 522 are nonconvex (16 have `convex=True`). 318 have binaries, 212 are purely continuous. 137 have gap = inf: 57 have no dual bound, 41 have no primal bound, and 41 have dual bound exactly 0. Gap distribution: (1e-4,1e-3] 18; (1e-3,1e-2] 30; (1e-2,0.1] 101; (0.1,1] 130; (1,10] 77; >10 (finite) 44; inf 137.
- **Stale listings (verified with SCIP via PySCIPOpt 6.2.1, 1 thread, default settings):** mpbp_06 solved to optimality in 60 s (337.155); waternd_shamir solved in 60 s (419000). The 20 mpbp instances were added 2026-03-18 and have no listed bounds. So "open" is an upper bound for some recent families. Most other families are genuinely hard (see below).
- Structure statistics come from my own OSiL parser (`/tmp/scout/osil.py`), applied to all open instances except three files >60 MB (acopf_caseactivsg25k/70k, hadamard_9) and one missing file (fct). "Atom" = maximal nonlinear subterm under linear wrappers. Variable classes: `B` binary, `I` integer, `C` bounded continuous with lb >= 0, `C±` bounded continuous crossing 0, `Cu` continuous with an infinite declared bound. `EQ`/`IN` = equality or inequality row.
- Files: `open.csv` (full open list with metadata), `struct.jsonl` (per-instance structure), `agg.txt` (per-family atom and row signatures), `appendix.md` (the table in Section 6).

## 1. Family overview (structural grouping of the 538 open instances)

| family (structural grouping) | open | gap=inf | median finite gap | median vars | median bins | median cons | #with unbounded vars in nonlinear terms |
|---|---|---|---|---|---|---|---|
| geometry / packing / distance | 57 | 12 | 1.03 | 200 | 0 | 388 | 11 |
| discretized optimal control (COPS etc.) | 51 | 26 | 8.18 | 2403 | 0 | 1600 | 44 |
| misc | 47 | 17 | 0.0984 | 200 | 36 | 114 | 20 |
| BQP / binary polynomial (maxcut, QAP, CSP, qspp, coloring) | 34 | 2 | 0.297 | 525 | 525 | 50 | 1 |
| autocorr_bern (low-autocorrelation binary seq.) | 29 | 0 | 1.35 | 51 | 50 | 1 | 0 |
| binary quadratic w/ linear constraints (layout, partition, tournament) | 29 | 0 | 0.0534 | 562 | 552 | 299 | 0 |
| GlobalLib ex* | 27 | 4 | 0.392 | 14 | 0 | 8 | 10 |
| other pooling/blending (digabel, epa, crudeoil_pooling, mpbp) | 27 | 21 | 0.000891 | 1212 | 384 | 2744 | 2 |
| AC OPF (powerflow/acopf) | 24 | 9 | 0.802 | 2370 | 0 | 4741 | 17 |
| pooling_spp (Alfaki-Haugland style large pooling) | 24 | 0 | 0.0447 | 3739 | 0 | 4586 | 0 |
| AC OPF + line switching (transswitch) | 18 | 12 | 0.473 | 518 | 78 | 881 | 18 |
| nuclear core reload | 18 | 6 | 9.89 | 1565 | 612 | 1264 | 18 |
| arki (ARKI consulting) | 14 | 8 | 6.72 | 4689 | 0 | 3186 | 12 |
| network design w/ congestion/queue (ndcc, nd, telecomsp) | 14 | 0 | 0.387 | 891 | 54 | 352 | 11 |
| ML surrogate (ANN tanh / KAN / kriging) | 11 | 8 | 19.9 | 1006 | 216 | 1121 | 10 |
| multiplant/cyclic scheduling | 10 | 0 | 0.438 | 408 | 207 | 266 | 10 |
| waterund (water under design, pooling-like) | 10 | 0 | 0.0246 | 135 | 0 | 135 | 0 |
| sfacloc (stochastic facility location) | 9 | 0 | 1.74 | 261 | 30 | 421 | 0 |
| unit commitment / energy scheduling | 8 | 0 | 0.000921 | 25654 | 4471 | 55116 | 6 |
| water design (Karuppiah/Grossmann-type) | 8 | 0 | 0.61 | 195 | 28 | 137 | 7 |
| waternd (water network design, H-W signpower) | 8 | 1 | 0.0974 | 749 | 622 | 326 | 8 |
| waterno1 (water op., Darcy signpower) | 8 | 0 | 0.152 | 1255 | 112 | 1540 | 0 |
| generation with trig (deb/var_con) | 7 | 7 | nan | 573 | 20 | 507 | 7 |
| heat exchanger networks (LMTD / area) | 7 | 0 | 0.00859 | 112 | 12 | 120 | 7 |
| crude oil scheduling (Li) | 6 | 0 | 0.00797 | 1070 | 156 | 2973 | 0 |
| portfolio / finance | 6 | 2 | 0.0484 | 433 | 101 | 225 | 6 |
| CHP / power plant operation | 5 | 1 | 0.0814 | 2248 | 288 | 3850 | 0 |
| trim loss | 5 | 0 | 0.366 | 215 | 173 | 120 | 4 |
| wastewater (Castro) | 5 | 0 | 0.313 | 303 | 0 | 251 | 0 |
| waterno2 (water op., trig/polynomial pump) | 5 | 0 | 7.07 | 1992 | 108 | 2470 | 0 |
| hadamard | 4 | 1 | 21.5 | 57 | 56 | 1 | 0 |
| topology optimization | 3 | 0 | 15.7 | 33600 | 2400 | 14323 | 3 |

"misc" (47) holds singletons and small groups: 4stufen/beuster (membranes, log/div), bayes2, cesam2 (entropy SAM balancing), contvar, densitymod, dosemin (erf), eg_* (exp), etamac, feedtray, fuzzy, gams01/03/05, gasnet, gasprod_sarawak (pooling-type q*F with binaries), ghg, infeas1, like, lop97ic, pedigree_sim, pindyck, pricing050, procurement, quantum, routingdelay_proj, sepasequ_complex, sssd persp, supplychain (sqrt), uselinear, wastepaper.

## 2. Structural characterization of the main families (from parsed OSiL)

Dominant atom and row signatures are aggregated over all open instances of the family. See `agg.txt` for details.

### 2.1 Geometry / packing / dispersion (57 open; 12 inf)
- Instances: knp (7), elec (4), pointpack (3), polygon (4), ringpack (7), kall_* (9), p_ball (2), gabriel (6), tspn (4), space (3), ngone, maxmin, orth_d*_pl (2), eq6_1, shiporig, ball_mk4_15.
- Structure: reverse-convex pairwise distance rows `||x_i - x_j||^2 >= d_ij` or `>= t` (row signature `IN:(C)^2x4 | C*Cx2`: 24,871 rows), sphere equalities `||x_i||^2 = r^2` (knp, elec), trig in polar form for polygon (`r_i r_j cos(θ_i-θ_j)`), and 1/dist for elec (Coulomb energy). There are no binaries except in ringpack, p_ball, gabriel, space, and tspn. Point-permutation symmetry is massive.
- Known technique: spatial branch and bound with secant/McCormick relaxations. The relaxation of each concave constraint `-||x_i-x_j||^2 <= -t` is nearly vacuous, so the listed dual bounds are trivial. Example: all knp5-* have dual bound 4.0, the largest value that is compatible with the sphere radius.
- **Verified here:**
  - *polygon* (the COPS largest small polygon; one vertex fixed at the origin, so polygonN has N vertices). The isodiametric inequality gives area ≤ π/4, so the dual bound is ≥ -0.785398. That cuts the gap from 6.4/18.5/30.7/42.3 (listed) to 7.2e-3/1.9e-3/1.2e-3/4.4e-4.
  - For odd N (polygon25, polygon75), Reinhardt's theorem (1922) says the regular N-gon is optimal. I built it in the OSiL model and checked feasibility (maximum violation 3e-15). Its objective values, -0.7802321 and -0.7848240, beat the listed primal values -0.779751 and -0.7844638. So these two instances are solved by a classical theorem.
  - *knp5-40*: the D5 root system (40 vectors ±e_i±e_j scaled to radius 2) is feasible (checked, violation 9e-16) with objective 1.0 > listed primal 0.98486.
  - A grid-discretized Delsarte LP bound (Gegenbauer polynomials up to degree 24, 3,000 grid points; numerical, **not certified**) gives objective ≤ 1.1056 (knp3-12; listed primal 1.105573, which is optimal by Fejes Tóth's Tammes N=12 theorem), 1.0429 (knp4-24), and 1.0710/1.0577/1.0453/1.0337/1.0229 (knp5-40…44). The listed dual bounds are 2.28, 3.68, and 4.0.
- Why the gap remains: capacity or density information is global, because it aggregates all pairs, while solver relaxations are local, one pair at a time. Symmetry makes branching ineffective.
- Candidate question: **positive-definite-kernel aggregation cuts.** For any positive-definite kernel K on the domain (Gegenbauer kernels on spheres; PD functions on R^d or the torus for boxes), `Σ_{i,j} K(x_i,x_j) ≥ 0` holds for every configuration.
  - Combined with the pairwise constraints, these valid cuts give Delsarte/Cohn–Elkies-type bounds.
  - Open parts: can a B&B solver separate them with a symmetry-reduced LP or SDP on Gram-matrix variables? How strong are they for finite N inside containers (boxes, rectangles, circles) with unequal radii? Can local versions be used inside B&B nodes?
  - Touches ≈25–35 open instances (knp 7, elec 4, pointpack 3, kall circles/ellipsoids ≈9, ringpack 7, p_ball 2, maxmin, orth).

### 2.2 Discretized dynamic optimization: optimal control and kinetic parameter estimation (51 open; 26 inf)
- Instances: catmix, chain, gasoil, glider, lnts, methanol, pinene, popdynm, rocket, camshape (4 each), parabol (4), dtoc5, optcdeg2, junkturn, trainf, cont6-qq, hvycrash, truck, lukvle10. Most come from COPS or GAMS model library discretizations.
- Structure: equality chains `x_{k+1} = x_k + h·f(x_k, x_{k+1}, u_k, θ)`. The nonlinear parts are bilinear state×control (catmix: `x_k u_k`, including the implicit/trapezoid term `x_{k+1} u_{k+1}`) or state×parameter (pinene, gasoil, methanol: `θ·y` with unknown rate constants θ ≥ 0 unbounded).
  - Row signatures: `EQ:(Cu)^2`, `EQ:Cu*Cu x3`, `EQ:Cu*Cu`.
  - Median 799 continuous variables with infinite declared bounds appear in nonlinear terms. 44/51 instances have such variables.
  - Objectives are least squares (parameter estimation) or a terminal state.
- **Verified:** SCIP (60 s) returns no finite dual bound (-1e20) for catmix100, methanol50, and gasoil50. With a *heuristic* (not proven valid) box of [-0.1, 1.1] on all unbounded variables, catmix100 gets dual -0.154 vs primal -0.0481. With [-10, 10] it gets -1.81. So finite bounds are necessary, but even then the per-step relaxation compounds and stays weak.
- Why the gap remains: states are not bounded in the model. FBBT cannot isolate `x_{k+1}` in implicit schemes. McCormick errors compound along the chain. Parameters are unbounded.
- Candidate question: **discrete-time invariance and reachable-set relaxations for one-step schemes with bilinear dependence.**
  - (a) Conditions under which the discretized system provably keeps positivity, conservation, or monotone comparison bounds. Examples: implicit Euler or trapezoid on Metzler/compartmental systems, which reduces to M-matrix conditions on `I - h A(θ,u)`. These bounds can be derived automatically.
  - (b) Tight convex relaxations of the k-step map, not per-step McCormick. For example, relax the product of one-step transfer matrices `Π (I - hA(u_k))^{-1}` for u in a box, or use the monotone dependence of the solution on θ.
  - Touches ≈40–51 open instances, plus any parameter-estimation or dynamic-optimization MINLP outside MINLPLib.

### 2.3 Multi-period blending with inventory tanks and operating modes (mpbp 20, crudeoil_li 6, crudeoil_pooling 2; related: gasprod_sarawak 2, pooling_epa3, blendgap)
- Structure, verified on mpbp_06:
  - Tank quality balance `I_t q_t = I_{t-1} q_{t-1} - F^out_t q_{t-1} + Σ_k c_k F^in_{k,t}` (rows `EQ: C*C x4..x10`). This is bilinear inventory×quality and flow×quality, chained over time.
  - Flows are switched by binaries (`b ≤ F ≤ 50 b`).
  - **Charge/discharge exclusivity** `b^out + b^in ≤ 1` (rows such as `b1 + b61 ≤ 1`).
  - A downstream blend tank has the same form, and product specs are bilinear. crudeoil_li is the continuous-time analogue (volume×composition).
- **Verified status:** SCIP, 120 s per instance on the 20 mpbp (maximization): 1 solved (mpbp_06). 12 have no feasible solution. For 5 others the dual/primal ratio is 1.2–2.7×, for example mpbp_22 at 5071.9/2426.5 and mpbp_04 at 1106.8/411.8. The remaining 2 (mpbp_03, mpbp_47) have negative incumbents against positive duals. Listed crudeoil_li gaps are 5e-4–0.037.
- Why the gap remains:
  - McCormick on `I_t q_t` ignores that, given the mode, the recursion is much simpler. In discharge mode the quality is unchanged (`q_t = q_{t-1}`). In charge mode the component mass `M_t = I_t q_t` is linear.
  - Errors compound over periods, and binaries enter only through big-M flow bounds.
- Candidate question: **convex hull (or a tight extended formulation) of the two-mode tank recursion** `{(I_{t-1}, q_{t-1}, F^in, F^out, I_t, q_t, z): mode z ∈ {charge, discharge, idle}}`, taken per period and then over a horizon of T periods. Two parts:
  - Does the disjunctive hull of the per-period set remain polyhedral, or SOC-representable, in the (I, M = I·q) variables?
  - How much of the chained bound does it close?
- Touches ≈28–32 open instances. It is distinct from the static pooling theory already in the repository, but novelty is **not checked**: Lotero et al. 2016, Kolodziej et al. 2013, and Ovalle/Bhatia/Laird/Grossmann 2026 are relevant.

### 2.4 AC optimal power flow, switching, generation with trig (powerflow 17, acopf 7, transswitch 18, deb/var_con 7; 49 open, 28 inf)
- Structure:
  - Rectangular form (`*r`, acopf): `C±*C±` and squares in equality power balance, `(Cu)^2` thermal limits.
  - Polar form (`*p`): `v_i v_j cos(θ_i-θ_j)`, `v_i v_j sin(...)`.
  - transswitch multiplies each line flow by a line-status binary: `B*Cu*Cu*cos(L)`. deb/var_con are similar, with sqrt(square) terms.
- **Verified:** SCIP 60 s gives dual 0 (or -1e-9) on transswitch0014r/0030r, powerflow0030p, deb10, var_con5. Listed duals are 0 for many.
- Known technique (literature, **not verified here**): SOC, QC, and SDP relaxations and their on/off extensions (Hijazi, Coffrin, Van Hentenryck; Jabr; Lavaei–Low) typically leave small gaps on these standard test systems. The main gap is **implementation, not theory**: general MINLP solvers do not build these relaxations.
- New-theory angle: the convex hull of the on/off trig-bilinear set `{(z, v_i, v_j, θ_ij, w^c, w^s): w^c = z v_i v_j cos θ_ij, ...}` for switching, and automatic recognition of these structures in generic QCQP form. Touches 49.

### 2.5 Binary polynomial optimization (96 open)
- Families: BQP (maxcut/chimera/ising 13, maxcsp 5, pb 8, qap/qapw, qspp 3, color_lab 3, graphpart 1) plus binary quadratic with linear constraints (faclay 9, sonet 7, sporttournament 11, edgecross, mbtd, flay06h) plus autocorr_bern (29; one row with ~3,000–13,000 cubic/quartic monomials) plus hadamard (4; degree 6–8).
- Technique: linearization, multilinear-polytope cuts, SDP (maxcut), symmetry handling. The theory is mature, and the repository already has multilinear work.
- autocorr (low-autocorrelation binary sequences, LABS) is the most distinctive: the objective is `Σ_k C_k^2`, a sum of squared aperiodic autocorrelations with Toeplitz and dihedral symmetry. Gaps are 0.13–6.5 and grow with n. The candidate question is relaxations that exploit the sum-of-squared-correlations/Parseval structure. The count is large, but the application is narrow.

### 2.6 Pooling (single period) and water under design (pooling_spp 24, waterund 10, wastewater 5, digabel 3)
- Pure bilinear `x = q·f` equality (pq-formulation, `EQ:C*C`), bilinear graph max degree 9–19, no binaries. Gaps: spp 0.1%–25%, waterund 0.03%–93%, wastewater 27–43%.
- Prior repository work covers pooling. It is listed for completeness and not ranked.

### 2.7 Nuclear core reload (18 open; gaps inf or ~1e6)
- Structure, verified on nuclearva/14a:
  - Discrete diffusion eigenvalue equations `λ_t φ_i = Σ_j G_ij k_j φ_j` with G ≥ 0 (rows `EQ:Cu*Cu x6..x10`).
  - `k_j = Σ assignment binaries × fuel reactivity` (rows with `B*Cu`).
  - Burnup `k_{j,t+1} = k_{j,t}(1 - α φ_{j,t})`, power peaking `k_j φ_j ≤ c`.
  - The objective maximizes the end-of-cycle λ (`x174`). φ and λ are unbounded.
- Candidate question: **Perron–Frobenius/Collatz–Wielandt cuts.** For nonnegative M(k) = G·diag(k) and a nonnegative eigenvector, `min_i Σ_j G_ij k_j ≤ λ ≤ max_i Σ_j G_ij k_j`, which is linear in k. There are also weighted versions (`λ ≤ max_i (M w)_i / w_i` for any fixed w > 0), and possibly the convex hull of the spectral radius over assignment polytopes.
  - This should turn infinite or 1e6 gaps into finite ones (**hypothesis, not tested**).
  - Touches 18. Generality is moderate: spectral-radius or eigenvalue constraints appear in reactor physics, population models, Markov chains, and structural stability.

### 2.8 Other families (brief)
- **arki (14):**
  - arki0009–0014: CES production functions `(Σ a x^-ρ)^(-1/ρ)` plus a log-utility objective (CGE-like).
  - arki0016/17: Gibbs-type `x ln x` objective with bilinear `x·μ` equalities.
  - Many unbounded variables; 8 have gap inf.
  - Question: hidden convexity (CES is concave for these ρ) and complementarity-type bilinear equalities.
- **Network design with congestion (ndcc 10, telecomsp 3, nd 1):** the ndcc rows `t(c - F) ≥ cF` are hyperbolic, hence rotated-SOC representable, i.e. convex. The perspective variants are also open with similar gaps (0.19–0.92), so the gap is the MIP design part (capacity choice) plus unrecognized hidden cones. Mostly implementation.
- **ML surrogates (11):**
  - ann_*_tanh: tanh equalities; no dual bound listed.
  - kan_*: Kolmogorov–Arnold networks, with binary-selected spline pieces times continuous inputs (`B*C±`, `Cu*C±`) and SiLU `x/(1+e^{-x})`.
  - kriging: `exp(-||x-x_i||)`.
  - Gaps are inf for 8. The main issue is unbounded hidden-layer variables, then weak piecewise-polynomial relaxations. The question is layerwise reachable-set bounds, which is similar to 2.2.
- **multiplants/csched (10):** production = rate × duration / cycle time. There are ratios `(C)/(C)*L` with a common denominator T, plus bilinear `C*Cu`. A Charnes–Cooper homogenization is blocked by binaries.
- **Water (29 = waterno1 8, waterno2 5, waternd 8, water design 8):** `signpower(q, 1.852 or 2)` head loss, `C^2.435` diameter terms, pump polynomials. This is covered by the repository's potential-flow and waterno2 work.
- **Heat exchanger networks (7):** LMTD `ΔT/ln(ΔT1/ΔT2)` and area `Q/(U·LMTD)`, `(Cu)^0.6` cost. Listed gaps are mostly < 1% except heatexch_gen1–3 (9–54%).
- **sfacloc (9):** trilinear `y·a_j·x_j` with x on a simplex (`EQ:C*C*C`). Gaps 0.2–32.

## 3. Ranking of candidate structures

Score = (open instances touched) × (plausibility that better theory gives substantially better bounds) × (importance beyond MINLPLib). The plausibility and generality ratings are judgments.

| rank | structure / question | open touched | plausibility | generality | evidence |
|---|---|---|---|---|---|
| 1 | Discretized dynamics: provable discrete-time state bounds (positivity/conservation/M-matrix/comparison) + relaxations of the k-step map with bilinear control/parameter dependence | ≈45 (51 incl. borderline); 26 have gap inf | high for inf → finite; medium for tight | high (dynamic optimization, kinetic parameter estimation, process control) | SCIP gives no dual bound on catmix100, methanol50, gasoil50; heuristic box gives finite but weak bound |
| 2 | Multi-period blending with inventory and charge/discharge modes: hull of the mode-dependent tank quality recursion, chained over time | ≈28–32 | medium-high | high (refinery/crude scheduling, water and gas storage) | SCIP 120 s: 1/20 mpbp solved, 12/20 without a feasible point, dual/primal 1.2–2.7× on 5, negative incumbents on 2; exclusivity rows confirmed |
| 3 | Point configurations with distance constraints: positive-definite-kernel (Delsarte/Cohn–Elkies-type) aggregation cuts, symmetry-reduced | ≈25–35 | high (verified numerically on knp; isodiametric on polygon) | medium (packing, cutting, layout, sensor/antenna placement, molecular) | polygon gaps drop from 6–42 to ≤0.72% via π/4; knp dual 4.0 → 1.02–1.07 (uncertified LP); two primal improvements via Reinhardt and D5 |
| 4 | AC power flow with switching and trig: on/off QC/SOC hulls and their automatic recognition in generic QCQP form | 49 | low for *new* theory (known relaxations likely close most of the gap, **unverified**); high for implementation | very high (energy) | duals 0 in SCIP 60 s on 5 tested instances |
| 5 | Eigenvalue (Perron) constraints with assignment-dependent nonnegative matrices: Collatz–Wielandt-type cuts and hulls | 18 | high for finite bounds (untested) | medium-low | model structure confirmed on nuclearva/14a |

Not ranked but large:
- Binary polynomial (96): mature theory, low marginal plausibility, except possibly the LABS-specific structure (29).
- Single-period pooling (41): the repository already covers pooling.
- Hidden-convexity/perspective recognition (ndcc, arki CES, trim loss): mostly implementation.

## 4. Things not verified
- Novelty of each candidate question: no literature search was done in this pass.
- AC OPF: that SOC/QC relaxations close these specific gaps is based on literature memory, not recomputed.
- The Delsarte bounds are grid-discretized, not certified. knp4-24's true optimum is unknown to me: the 24-cell gives 1.0, and I believe its optimality as a spherical code is not proven.
- The nuclear Collatz–Wielandt bound was not implemented.
- The catmix box bounds used in the test are heuristic, not proven valid.
- Family semantics for sfacloc, arki, and misc were inferred from structure, not from the source papers.

## 5. Scripts
`/tmp/scout/load.py` (metadata), `osil.py` (parser/analyzer), `runall.py`, `agg.py`, `fam.py` (family map), `show.py`/`rowsof.py` (pretty-printers), `evalosil.py` (feasibility checker), `scip_run.py`, `scip_bounded.py`, `delsarte.py`. Results: `scip60.jsonl`, `scip_mpbp.jsonl`.

## 6. Appendix: all 538 open instances
(gap as listed in MINLPLib; ops = nonlinear operator flags from the metadata, beyond quadratic/multiplication; empty = only polynomial/quadratic)

| name | family | probtype | gap | vars | bin | int | cons | ops |
|---|---|---|---|---|---|---|---|---|
| acopf_case1354pegase_qcqp | AC OPF | QCP | 2.22 | 19236 | 0 | 0 | 21580 |  |
| acopf_case13659pegase_qcqp | AC OPF | QCP | 0.711 | 199281 | 0 | 0 | 191097 |  |
| acopf_case6468rte_qcqp | AC OPF | QCP | 3.03 | 88932 | 0 | 0 | 90966 |  |
| acopf_case6515rte_qcqp | AC OPF | QCP | 4.24 | 89575 | 0 | 0 | 93059 |  |
| acopf_case9241pegase_qcqp | AC OPF | QCP | 2.74 | 145389 | 0 | 0 | 155089 |  |
| acopf_caseactivsg25k_qcqp | AC OPF | QCQP | 0.923 | 328043 | 0 | 0 | 365034 |  |
| acopf_caseactivsg70k_qcqp | AC OPF | QCQP | inf | 900023 | 0 | 0 | 1016476 |  |
| powerflow0009p | AC OPF | NLP | 0.488 | 60 | 0 | 0 | 139 | cos,mul,sin,sqr |
| powerflow0014p | AC OPF | NLP | 0.973 | 118 | 0 | 0 | 277 | cos,mul,sin,sqr |
| powerflow0014r | AC OPF | QCQP | 0.000279 | 118 | 0 | 0 | 197 |  |
| powerflow0030p | AC OPF | NLP | inf | 236 | 0 | 0 | 555 | cos,mul,sin,sqr |
| powerflow0030r | AC OPF | QCQP | 0.00292 | 236 | 0 | 0 | 391 |  |
| powerflow0039p | AC OPF | NLP | 389 | 282 | 0 | 0 | 657 | cos,mul,sin,sqr |
| powerflow0039r | AC OPF | QCQP | 0.0146 | 282 | 0 | 0 | 473 |  |
| powerflow0057p | AC OPF | NLP | inf | 440 | 0 | 0 | 1037 | cos,mul,sin,sqr |
| powerflow0057r | AC OPF | QCQP | inf | 440 | 0 | 0 | 725 |  |
| powerflow0118p | AC OPF | NLP | inf | 1060 | 0 | 0 | 2479 | cos,mul,sin,sqr |
| powerflow0118r | AC OPF | QCQP | 0.802 | 1060 | 0 | 0 | 1763 |  |
| powerflow0300p | AC OPF | NLP | inf | 2370 | 0 | 0 | 5557 | cos,mul,sin,sqr |
| powerflow0300r | AC OPF | QCQP | inf | 2370 | 0 | 0 | 3925 |  |
| powerflow2383wpp | AC OPF | NLP | inf | 16964 | 0 | 0 | 39701 | cos,mul,sin,sqr |
| powerflow2383wpr | AC OPF | QCP | inf | 16964 | 0 | 0 | 28157 |  |
| powerflow2736spp | AC OPF | NLP | 0.392 | 19916 | 0 | 0 | 46821 | cos,mul,sin,sqr |
| powerflow2736spr | AC OPF | QCP | 0.392 | 19916 | 0 | 0 | 32845 |  |
| transswitch0009p | AC OPF + line switching | MBNLP | 0.653 | 69 | 9 | 0 | 139 | cos,mul,sin,sqr |
| transswitch0009r | AC OPF + line switching | MBNLP | 0.0218 | 69 | 9 | 0 | 103 |  |
| transswitch0014p | AC OPF + line switching | MBNLP | inf | 138 | 20 | 0 | 277 | cos,mul,sin,sqr |
| transswitch0014r | AC OPF + line switching | MBNLP | inf | 138 | 20 | 0 | 197 |  |
| transswitch0030p | AC OPF + line switching | MBNLP | inf | 277 | 41 | 0 | 555 | cos,mul,sin,sqr |
| transswitch0030r | AC OPF + line switching | MBNLP | inf | 277 | 41 | 0 | 391 |  |
| transswitch0039p | AC OPF + line switching | MBNLP | 2.09e+04 | 328 | 46 | 0 | 657 | cos,mul,sin,sqr |
| transswitch0039r | AC OPF + line switching | MBNLP | 0.554 | 328 | 46 | 0 | 473 |  |
| transswitch0057p | AC OPF + line switching | MBNLP | inf | 518 | 78 | 0 | 1037 | cos,mul,sin,sqr |
| transswitch0057r | AC OPF + line switching | MBNLP | inf | 518 | 78 | 0 | 725 |  |
| transswitch0118p | AC OPF + line switching | MBNLP | inf | 1239 | 179 | 0 | 2479 | cos,mul,sin,sqr |
| transswitch0118r | AC OPF + line switching | MBNLP | inf | 1239 | 179 | 0 | 1763 |  |
| transswitch0300p | AC OPF + line switching | MBNLP | inf | 2778 | 408 | 0 | 5557 | cos,mul,sin,sqr |
| transswitch0300r | AC OPF + line switching | MBNLP | inf | 2778 | 408 | 0 | 3925 |  |
| transswitch2383wpp | AC OPF + line switching | MBNLP | inf | 19850 | 2886 | 0 | 39701 | cos,mul,sin,sqr |
| transswitch2383wpr | AC OPF + line switching | MBNLP | inf | 19850 | 2886 | 0 | 28157 |  |
| transswitch2736spp | AC OPF + line switching | MBNLP | 0.392 | 23410 | 3494 | 0 | 46821 | cos,mul,sin,sqr |
| transswitch2736spr | AC OPF + line switching | MBNLP | 0.392 | 23410 | 3494 | 0 | 32845 |  |
| chimera_lga-02 | BQP / binary polynomial | BQP | 0.00823 | 964 | 964 | 0 | 0 |  |
| chimera_mgw-c16-2031-01 | BQP / binary polynomial | BQP | 0.0763 | 2032 | 2032 | 0 | 0 |  |
| chimera_mgw-c16-2031-02 | BQP / binary polynomial | BQP | 0.0818 | 2032 | 2032 | 0 | 0 |  |
| chimera_mgw-c8-507-onc8-01 | BQP / binary polynomial | BQP | 0.03 | 508 | 508 | 0 | 0 |  |
| chimera_mgw-c8-507-onc8-02 | BQP / binary polynomial | BQP | 0.0247 | 508 | 508 | 0 | 0 |  |
| chimera_rfr-01 | BQP / binary polynomial | BQP | 0.034 | 2032 | 2032 | 0 | 0 |  |
| chimera_rfr-02 | BQP / binary polynomial | BQP | 0.0308 | 2032 | 2032 | 0 | 0 |  |
| chimera_selby-c16-01 | BQP / binary polynomial | BQP | 0.0725 | 2031 | 2031 | 0 | 0 |  |
| chimera_selby-c16-02 | BQP / binary polynomial | BQP | 0.079 | 2031 | 2031 | 0 | 0 |  |
| chimera_selby-c8-onc8-01 | BQP / binary polynomial | BQP | 0.0263 | 507 | 507 | 0 | 0 |  |
| chimera_selby-c8-onc8-02 | BQP / binary polynomial | BQP | 0.02 | 507 | 507 | 0 | 0 |  |
| color_lab2_4x0 | BQP / binary polynomial | BQP | 0.223 | 300 | 300 | 0 | 61 |  |
| color_lab3_4x0 | BQP / binary polynomial | BQP | 0.158 | 395 | 395 | 0 | 80 |  |
| color_lab6b_4x20 | BQP / binary polynomial | BQP | inf | 235 | 235 | 0 | 48 |  |
| graphpart_clique-70 | BQP / binary polynomial | BQP | 0.289 | 210 | 210 | 0 | 70 |  |
| ising2_5-300_5555 | BQP / binary polynomial | BQP | 0.00894 | 300 | 300 | 0 | 0 |  |
| maxcsp-ehi-85-297-12 | BQP / binary polynomial | BQP | 5.43 | 2071 | 2071 | 0 | 297 |  |
| maxcsp-ehi-85-297-36 | BQP / binary polynomial | BQP | 2.48 | 2046 | 2046 | 0 | 297 |  |
| maxcsp-ehi-85-297-71 | BQP / binary polynomial | BQP | 8 | 2075 | 2075 | 0 | 297 |  |
| maxcsp-ehi-90-315-70 | BQP / binary polynomial | BQP | 8 | 2203 | 2203 | 0 | 315 |  |
| maxcsp-langford-3-11 | BQP / binary polynomial | BQP | inf | 627 | 627 | 0 | 33 |  |
| pb302035 | BQP / binary polynomial | BQP | 0.625 | 600 | 600 | 0 | 50 |  |
| pb302055 | BQP / binary polynomial | BQP | 1.03 | 600 | 600 | 0 | 50 |  |
| pb302075 | BQP / binary polynomial | BQP | 0.857 | 600 | 600 | 0 | 50 |  |
| pb302095 | BQP / binary polynomial | BQP | 0.359 | 600 | 600 | 0 | 50 |  |
| pb351535 | BQP / binary polynomial | BQP | 0.711 | 525 | 525 | 0 | 50 |  |
| pb351555 | BQP / binary polynomial | BQP | 0.698 | 525 | 525 | 0 | 50 |  |
| pb351575 | BQP / binary polynomial | BQP | 2.06 | 525 | 525 | 0 | 50 |  |
| pb351595 | BQP / binary polynomial | BQP | 1.39 | 525 | 525 | 0 | 50 |  |
| qap | BQP / binary polynomial | BQP | 1.6 | 225 | 225 | 0 | 30 |  |
| qapw | BQP / binary polynomial | MBQP | 0.46 | 450 | 225 | 0 | 255 |  |
| qspp_0_13_0_1_10_1 | BQP / binary polynomial | BQP | 0.0893 | 312 | 312 | 0 | 169 |  |
| qspp_0_14_0_1_10_1 | BQP / binary polynomial | BQP | 0.306 | 364 | 364 | 0 | 196 |  |
| qspp_0_15_0_1_10_1 | BQP / binary polynomial | BQP | 0.658 | 420 | 420 | 0 | 225 |  |
| chp_partload | CHP / power plant operation | MBNLP | 0.134 | 2248 | 45 | 0 | 2516 | div,log,mul,sqr,vcpower |
| chp_shorttermplan1b | CHP / power plant operation | MBNLP | 0.00619 | 1680 | 288 | 0 | 3850 |  |
| chp_shorttermplan2c | CHP / power plant operation | MBNLP | inf | 2448 | 384 | 0 | 6734 |  |
| chp_shorttermplan2d | CHP / power plant operation | MBNLP | 0.0288 | 3120 | 528 | 0 | 6838 |  |
| super3t | CHP / power plant operation | MBNLP | 0.458 | 1056 | 44 | 0 | 1343 | div,log,mul,power,sqr |
| ex5_3_3 | GlobalLib ex* | QCQP | 0.308 | 62 | 0 | 0 | 53 |  |
| ex6_2_11 | GlobalLib ex* | NLP | 0.785 | 3 | 0 | 0 | 1 | div,log,mul |
| ex6_2_13 | GlobalLib ex* | NLP | 0.00308 | 6 | 0 | 0 | 3 | div,log,mul |
| ex6_2_5 | GlobalLib ex* | NLP | 4.15 | 9 | 0 | 0 | 3 | div,log,mul |
| ex6_2_6 | GlobalLib ex* | NLP | 0.344 | 3 | 0 | 0 | 1 | log,mul |
| ex6_2_7 | GlobalLib ex* | NLP | 7.42 | 9 | 0 | 0 | 3 | log,mul |
| ex7_3_5 | GlobalLib ex* | NLP | 0.000181 | 13 | 0 | 0 | 15 |  |
| ex8_1_3 | GlobalLib ex* | NLP | inf | 2 | 0 | 0 | 0 |  |
| ex8_1_4 | GlobalLib ex* | NLP | inf | 2 | 0 | 0 | 0 |  |
| ex8_1_5 | GlobalLib ex* | NLP | inf | 2 | 0 | 0 | 0 |  |
| ex8_3_13 | GlobalLib ex* | NLP | 0.159 | 115 | 0 | 0 | 72 | div,exp,mul,vcpower |
| ex8_3_2 | GlobalLib ex* | QCP | 0.407 | 110 | 0 | 0 | 76 |  |
| ex8_3_3 | GlobalLib ex* | QCP | 0.392 | 110 | 0 | 0 | 76 |  |
| ex8_3_4 | GlobalLib ex* | QCP | 0.62 | 110 | 0 | 0 | 76 |  |
| ex8_3_5 | GlobalLib ex* | QCP | 13.5 | 110 | 0 | 0 | 76 |  |
| ex8_3_7 | GlobalLib ex* | NLP | 30.6 | 126 | 0 | 0 | 92 |  |
| ex8_3_8 | GlobalLib ex* | QCP | 0.751 | 126 | 0 | 0 | 93 |  |
| ex8_3_9 | GlobalLib ex* | QCP | 0.311 | 78 | 0 | 0 | 45 |  |
| ex8_4_2 | GlobalLib ex* | NLP | 0.0797 | 24 | 0 | 0 | 10 |  |
| ex8_4_6 | GlobalLib ex* | NLP | 0.00376 | 14 | 0 | 0 | 8 | exp,mul |
| ex8_4_7 | GlobalLib ex* | NLP | 0.0117 | 62 | 0 | 0 | 40 | div,exp,mul |
| ex8_5_1 | GlobalLib ex* | NLP | 12.9 | 6 | 0 | 0 | 4 | div,log,mul |
| ex8_5_2 | GlobalLib ex* | NLP | 1.62e+03 | 6 | 0 | 0 | 4 | div,log,mul |
| ex8_5_4 | GlobalLib ex* | NLP | 0.00209 | 5 | 0 | 0 | 4 | div,log,mul |
| ex8_5_6 | GlobalLib ex* | NLP | 0.0026 | 6 | 0 | 0 | 4 | div,log,mul |
| ex8_6_1 | GlobalLib ex* | NLP | inf | 75 | 0 | 0 | 45 | div,sqr |
| ex8_6_2 | GlobalLib ex* | NLP | 0.411 | 30 | 0 | 0 | 0 | exp,sqr,vcpower |
| ann_compressor_tanh | ML surrogate | NLP | inf | 96 | 0 | 0 | 95 | tanh |
| ann_cumene_tanh | ML surrogate | NLP | inf | 794 | 0 | 0 | 790 | tanh |
| ann_fermentation_tanh | ML surrogate | NLP | inf | 12 | 0 | 0 | 9 | tanh |
| ann_peaks_tanh | ML surrogate | NLP | inf | 100 | 0 | 0 | 98 | tanh |
| kan_r3_h1_n4 | ML surrogate | MBNLP | inf | 1129 | 288 | 0 | 1478 | div,exp |
| kan_r3_h1_n5 | ML surrogate | MBNLP | 2.46e+03 | 1410 | 360 | 0 | 1847 | div,exp |
| kan_r3_h1_n9 | ML surrogate | MBNLP | inf | 2534 | 648 | 0 | 3323 | div,exp |
| kan_r5_h1_n3 | ML surrogate | MBNLP | 19.9 | 838 | 216 | 0 | 1121 | div,exp |
| kan_r5_h1_n5 | ML surrogate | MBNLP | inf | 1392 | 360 | 0 | 1867 | div,exp |
| kan_r5_h1_n8 | ML surrogate | MBNLP | inf | 2223 | 576 | 0 | 2986 | div,exp |
| kriging_peaks-full500 | ML surrogate | NLP | 0.755 | 1006 | 0 | 0 | 1004 | exp,mul,sqrt |
| arki0002 | arki | NLP | inf | 2456 | 0 | 0 | 1976 | div,exp |
| arki0004 | arki | NLP | inf | 2090 | 0 | 0 | 2081 | div,log,sqr |
| arki0006 | arki | NLP | 1.26 | 2370 | 0 | 0 | 5152 |  |
| arki0009 | arki | NLP | 32.4 | 7714 | 0 | 0 | 6707 | log,mul,vcpower |
| arki0010 | arki | NLP | 35.8 | 4144 | 0 | 0 | 3427 | log,mul,vcpower |
| arki0011 | arki | NLP | inf | 19314 | 0 | 0 | 17737 | log,mul,vcpower |
| arki0012 | arki | NLP | inf | 19314 | 0 | 0 | 17737 | log,mul,vcpower |
| arki0013 | arki | NLP | inf | 19314 | 0 | 0 | 17737 | log,mul,vcpower |
| arki0014 | arki | NLP | inf | 19305 | 0 | 0 | 17692 | log,mul,vcpower |
| arki0015 | arki | NLP | 0.0266 | 2093 | 0 | 0 | 1496 | div,exp,mul,vcpower |
| arki0016 | arki | NLP | inf | 5047 | 0 | 0 | 2946 | log,mul |
| arki0017 | arki | NLP | 12.2 | 4332 | 0 | 0 | 2572 | log,mul |
| arki0018 | arki | NLP | inf | 9804 | 0 | 0 | 9 | log,mul |
| arki0021 | arki | NLP | 0.558 | 3187 | 0 | 0 | 2 | div,log,mul |
| autocorr_bern30-15 | autocorr_bern | MBNLP | 0.129 | 31 | 30 | 0 | 1 |  |
| autocorr_bern30-23 | autocorr_bern | MBNLP | 0.535 | 31 | 30 | 0 | 1 |  |
| autocorr_bern30-30 | autocorr_bern | MBNLP | 0.625 | 31 | 30 | 0 | 1 |  |
| autocorr_bern35-18 | autocorr_bern | MBNLP | 0.17 | 36 | 35 | 0 | 1 |  |
| autocorr_bern35-26 | autocorr_bern | MBNLP | 0.506 | 36 | 35 | 0 | 1 |  |
| autocorr_bern35-35fix | autocorr_bern | MBNLP | 3.47 | 36 | 35 | 0 | 1 |  |
| autocorr_bern40-10 | autocorr_bern | MBNLP | 0.133 | 41 | 40 | 0 | 1 |  |
| autocorr_bern40-20 | autocorr_bern | MBNLP | 0.383 | 41 | 40 | 0 | 1 |  |
| autocorr_bern40-30 | autocorr_bern | MBNLP | 1.35 | 41 | 40 | 0 | 1 |  |
| autocorr_bern40-40 | autocorr_bern | MBNLP | 2.14 | 41 | 40 | 0 | 1 |  |
| autocorr_bern45-11 | autocorr_bern | MBNLP | 0.345 | 46 | 45 | 0 | 1 |  |
| autocorr_bern45-23 | autocorr_bern | MBNLP | 1.17 | 46 | 45 | 0 | 1 |  |
| autocorr_bern45-34 | autocorr_bern | MBNLP | 2.65 | 46 | 45 | 0 | 1 |  |
| autocorr_bern45-45 | autocorr_bern | MBNLP | 3.42 | 46 | 45 | 0 | 1 |  |
| autocorr_bern50-06 | autocorr_bern | MBNLP | 0.185 | 51 | 50 | 0 | 1 |  |
| autocorr_bern50-13 | autocorr_bern | MBNLP | 0.724 | 51 | 50 | 0 | 1 |  |
| autocorr_bern50-25 | autocorr_bern | MBNLP | 2.32 | 51 | 50 | 0 | 1 |  |
| autocorr_bern50-38 | autocorr_bern | MBNLP | 4.21 | 51 | 50 | 0 | 1 |  |
| autocorr_bern50-50 | autocorr_bern | MBNLP | 4.53 | 51 | 50 | 0 | 1 |  |
| autocorr_bern55-06 | autocorr_bern | MBNLP | 0.372 | 56 | 55 | 0 | 1 |  |
| autocorr_bern55-14 | autocorr_bern | MBNLP | 0.932 | 56 | 55 | 0 | 1 |  |
| autocorr_bern55-28 | autocorr_bern | MBNLP | 2.66 | 56 | 55 | 0 | 1 |  |
| autocorr_bern55-41 | autocorr_bern | MBNLP | 4.71 | 56 | 55 | 0 | 1 |  |
| autocorr_bern55-55 | autocorr_bern | MBNLP | 5.51 | 56 | 55 | 0 | 1 |  |
| autocorr_bern60-08 | autocorr_bern | MBNLP | 0.539 | 61 | 60 | 0 | 1 |  |
| autocorr_bern60-15 | autocorr_bern | MBNLP | 1.47 | 61 | 60 | 0 | 1 |  |
| autocorr_bern60-30 | autocorr_bern | MBNLP | 3.08 | 61 | 60 | 0 | 1 |  |
| autocorr_bern60-45 | autocorr_bern | MBNLP | 5.52 | 61 | 60 | 0 | 1 |  |
| autocorr_bern60-60 | autocorr_bern | MBNLP | 6.49 | 61 | 60 | 0 | 1 |  |
| edgecross24-115 | binary quadratic w/ linear constraints | MBQCP | 0.0309 | 553 | 552 | 0 | 8097 |  |
| faclay30 | binary quadratic w/ linear constraints | MBQCP | 0.0534 | 436 | 435 | 0 | 8121 |  |
| faclay30h | binary quadratic w/ linear constraints | MBQCP | 0.24 | 436 | 435 | 0 | 8121 |  |
| faclay33 | binary quadratic w/ linear constraints | MBQCP | 0.258 | 529 | 528 | 0 | 10913 |  |
| faclay35 | binary quadratic w/ linear constraints | MBQCP | 0.289 | 596 | 595 | 0 | 13091 |  |
| faclay60 | binary quadratic w/ linear constraints | MBQCP | 2.16 | 1771 | 1770 | 0 | 68441 |  |
| faclay70 | binary quadratic w/ linear constraints | MBQCP | 10.8 | 2416 | 2415 | 0 | 109481 |  |
| faclay75 | binary quadratic w/ linear constraints | MBQCP | 11.9 | 2776 | 2775 | 0 | 135051 |  |
| faclay80 | binary quadratic w/ linear constraints | MBQCP | 12.4 | 3161 | 3160 | 0 | 164321 |  |
| flay06h | binary quadratic w/ linear constraints | MBNLP | 0.0314 | 566 | 60 | 0 | 693 |  |
| mbtd | binary quadratic w/ linear constraints | MBNLP | 0.327 | 210 | 200 | 0 | 70 |  |
| sonet22v4 | binary quadratic w/ linear constraints | BQCP | 0.0272 | 231 | 231 | 0 | 4642 |  |
| sonet22v5 | binary quadratic w/ linear constraints | BQCQP | 0.715 | 252 | 252 | 0 | 252 |  |
| sonet23v4 | binary quadratic w/ linear constraints | BQCQP | 0.245 | 275 | 275 | 0 | 275 |  |
| sonet23v6 | binary quadratic w/ linear constraints | BQCP | 0.109 | 253 | 253 | 0 | 5336 |  |
| sonet24v5 | binary quadratic w/ linear constraints | BQCQP | 0.713 | 299 | 299 | 0 | 299 |  |
| sonet25v5 | binary quadratic w/ linear constraints | BQCP | 0.0723 | 300 | 300 | 0 | 6925 |  |
| sonet25v6 | binary quadratic w/ linear constraints | BQCQP | 1.44 | 324 | 324 | 0 | 324 |  |
| sporttournament30 | binary quadratic w/ linear constraints | MBQCP | 0.00722 | 436 | 435 | 0 | 1 |  |
| sporttournament32 | binary quadratic w/ linear constraints | MBQCP | 0.0126 | 497 | 496 | 0 | 1 |  |
| sporttournament34 | binary quadratic w/ linear constraints | MBQCP | 0.0162 | 562 | 561 | 0 | 1 |  |
| sporttournament36 | binary quadratic w/ linear constraints | MBQCP | 0.0159 | 631 | 630 | 0 | 1 |  |
| sporttournament38 | binary quadratic w/ linear constraints | MBQCP | 0.025 | 704 | 703 | 0 | 1 |  |
| sporttournament40 | binary quadratic w/ linear constraints | MBQCP | 0.039 | 781 | 780 | 0 | 1 |  |
| sporttournament42 | binary quadratic w/ linear constraints | MBQCP | 0.0335 | 862 | 861 | 0 | 1 |  |
| sporttournament44 | binary quadratic w/ linear constraints | MBQCP | 0.0372 | 947 | 946 | 0 | 1 |  |
| sporttournament46 | binary quadratic w/ linear constraints | MBQCP | 0.0357 | 1036 | 1035 | 0 | 1 |  |
| sporttournament48 | binary quadratic w/ linear constraints | MBQCP | 0.0402 | 1129 | 1128 | 0 | 1 |  |
| sporttournament50 | binary quadratic w/ linear constraints | MBQCP | 0.0432 | 1226 | 1225 | 0 | 1 |  |
| crudeoil_li01 | crude oil scheduling | MBQCP | 0.00268 | 344 | 48 | 0 | 695 |  |
| crudeoil_li02 | crude oil scheduling | MBQCP | 0.000536 | 1297 | 240 | 0 | 5004 |  |
| crudeoil_li03 | crude oil scheduling | MBQCP | 0.0116 | 964 | 132 | 0 | 2442 |  |
| crudeoil_li05 | crude oil scheduling | MBQCP | 0.037 | 940 | 132 | 0 | 1916 |  |
| crudeoil_li11 | crude oil scheduling | MBQCP | 0.00489 | 1177 | 180 | 0 | 3505 |  |
| crudeoil_li21 | crude oil scheduling | MBQCP | 0.0111 | 1348 | 216 | 0 | 4681 |  |
| camshape100 | discretized optimal control | QCP | 0.0445 | 199 | 0 | 0 | 200 |  |
| camshape200 | discretized optimal control | QCP | 0.129 | 399 | 0 | 0 | 400 |  |
| camshape400 | discretized optimal control | QCP | 0.172 | 799 | 0 | 0 | 800 |  |
| camshape800 | discretized optimal control | QCP | 0.204 | 1599 | 0 | 0 | 1600 |  |
| catmix100 | discretized optimal control | QCP | inf | 303 | 0 | 0 | 200 |  |
| catmix200 | discretized optimal control | QCP | inf | 603 | 0 | 0 | 400 |  |
| catmix400 | discretized optimal control | QCP | inf | 1203 | 0 | 0 | 800 |  |
| catmix800 | discretized optimal control | QCP | inf | 2403 | 0 | 0 | 1600 |  |
| chain100 | discretized optimal control | NLP | inf | 202 | 0 | 0 | 101 | mul,sqr,sqrt |
| chain200 | discretized optimal control | NLP | inf | 402 | 0 | 0 | 201 | mul,sqr,sqrt |
| chain400 | discretized optimal control | NLP | inf | 802 | 0 | 0 | 401 | mul,sqr,sqrt |
| chain50 | discretized optimal control | NLP | inf | 102 | 0 | 0 | 51 | mul,sqr,sqrt |
| cont6-qq | discretized optimal control | QCQP | inf | 79998 | 0 | 0 | 40397 |  |
| dtoc5 | discretized optimal control | QCQP | 8.59e+03 | 99999 | 0 | 0 | 49999 |  |
| gasoil100 | discretized optimal control | NLP | 8.15e+05 | 2603 | 0 | 0 | 2598 |  |
| gasoil200 | discretized optimal control | NLP | 8.15e+05 | 5203 | 0 | 0 | 5198 |  |
| gasoil400 | discretized optimal control | NLP | 8.15e+05 | 10403 | 0 | 0 | 10398 |  |
| gasoil50 | discretized optimal control | NLP | inf | 1303 | 0 | 0 | 1298 |  |
| glider100 | discretized optimal control | NLP | inf | 1315 | 0 | 0 | 1209 | exp,mul,sqr,sqrt |
| glider200 | discretized optimal control | NLP | inf | 2615 | 0 | 0 | 2409 | exp,mul,sqr,sqrt |
| glider400 | discretized optimal control | NLP | inf | 5215 | 0 | 0 | 4809 | exp,mul,sqr,sqrt |
| glider50 | discretized optimal control | NLP | 3.54e+05 | 665 | 0 | 0 | 609 | exp,mul,sqr,sqrt |
| hvycrash | discretized optimal control | NLP | inf | 201 | 0 | 0 | 150 | cos,div,mul |
| junkturn | discretized optimal control | QCQP | inf | 200008 | 0 | 0 | 140000 |  |
| lnts100 | discretized optimal control | NLP | 0.0896 | 506 | 0 | 0 | 400 | cos,mul,sin |
| lnts200 | discretized optimal control | NLP | 0.0972 | 1006 | 0 | 0 | 800 | cos,mul,sin |
| lnts400 | discretized optimal control | NLP | 0.106 | 2006 | 0 | 0 | 1600 | cos,mul,sin |
| lnts50 | discretized optimal control | NLP | 0.0548 | 256 | 0 | 0 | 200 | cos,mul,sin |
| lukvle10 | discretized optimal control | NLP | 6.93e+03 | 1000 | 0 | 0 | 998 | rpower,sqr |
| methanol100 | discretized optimal control | NLP | inf | 3005 | 0 | 0 | 2997 | div,mul |
| methanol200 | discretized optimal control | NLP | inf | 6005 | 0 | 0 | 5997 | div,mul |
| methanol400 | discretized optimal control | NLP | inf | 12005 | 0 | 0 | 11997 | div,mul |
| methanol50 | discretized optimal control | NLP | inf | 1505 | 0 | 0 | 1497 | div,mul |
| optcdeg2 | discretized optimal control | QCQP | 65.8 | 150002 | 0 | 0 | 100000 |  |
| parabol5_2_2 | discretized optimal control | QCP | inf | 40401 | 0 | 0 | 40201 |  |
| parabol5_2_3 | discretized optimal control | QCP | inf | 40401 | 0 | 0 | 40201 |  |
| parabol5_2_4 | discretized optimal control | QCP | 8.42e+03 | 40401 | 0 | 0 | 40201 |  |
| parabol_p | discretized optimal control | QCP | inf | 12097 | 0 | 0 | 11906 |  |
| pinene100 | discretized optimal control | QCQP | 472 | 5005 | 0 | 0 | 4995 |  |
| pinene200 | discretized optimal control | QCQP | 472 | 10005 | 0 | 0 | 9995 |  |
| pinene50 | discretized optimal control | QCQP | 472 | 2505 | 0 | 0 | 2495 |  |
| popdynm100 | discretized optimal control | QCQP | inf | 5615 | 0 | 0 | 5592 |  |
| popdynm200 | discretized optimal control | QCQP | inf | 11215 | 0 | 0 | 11192 |  |
| popdynm25 | discretized optimal control | QCQP | 5.56e+12 | 1415 | 0 | 0 | 1392 |  |
| popdynm50 | discretized optimal control | QCQP | inf | 2815 | 0 | 0 | 2792 |  |
| rocket100 | discretized optimal control | NLP | 0.014 | 607 | 0 | 0 | 502 | exp,mul,sqr |
| rocket200 | discretized optimal control | NLP | 0.0597 | 1207 | 0 | 0 | 1002 | exp,mul,sqr |
| rocket400 | discretized optimal control | NLP | 8.18 | 2407 | 0 | 0 | 2002 | exp,mul,sqr |
| rocket50 | discretized optimal control | NLP | 0.0156 | 307 | 0 | 0 | 252 | exp,mul,sqr |
| trainf | discretized optimal control | QCQP | inf | 40000 | 0 | 0 | 20002 |  |
| truck | discretized optimal control | NLP | 1.26 | 5007 | 0 | 0 | 4009 | cos,mul,sin |
| deb10 | generation with trig | MBNLP | inf | 182 | 22 | 0 | 129 | cos,mul,sin |
| deb6 | generation with trig | MBNLP | inf | 475 | 20 | 0 | 507 | cos,mul,sin,sqr,sqrt |
| deb7 | generation with trig | MBNLP | inf | 813 | 20 | 0 | 897 | cos,mul,sin,sqr,sqrt |
| deb8 | generation with trig | MBNLP | inf | 823 | 20 | 0 | 897 | cos,mul,sin,sqr,sqrt |
| deb9 | generation with trig | MBNLP | inf | 813 | 20 | 0 | 917 | cos,mul,sin,sqr,sqrt |
| var_con10 | generation with trig | MBNLP | inf | 573 | 12 | 0 | 464 | cos,mul,sin |
| var_con5 | generation with trig | MBNLP | inf | 573 | 12 | 0 | 464 | cos,mul,sin |
| ball_mk4_15 | geometry / packing / distance | IQCP | inf | 30 | 0 | 30 | 1 |  |
| elec100 | geometry / packing / distance | NLP | 2.11 | 300 | 0 | 0 | 100 | div,sqr,sqrt |
| elec200 | geometry / packing / distance | NLP | 2.21 | 600 | 0 | 0 | 200 | div,sqr,sqrt |
| elec25 | geometry / packing / distance | NLP | 1.7 | 75 | 0 | 0 | 25 | div,sqr,sqrt |
| elec50 | geometry / packing / distance | NLP | 1.94 | 150 | 0 | 0 | 50 | div,sqr,sqrt |
| eq6_1 | geometry / packing / distance | NLP | 2.45 | 16 | 0 | 0 | 60 | sqr,sqrt |
| gabriel05 | geometry / packing / distance | MBQCP | inf | 775 | 256 | 0 | 1795 |  |
| gabriel06 | geometry / packing / distance | MBQCP | inf | 2204 | 692 | 0 | 5080 |  |
| gabriel07 | geometry / packing / distance | MBQCP | inf | 2323 | 672 | 0 | 5675 |  |
| gabriel08 | geometry / packing / distance | MBQCP | inf | 5788 | 1964 | 0 | 22168 |  |
| gabriel09 | geometry / packing / distance | MBQCP | 0.151 | 1868 | 756 | 0 | 10088 |  |
| gabriel10 | geometry / packing / distance | MBQCP | 0.011 | 16476 | 6428 | 0 | 115600 |  |
| kall_circles_c6c | geometry / packing / distance | QCP | 0.581 | 20 | 0 | 0 | 63 |  |
| kall_circlespolygons_c1p5a | geometry / packing / distance | QCP | inf | 158 | 0 | 0 | 174 |  |
| kall_circlespolygons_c1p5b | geometry / packing / distance | QCP | inf | 791 | 0 | 0 | 816 |  |
| kall_circlespolygons_c1p6a | geometry / packing / distance | QCP | inf | 1110 | 0 | 0 | 1134 |  |
| kall_circlesrectangles_c6r1 | geometry / packing / distance | QCP | 0.633 | 184 | 0 | 0 | 192 |  |
| kall_circlesrectangles_c6r29 | geometry / packing / distance | QCP | inf | 390 | 0 | 0 | 388 |  |
| kall_circlesrectangles_c6r39 | geometry / packing / distance | QCP | inf | 634 | 0 | 0 | 619 |  |
| kall_ellipsoids_tc02b | geometry / packing / distance | NLP | 0.44 | 124 | 0 | 0 | 128 | mul,sqr,sqrt |
| kall_ellipsoids_tc03c | geometry / packing / distance | NLP | 0.921 | 193 | 0 | 0 | 196 | mul,sqr,sqrt |
| kall_ellipsoids_tc05a | geometry / packing / distance | NLP | 0.877 | 464 | 0 | 0 | 461 |  |
| knp3-12 | geometry / packing / distance | QCP | 1.06 | 37 | 0 | 0 | 78 |  |
| knp4-24 | geometry / packing / distance | QCP | 2.68 | 97 | 0 | 0 | 300 |  |
| knp5-40 | geometry / packing / distance | QCP | 3.06 | 201 | 0 | 0 | 820 |  |
| knp5-41 | geometry / packing / distance | QCP | 3.13 | 206 | 0 | 0 | 861 |  |
| knp5-42 | geometry / packing / distance | QCP | 3.17 | 211 | 0 | 0 | 903 |  |
| knp5-43 | geometry / packing / distance | QCP | 3.22 | 216 | 0 | 0 | 946 |  |
| knp5-44 | geometry / packing / distance | QCP | 3.23 | 221 | 0 | 0 | 990 |  |
| maxmin | geometry / packing / distance | NLP | 1.23 | 27 | 0 | 0 | 78 | sqr,sqrt |
| ngone | geometry / packing / distance | QCQP | 21.7 | 200 | 0 | 0 | 5048 |  |
| orth_d3m6_pl | geometry / packing / distance | NLP | 2.57 | 42 | 0 | 0 | 127 |  |
| orth_d4m6_pl | geometry / packing / distance | NLP | 1.03 | 42 | 0 | 0 | 86 |  |
| p_ball_30b_10p_2d_h | geometry / packing / distance | MBNLP | inf | 1010 | 300 | 0 | 1149 | div,mul,sqr |
| p_ball_30b_10p_2d_m | geometry / packing / distance | MBQCP | 1.15 | 410 | 300 | 0 | 529 |  |
| pointpack10 | geometry / packing / distance | QCP | 0.218 | 21 | 0 | 0 | 55 |  |
| pointpack12 | geometry / packing / distance | QCP | 0.501 | 25 | 0 | 0 | 78 |  |
| pointpack14 | geometry / packing / distance | QCP | 0.843 | 29 | 0 | 0 | 105 |  |
| polygon100 | geometry / packing / distance | NLP | 42.3 | 200 | 0 | 0 | 5049 | cos,mul,sin,sqr |
| polygon25 | geometry / packing / distance | NLP | 6.44 | 50 | 0 | 0 | 324 | cos,mul,sin,sqr |
| polygon50 | geometry / packing / distance | NLP | 18.5 | 100 | 0 | 0 | 1274 | cos,mul,sin,sqr |
| polygon75 | geometry / packing / distance | NLP | 30.7 | 150 | 0 | 0 | 2849 | cos,mul,sin,sqr |
| ringpack_10_1 | geometry / packing / distance | MBQCP | 0.0395 | 70 | 50 | 0 | 385 |  |
| ringpack_10_2 | geometry / packing / distance | MBQCP | 0.0395 | 80 | 60 | 0 | 475 |  |
| ringpack_20_1 | geometry / packing / distance | MBQCP | 0.0604 | 215 | 175 | 0 | 2547 |  |
| ringpack_20_2 | geometry / packing / distance | MBQCP | 0.0604 | 235 | 195 | 0 | 2927 |  |
| ringpack_20_3 | geometry / packing / distance | MBQCP | 0.0395 | 253 | 213 | 0 | 3228 |  |
| ringpack_30_1 | geometry / packing / distance | MBQCP | 0.109 | 433 | 373 | 0 | 7898 |  |
| ringpack_30_2 | geometry / packing / distance | MBQCP | 0.0533 | 463 | 403 | 0 | 8768 |  |
| shiporig | geometry / packing / distance | NLP | inf | 10 | 0 | 0 | 17 | mul,sqrt |
| space25 | geometry / packing / distance | MBQCP | 2.98 | 893 | 750 | 0 | 235 |  |
| space25a | geometry / packing / distance | MBQCP | 2.4 | 383 | 240 | 0 | 201 |  |
| space960 | geometry / packing / distance | MIQCP | 0.262 | 5537 | 0 | 960 | 6497 |  |
| tspn08 | geometry / packing / distance | MBNLP | 0.0065 | 44 | 28 | 0 | 18 | mul,sqr,sqrt |
| tspn10 | geometry / packing / distance | MBNLP | 0.0118 | 65 | 45 | 0 | 21 | mul,sqr,sqrt |
| tspn12 | geometry / packing / distance | MBNLP | 0.0295 | 90 | 66 | 0 | 26 | mul,sqr,sqrt |
| tspn15 | geometry / packing / distance | MBNLP | 0.0414 | 135 | 105 | 0 | 34 | mul,sqr,sqrt |
| hadamard_6 | hadamard | MBNLP | 1.78 | 37 | 36 | 0 | 1 |  |
| hadamard_7 | hadamard | MBNLP | 21.5 | 50 | 49 | 0 | 1 |  |
| hadamard_8 | hadamard | MBNLP | 254 | 65 | 64 | 0 | 1 |  |
| hadamard_9 | hadamard | MBNLP | inf | 82 | 81 | 0 | 1 |  |
| ex1233 | heat exchanger networks | MBNLP | 0.000266 | 52 | 12 | 0 | 64 | div,mul,vcpower |
| heatexch_gen1 | heat exchanger networks | MBNLP | 0.54 | 112 | 12 | 0 | 120 | div,log |
| heatexch_gen2 | heat exchanger networks | MBNLP | 0.0888 | 148 | 16 | 0 | 166 | div,log,vcpower |
| heatexch_gen3 | heat exchanger networks | MBNLP | 0.158 | 580 | 60 | 0 | 510 | div,log,vcpower |
| heatexch_spec1 | heat exchanger networks | MBNLP | 0.000274 | 56 | 12 | 0 | 64 | div,mul,vcpower |
| heatexch_spec3 | heat exchanger networks | MBNLP | 0.00859 | 260 | 60 | 0 | 250 | div,mul,vcpower |
| synheat | heat exchanger networks | MBNLP | 0.000233 | 56 | 12 | 0 | 64 | div,mul,vcpower |
| 4stufen | misc | MBNLP | 0.0326 | 149 | 48 | 0 | 98 | div,log |
| bayes2_20 | misc | QCP | inf | 86 | 0 | 0 | 77 |  |
| bayes2_30 | misc | QCP | inf | 86 | 0 | 0 | 77 |  |
| beuster | misc | MBNLP | 0.106 | 157 | 52 | 0 | 114 | div,log |
| btest14 | misc | NLP | 0.0256 | 135 | 0 | 0 | 93 | exp |
| case_1scv2 | misc | MBNLP | 7.74 | 1556 | 50 | 0 | 1265 |  |
| cesam2cent | misc | NLP | inf | 316 | 0 | 0 | 165 | centropy,exp |
| cesam2log | misc | NLP | inf | 316 | 0 | 0 | 165 | exp,log,mul |
| contvar | misc | MBNLP | 0.444 | 296 | 88 | 0 | 284 | cvpower,div,exp,log,mul,sqr |
| densitymod | misc | MBNLP | inf | 23529 | 23424 | 0 | 550 | abs |
| dosemin2d | misc | MBNLP | inf | 165 | 32 | 0 | 118 | errorf,mul,sqr,sqrt |
| dosemin3d | misc | MBNLP | inf | 1046 | 18 | 0 | 1002 | errorf,mul,sqr,sqrt |
| eg_all_s | misc | MINLP | inf | 8 | 0 | 7 | 28 | exp,mul,sqr |
| eg_disc2_s | misc | MINLP | inf | 8 | 0 | 3 | 28 | exp,mul,sqr |
| eg_disc_s | misc | MINLP | inf | 8 | 0 | 4 | 28 | exp,mul,sqr |
| eg_int_s | misc | MINLP | inf | 8 | 0 | 3 | 28 | exp,mul,sqr |
| etamac | misc | NLP | 0.0722 | 97 | 0 | 0 | 70 | log,mul,vcpower |
| fct | misc | NLP | inf | 11 | 0 | 0 | 9 | abs,mod,sin |
| feedtray | misc | MBNLP | 3.89 | 97 | 7 | 0 | 91 | div,exp,mul,sqr,vcpower |
| fuzzy | misc | MBNLP | inf | 896 | 120 | 0 | 1056 | div,min |
| gams01 | misc | MBNLP | 8.08 | 145 | 110 | 0 | 1268 | exp,sqr,sqrt |
| gams03 | misc | MIQP | 0.233 | 2400 | 400 | 2000 | 1020 |  |
| gams05 | misc | IQCP | inf | 7093 | 0 | 7093 | 5707 |  |
| gasnet | misc | MBNLP | 0.0907 | 90 | 10 | 0 | 69 |  |
| gasprod_sarawak16 | misc | MBQCP | 0.00243 | 1526 | 38 | 0 | 2252 |  |
| gasprod_sarawak81 | misc | MBQCP | 0.00389 | 7571 | 38 | 0 | 11092 |  |
| ghg_2veh | misc | MBNLP | 0.0776 | 57 | 18 | 0 | 62 | div,exp,mul |
| ghg_3veh | misc | MBNLP | 0.213 | 96 | 36 | 0 | 119 | div,exp,mul |
| infeas1 | misc | NLP | 0.129 | 272 | 0 | 0 | 1614 | exp,log |
| like | misc | NLP | 728 | 9 | 0 | 0 | 3 | div,exp,log,mul,sqr |
| lop97ic | misc | MIQCQP | 0.0165 | 1753 | 0 | 1662 | 91 |  |
| pedigree_sim2000 | misc | MBQCP | 0.00176 | 2000 | 1000 | 0 | 794 |  |
| pedigree_sim400 | misc | MBQCP | 0.00168 | 400 | 150 | 0 | 101 |  |
| pindyck | misc | NLP | 0.615 | 116 | 0 | 0 | 96 | cvpower,mul |
| pricing050 | misc | NLP | 0.573 | 50 | 0 | 0 | 5 | exp,mul,power,sqr |
| procurement1large | misc | MBNLP | 3.01 | 7176 | 400 | 0 | 6054 | div,log,mul |
| procurement1mot | misc | MBNLP | 0.931 | 784 | 60 | 0 | 749 | div,log,mul |
| quantum | misc | NLP | inf | 2 | 0 | 0 | 0 | div,gamma,mul,rpower,sqr |
| routingdelay_proj | misc | MBNLP | 0.0156 | 1123 | 396 | 0 | 2977 | div,sqr |
| sepasequ_complex | misc | MBNLP | 0.0742 | 497 | 50 | 0 | 1310 | div |
| sssd18-08persp | misc | MBQCP | 0.00119 | 200 | 168 | 0 | 82 |  |
| sssd20-08persp | misc | MBQCP | 0.000514 | 216 | 184 | 0 | 84 |  |
| supplychainp1_053050 | misc | MBNLP | 0.261 | 15320 | 1680 | 0 | 33190 | sqrt |
| supplychainr1_053050 | misc | MBNLP | 0.0114 | 5150 | 1680 | 0 | 6580 | sqrt |
| uselinear | misc | MBNLP | inf | 6792 | 58 | 0 | 7030 | exp,log,mul |
| wastepaper5 | misc | MBNLP | 33.7 | 104 | 65 | 0 | 46 |  |
| wastepaper6 | misc | MBNLP | inf | 136 | 90 | 0 | 54 |  |
| csched2 | multiplant/cyclic scheduling | MBNLP | 0.38 | 401 | 308 | 0 | 138 | div,exp,mul |
| csched2a | multiplant/cyclic scheduling | MBNLP | 0.836 | 232 | 140 | 0 | 137 | div,exp,mul |
| multiplants_mtg1b | multiplant/cyclic scheduling | MBNLP | 0.0176 | 194 | 93 | 0 | 257 |  |
| multiplants_mtg1c | multiplant/cyclic scheduling | MBNLP | 0.361 | 245 | 120 | 0 | 319 |  |
| multiplants_mtg6 | multiplant/cyclic scheduling | MBNLP | 0.00453 | 350 | 176 | 0 | 481 |  |
| multiplants_stg1 | multiplant/cyclic scheduling | MBNLP | 2.51 | 415 | 198 | 0 | 262 |  |
| multiplants_stg1a | multiplant/cyclic scheduling | MBNLP | 0.805 | 424 | 216 | 0 | 250 |  |
| multiplants_stg1b | multiplant/cyclic scheduling | MBNLP | 0.497 | 476 | 243 | 0 | 280 |  |
| multiplants_stg1c | multiplant/cyclic scheduling | MBNLP | 0.748 | 477 | 252 | 0 | 270 |  |
| multiplants_stg5 | multiplant/cyclic scheduling | MBNLP | 0.0565 | 451 | 216 | 0 | 299 |  |
| nd_netgen-2000-2-5-a-a-ns_7 | network design w/ congestion/queue | MBQCP | 0.532 | 9999 | 2000 | 0 | 8088 |  |
| ndcc12 | network design w/ congestion/queue | MBQCP | 0.856 | 644 | 46 | 0 | 237 |  |
| ndcc12persp | network design w/ congestion/queue | MBQCP | 0.925 | 690 | 46 | 0 | 283 |  |
| ndcc13 | network design w/ congestion/queue | MBQCP | 0.194 | 630 | 42 | 0 | 254 |  |
| ndcc13persp | network design w/ congestion/queue | MBQCP | 0.186 | 672 | 42 | 0 | 296 |  |
| ndcc14 | network design w/ congestion/queue | MBQCP | 0.596 | 864 | 54 | 0 | 305 |  |
| ndcc14persp | network design w/ congestion/queue | MBQCP | 0.61 | 918 | 54 | 0 | 359 |  |
| ndcc15 | network design w/ congestion/queue | MBQCP | 0.243 | 680 | 40 | 0 | 306 |  |
| ndcc15persp | network design w/ congestion/queue | MBQCP | 0.21 | 720 | 40 | 0 | 346 |  |
| ndcc16 | network design w/ congestion/queue | MBQCP | 0.66 | 1080 | 60 | 0 | 377 |  |
| ndcc16persp | network design w/ congestion/queue | MBQCP | 0.653 | 1140 | 60 | 0 | 437 |  |
| telecomsp_metro | network design w/ congestion/queue | MBQCP | 0.0851 | 4284 | 4200 | 0 | 5078 |  |
| telecomsp_njlata | network design w/ congestion/queue | MBQCP | 0.0292 | 5198 | 5152 | 0 | 3466 |  |
| telecomsp_nor_sun | network design w/ congestion/queue | MBQCP | 0.0945 | 31926 | 31824 | 0 | 21270 |  |
| nuclear104 | nuclear core reload | MBQCP | inf | 23813 | 10816 | 0 | 14245 |  |
| nuclear10a | nuclear core reload | MBQCP | inf | 13010 | 10920 | 0 | 3339 |  |
| nuclear10b | nuclear core reload | MBQCP | 3.18 | 23826 | 10920 | 0 | 24971 |  |
| nuclear14 | nuclear core reload | MBQCP | 8.85e+05 | 1562 | 576 | 0 | 1226 |  |
| nuclear14a | nuclear core reload | MBQCP | 9.84 | 992 | 600 | 0 | 633 |  |
| nuclear14b | nuclear core reload | MBQCP | 0.0627 | 1568 | 600 | 0 | 1785 |  |
| nuclear25 | nuclear core reload | MBQCP | inf | 1678 | 625 | 0 | 1303 |  |
| nuclear25a | nuclear core reload | MBQCP | 9.95 | 1058 | 650 | 0 | 659 |  |
| nuclear25b | nuclear core reload | MBQCP | 0.0724 | 1683 | 650 | 0 | 1909 |  |
| nuclear49 | nuclear core reload | MBQCP | inf | 5735 | 2401 | 0 | 3873 |  |
| nuclear49a | nuclear core reload | MBQCP | 9.73 | 3341 | 2450 | 0 | 1431 |  |
| nuclear49b | nuclear core reload | MBQCP | 0.0478 | 5742 | 2450 | 0 | 6233 |  |
| nuclearva | nuclear core reload | MBQCP | 9.86e+05 | 351 | 168 | 0 | 317 |  |
| nuclearvb | nuclear core reload | MBQCP | 9.7e+05 | 351 | 168 | 0 | 317 |  |
| nuclearvc | nuclear core reload | MBQCP | inf | 351 | 168 | 0 | 317 |  |
| nuclearvd | nuclear core reload | MBQCP | inf | 351 | 168 | 0 | 317 |  |
| nuclearve | nuclear core reload | MBQCP | 9.64e+05 | 351 | 168 | 0 | 317 |  |
| nuclearvf | nuclear core reload | MBQCP | 9.76e+05 | 351 | 168 | 0 | 317 |  |
| blendgap | other pooling/blending | MBNLP | inf | 331 | 66 | 0 | 359 | errorf,exp,mul,sqr |
| crudeoil_pooling_ct1 | other pooling/blending | MBQCQP | 0.214 | 310 | 80 | 0 | 565 |  |
| crudeoil_pooling_dt2 | other pooling/blending | MBQCP | 0.00118 | 4962 | 1270 | 0 | 8178 |  |
| mpbp_03 | other pooling/blending | MBQCP | inf | 1104 | 384 | 0 | 2376 |  |
| mpbp_04 | other pooling/blending | MBQCP | inf | 954 | 240 | 0 | 2136 |  |
| mpbp_05 | other pooling/blending | MBQCP | inf | 1800 | 636 | 0 | 4232 |  |
| mpbp_06 | other pooling/blending | MBQCP | inf | 318 | 96 | 0 | 530 |  |
| mpbp_07 | other pooling/blending | MBQCP | inf | 1720 | 680 | 0 | 4106 |  |
| mpbp_09 | other pooling/blending | MBQCP | inf | 1890 | 720 | 0 | 4668 |  |
| mpbp_15 | other pooling/blending | MBQCP | inf | 1770 | 720 | 0 | 4224 |  |
| mpbp_19 | other pooling/blending | MBQCP | inf | 730 | 225 | 0 | 1540 |  |
| mpbp_21 | other pooling/blending | MBQCP | inf | 2020 | 810 | 0 | 5068 |  |
| mpbp_22 | other pooling/blending | MBQCP | inf | 1212 | 486 | 0 | 3028 |  |
| mpbp_30 | other pooling/blending | MBQCP | inf | 2058 | 728 | 0 | 4462 |  |
| mpbp_31 | other pooling/blending | MBQCP | inf | 980 | 225 | 0 | 2190 |  |
| mpbp_32 | other pooling/blending | MBQCP | inf | 1372 | 315 | 0 | 3138 |  |
| mpbp_33 | other pooling/blending | MBQCP | inf | 2160 | 720 | 0 | 4212 |  |
| mpbp_34 | other pooling/blending | MBQCP | inf | 2340 | 720 | 0 | 5088 |  |
| mpbp_35 | other pooling/blending | MBQCP | inf | 2130 | 600 | 0 | 4990 |  |
| mpbp_36 | other pooling/blending | MBQCP | inf | 1344 | 504 | 0 | 2744 |  |
| mpbp_46 | other pooling/blending | MBQCP | inf | 870 | 336 | 0 | 1932 |  |
| mpbp_47 | other pooling/blending | MBQCP | inf | 978 | 384 | 0 | 2280 |  |
| mpbp_48 | other pooling/blending | MBQCP | inf | 3408 | 1500 | 0 | 12690 |  |
| pooling_digabel16 | other pooling/blending | QCP | 0.000258 | 171 | 0 | 0 | 117 |  |
| pooling_digabel18 | other pooling/blending | QCP | 0.000132 | 208 | 0 | 0 | 412 |  |
| pooling_digabel19 | other pooling/blending | QCP | 0.000605 | 212 | 0 | 0 | 171 |  |
| pooling_epa3 | other pooling/blending | MBNLP | 0.00223 | 1104 | 150 | 0 | 1717 | exp,mul,vcpower |
| pooling_sppa0pq | pooling_spp | QCP | 0.00809 | 500 | 0 | 0 | 744 |  |
| pooling_sppa0stp | pooling_spp | QCP | 0.0195 | 616 | 0 | 0 | 1083 |  |
| pooling_sppa0tp | pooling_spp | QCP | 0.0182 | 500 | 0 | 0 | 744 |  |
| pooling_sppa5pq | pooling_spp | QCP | 0.0122 | 1245 | 0 | 0 | 1383 |  |
| pooling_sppa5stp | pooling_spp | QCP | 0.0154 | 1441 | 0 | 0 | 2361 |  |
| pooling_sppa5tp | pooling_spp | QCP | 0.012 | 1245 | 0 | 0 | 1383 |  |
| pooling_sppb0pq | pooling_spp | QCP | 0.0445 | 1537 | 0 | 0 | 1957 |  |
| pooling_sppb0stp | pooling_spp | QCP | 0.0588 | 1826 | 0 | 0 | 3127 |  |
| pooling_sppb0tp | pooling_spp | QCP | 0.0449 | 1537 | 0 | 0 | 1957 |  |
| pooling_sppb2pq | pooling_spp | QCP | 0.0389 | 3739 | 0 | 0 | 3897 |  |
| pooling_sppb2stp | pooling_spp | QCP | 0.0467 | 4208 | 0 | 0 | 7007 |  |
| pooling_sppb2tp | pooling_spp | QCP | 0.0393 | 3739 | 0 | 0 | 3897 |  |
| pooling_sppb5pq | pooling_spp | QCP | 0.001 | 8991 | 0 | 0 | 8751 |  |
| pooling_sppb5stp | pooling_spp | QCP | 0.00404 | 9753 | 0 | 0 | 16715 |  |
| pooling_sppb5tp | pooling_spp | QCP | 0.00383 | 8991 | 0 | 0 | 8751 |  |
| pooling_sppc0pq | pooling_spp | QCP | 0.122 | 3637 | 0 | 0 | 4586 |  |
| pooling_sppc0stp | pooling_spp | QCP | 0.126 | 4233 | 0 | 0 | 7442 |  |
| pooling_sppc0tp | pooling_spp | QCP | 0.117 | 3637 | 0 | 0 | 4586 |  |
| pooling_sppc1pq | pooling_spp | QCP | 0.163 | 5840 | 0 | 0 | 6530 |  |
| pooling_sppc1stp | pooling_spp | QCP | 0.247 | 6613 | 0 | 0 | 11330 |  |
| pooling_sppc1tp | pooling_spp | QCP | 0.17 | 5840 | 0 | 0 | 6530 |  |
| pooling_sppc3pq | pooling_spp | QCP | 0.0648 | 10567 | 0 | 0 | 10876 |  |
| pooling_sppc3stp | pooling_spp | QCP | 0.243 | 11635 | 0 | 0 | 20022 |  |
| pooling_sppc3tp | pooling_spp | QCP | 0.063 | 10567 | 0 | 0 | 10876 |  |
| hhfair | portfolio / finance | NLP | inf | 29 | 0 | 0 | 25 | sqr,vcpower |
| kport40 | portfolio / finance | MINLP | 0.0413 | 267 | 3 | 111 | 48 |  |
| portfol_classical200_2 | portfolio / finance | MBQCP | 0.0555 | 600 | 200 | 0 | 403 |  |
| portfol_shortfall200_05 | portfolio / finance | MBQCP | 0.0112 | 804 | 201 | 0 | 607 |  |
| saa_2 | portfolio / finance | MBNLP | 5.09 | 4407 | 400 | 0 | 6205 |  |
| worst | portfolio / finance | NLP | inf | 34 | 0 | 0 | 29 | div,errorf,exp,log,mul,sqr |
| sfacloc1_2_80 | sfacloc | MBNLP | 0.49 | 231 | 62 | 0 | 2088 |  |
| sfacloc1_2_90 | sfacloc | MBNLP | 0.334 | 199 | 30 | 0 | 348 |  |
| sfacloc1_2_95 | sfacloc | MBNLP | 0.195 | 171 | 9 | 0 | 208 |  |
| sfacloc1_3_80 | sfacloc | MBNLP | 3.18 | 293 | 62 | 0 | 2161 |  |
| sfacloc1_3_90 | sfacloc | MBNLP | 1.74 | 261 | 30 | 0 | 421 |  |
| sfacloc1_3_95 | sfacloc | MBNLP | 1.46 | 233 | 9 | 0 | 281 |  |
| sfacloc1_4_80 | sfacloc | MBNLP | 32.5 | 355 | 62 | 0 | 2234 |  |
| sfacloc1_4_90 | sfacloc | MBNLP | 7.85 | 323 | 30 | 0 | 494 |  |
| sfacloc1_4_95 | sfacloc | MBNLP | 7.36 | 295 | 9 | 0 | 354 |  |
| topopt-cantilever_60x40_50 | topology optimization | MBQCP | 28.8 | 33600 | 2400 | 0 | 14323 |  |
| topopt-mbb_60x40_50 | topology optimization | MBQCP | 15.7 | 33600 | 2400 | 0 | 14363 |  |
| topopt-zhou-rozvany_75 | topology optimization | MBQCP | 0.0202 | 1400 | 100 | 0 | 371 |  |
| tln12 | trim loss | MIQCP | 0.0398 | 168 | 12 | 156 | 72 |  |
| tls12 | trim loss | MINLP | 3.75 | 812 | 656 | 12 | 384 |  |
| tls5 | trim loss | MINLP | 0.157 | 161 | 131 | 5 | 90 |  |
| tls6 | trim loss | MINLP | 0.366 | 215 | 173 | 6 | 120 |  |
| tls7 | trim loss | MINLP | 1.12 | 345 | 289 | 7 | 154 |  |
| gams02 | unit commitment / energy scheduling | MBNLP | 0.0268 | 12688 | 96 | 0 | 14608 |  |
| gams04 | unit commitment / energy scheduling | MINLP | 0.000181 | 36766 | 6123 | 26 | 46137 |  |
| hydroenergy2 | unit commitment / energy scheduling | MBQCP | 0.00957 | 576 | 192 | 0 | 856 |  |
| hydroenergy3 | unit commitment / energy scheduling | MBQCP | 0.0184 | 1008 | 336 | 0 | 1498 |  |
| unitcommit_200_0_5_mod_7 | unit commitment / energy scheduling | MBQCP | 0.00158 | 28142 | 4450 | 0 | 77776 |  |
| unitcommit_200_100_1_mod_8 | unit commitment / energy scheduling | MBQP | 0.000262 | 25700 | 4514 | 0 | 64096 |  |
| unitcommit_200_100_2_mod_7 | unit commitment / energy scheduling | MBQCP | 0.000158 | 35370 | 4492 | 0 | 69569 |  |
| unitcommit_200_100_2_mod_8 | unit commitment / energy scheduling | MBQP | 0.00018 | 25609 | 4492 | 0 | 64348 |  |
| wastewater11m2 | wastewater | QCP | 0.425 | 303 | 0 | 0 | 251 |  |
| wastewater12m2 | wastewater | QCP | 0.353 | 516 | 0 | 0 | 407 |  |
| wastewater13m2 | wastewater | QCP | 0.313 | 1039 | 0 | 0 | 782 |  |
| wastewater14m1 | wastewater | QCP | 0.0001 | 74 | 0 | 0 | 46 |  |
| wastewater14m2 | wastewater | QCP | 0.27 | 208 | 0 | 0 | 204 |  |
| water | water design | NLP | 0.35 | 41 | 0 | 0 | 25 | abs,div,mul,vcpower |
| water3 | water design | MBNLP | 0.139 | 195 | 28 | 0 | 137 |  |
| waterful2 | water design | MBNLP | 0.999 | 629 | 56 | 0 | 383 |  |
| waternd2 | water design | MBNLP | 0.00319 | 232 | 72 | 0 | 249 | vcpower |
| waters | water design | MBNLP | 3.12 | 195 | 14 | 0 | 137 |  |
| watersbp | water design | MBNLP | 1.7 | 195 | 28 | 0 | 137 |  |
| waterx | water design | MBNLP | 0.126 | 70 | 14 | 0 | 54 |  |
| waterz | water design | MBNLP | 0.87 | 195 | 126 | 0 | 137 |  |
| waternd_blacksburg | waternd | MBNLP | 0.0974 | 591 | 490 | 0 | 205 | mul,signpower,vcpower |
| waternd_fossiron | waternd | MBNLP | 0.0161 | 907 | 754 | 0 | 326 | mul,signpower,vcpower |
| waternd_fosspoly0 | waternd | MBNLP | 0.0462 | 559 | 406 | 0 | 326 | mul,signpower,vcpower |
| waternd_fosspoly1 | waternd | MBNLP | 11.6 | 1429 | 1276 | 0 | 326 | mul,signpower,vcpower |
| waternd_hanoi | waternd | MBNLP | 0.0517 | 304 | 204 | 0 | 201 | mul,signpower,vcpower |
| waternd_modena | waternd | MBNLP | 0.239 | 5027 | 4121 | 0 | 1853 | mul,signpower,vcpower |
| waternd_pescara | waternd | MBNLP | 0.17 | 1556 | 1287 | 0 | 563 | mul,signpower,vcpower |
| waternd_shamir | waternd | MBNLP | inf | 135 | 112 | 0 | 46 | mul,signpower,vcpower |
| waterno1_02 | waterno1 | MBNLP | 0.00137 | 326 | 30 | 0 | 391 | signpower |
| waterno1_03 | waterno1 | MBNLP | 0.0107 | 495 | 45 | 0 | 600 | signpower |
| waterno1_04 | waterno1 | MBNLP | 0.0312 | 664 | 60 | 0 | 809 | signpower |
| waterno1_06 | waterno1 | MBNLP | 0.111 | 1002 | 90 | 0 | 1227 | signpower |
| waterno1_09 | waterno1 | MBNLP | 0.194 | 1509 | 135 | 0 | 1854 | signpower |
| waterno1_12 | waterno1 | MBNLP | 0.194 | 2016 | 180 | 0 | 2481 | signpower |
| waterno1_18 | waterno1 | MBNLP | 0.235 | 3030 | 270 | 0 | 3735 | signpower |
| waterno1_24 | waterno1 | MBNLP | 0.249 | 4044 | 360 | 0 | 4989 | signpower |
| waterno2_06 | waterno2 | MBNLP | 1.61 | 996 | 54 | 0 | 1234 |  |
| waterno2_09 | waterno2 | MBNLP | 5.87 | 1494 | 81 | 0 | 1852 |  |
| waterno2_12 | waterno2 | MBNLP | 7.07 | 1992 | 108 | 0 | 2470 |  |
| waterno2_18 | waterno2 | MBNLP | 12.7 | 2988 | 162 | 0 | 3706 |  |
| waterno2_24 | waterno2 | MBNLP | 14.4 | 3984 | 216 | 0 | 4942 |  |
| waterund01 | waterund | QCP | 0.00051 | 40 | 0 | 0 | 38 |  |
| waterund14 | waterund | QCP | 0.00029 | 125 | 0 | 0 | 135 |  |
| waterund17 | waterund | QCP | 0.01 | 74 | 0 | 0 | 66 |  |
| waterund18 | waterund | QCP | 0.00671 | 60 | 0 | 0 | 64 |  |
| waterund22 | waterund | QCP | 0.000259 | 146 | 0 | 0 | 135 |  |
| waterund25 | waterund | QCP | 0.0392 | 121 | 0 | 0 | 87 |  |
| waterund27 | waterund | QCP | 0.0836 | 432 | 0 | 0 | 208 |  |
| waterund28 | waterund | QCP | 0.0539 | 760 | 0 | 0 | 540 |  |
| waterund32 | waterund | QCP | 0.934 | 660 | 0 | 0 | 380 |  |
| waterund36 | waterund | QCP | 0.0905 | 324 | 0 | 0 | 239 |  |
