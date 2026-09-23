# Brainstorm 2, solver-core lens: theorems and algorithms that could change default solver behavior

Date: 2026-09-23. Viewpoint: a developer of a global MINLP solver (SCIP, Gurobi, BARON). The question is which results about spatial branching, bound tightening, nonlinear cut selection, relaxation choice, symmetry, or reuse across nodes could change a *default* on broad benchmarks (MINLPLib, QPLIB). A result that only helps a narrow family does not qualify.

Inputs: `/tmp/brainstorm2_context.md`, `scouting/scout_literature.md`, `scouting/scout_area23_bt_branch.md`, and a quick novelty search on the web. The eight targets were ranked after four feasibility probes with SCIP 10.0 (PySCIPOpt 6.2.1) and two small Gurobi toy computations. The scripts and raw data are in `scouting/brainstorm2-solvercore-probe/`.

## 0. Summary and ranking

| Rank | Target | Evidence from the probes | Novelty (bounded search) | Main risk |
|---|---|---|---|---|
| 1 | **Contraction theory for iterated OBBT, plus adaptive iterated OBBT** | Rounds 2–6 close a further ≥10 pp of the root gap on 41 of 140 instances. From the iterated-OBBT box, nodes fall 2.9× (33 instances). Toy problems show the predicted linear and sharp regimes | ~65% open | Used the known optimal value as cutoff; our OBBT loop is costly |
| 2 | **Provable activation rule for quadratic intersection cuts** | Root gap closure rises by 7.6 pp on average, but nodes are unchanged overall (ratio 0.97). Per-instance swings are 10–600× in both directions | ~70% open | Closing more root gap does not predict node savings |
| 3 | Symmetry handling in spatial B&B: one orbit representative plus node bounds | Not probed (in-house: `P_30` takes 11 nodes with symmetry handling and times out without it) | ~75% open | Only SCIP detects nonlinear symmetry |
| 4 | Cheap certificate that the SDP relaxation cannot prune a node | Not probed | ~50% (ML and heuristic rules exist) | QCQP-only; needs an SDP solver in the loop |
| 5 | Exact max–min branching point by bisection, plus the "fixed-multiplier blindness" proposition | Probe C: fixed-multiplier Lagrangian child bounds capture 2.3% (mean) of the true child gain | Monotonicity is folklore; blindness appears unstated | Branching noise (probe B) |
| 6 | Original-space "box-flower" cuts for continuous products | SCIP's continuous-product flower cuts change the root bound on 3 of 140 instances | ~60% | Little upside on MINLPLib |
| 7 | Tree-size model for spatial branching with width-dependent gains | Probe B: seed noise is as large as any branching-parameter effect | ~80% open | Cannot be validated on benchmark sets of normal size |
| 8 | Separation theorem: branching on linear forms or auxiliary variables versus coordinate branching | SCIP's auxiliary-variable branching changes nodes by 0.98× on 54 instances | ~70% | Negligible MINLPLib impact |

Discarded after the probes:

- **Box-parametric Lagrangian bounds with fixed multipliers.** These would reuse the parent's duals to bound children or tighten domains. Probe C shows they are blind to the tightening of McCormick relaxations; see §1.5.
- **Edge-concave cuts.** Enabling `separating/eccuts` changed the root bound on none of 140 instances.

## 1. Probes

All runs used 1 thread and the MINLPLib primal value `U` as the objective limit (tolerance 1e-6·max(1,|U|)). The pool has 208 instances: nonconvex MINLPLib instances listed as solved, with 5–400 variables and at most 3 per family (`pool.csv`). SCIP defaults were used otherwise.

### 1.1 Probe A: how much root gap does iterated OBBT close? (`probeA.py`, `probeA_summary.csv`)

**Method.** The sample is 140 instances whose root node has a positive gap with OBBT off. Round k runs a root-only SCIP solve with OBBT on. It starts from the original-variable global bounds left by round k−1, and stops after 6 rounds or when the summed relative width reduction falls below 1e-3. There are two OBBT modes: SCIP defaults, and "full" (no LP iteration limit, all variables). SCIP's own OBBT runs after the root LP loop, so the bound a round reports does not include that round's own tightening. Gap closed is therefore measured for the box *entering* each round, against the root bound with OBBT off.

**Results.** Gap closed, relative to the OBBT-off root bound:

| Box | Mean | Median | Share with ≥50% closed | Share fully closed |
|---|---|---|---|---|
| After 1 OBBT round (SCIP default effectively gets this) | 31.6% | 6.4% | 34% | 10% |
| After ≤6 rounds, default OBBT | 41.9% | 22.9% | 43% | 19% |
| After ≤6 rounds, full OBBT | 42.8% | 25.7% | 43% | 20% |

- Rounds 2 and later add ≥10 pp on 41/140 instances and ≥25 pp on 23/140. Examples: `tln5`, `waternd1`, `pooling_rt2tp`, `waterno2_02`, `nvs13`, and `spectra2` go from ≤32% to 94–100%.
- The full and default OBBT modes differ by only 1 pp. **The limit is the number of rounds, not the per-round LP budget.**
- 50/140 instances were still contracting at round 6. On several the per-round width reduction *grows* (`waternd1`: 4.3, 5.1, 9.4, 14.0, 17.5). This points to superlinear contraction toward the optimum.
- **An online trigger works.** Continue if the second round shrank the box at least half as much as the first. This rule catches 33 of the 41 instances that benefit, with 18 false positives among the other 99.

### 1.2 Probe A2: does the iterated-OBBT box reduce the tree? (`probeA2.py`, `probeA2_summary.csv`)

**Method.** The 41 instances with ≥10 pp extra closure were fully solved (300 s, seeds 0 and 1), once from the original box and once from the box left by iterated full OBBT.

**Results.**

- Both arms solve 33 instances. The iterated box also solves `forest` and `pooling_epa1`. Six instances stay unsolved in both arms: `alkylation`, `batch_nc`, `batch0812_nc`, `heatexch_spec2`, `prob07`, `waterund08`.
- **Nodes (shifted geometric mean, shift 10): 134.9 → 45.7, a ratio of 0.34.** 21 of 33 instances need ≥2× fewer nodes; one needs ≥1.5× more (`watertreatnd_conc`, 156 → 578).
- Time excluding OBBT: 1.37 s → 0.72 s (shifted geometric mean, shift 1). Our naive OBBT loop, which reruns the whole SCIP root each round, adds enough to make the total 3.37 s. The instances are easy, so cost matters. A real implementation must warm-start the rounds and restrict them to variables that moved.
- Sanity check: the iterated-box arm found the known optimum in every solve.

### 1.3 Toy check of the contraction theory (`toy_obbt.py`, `toy_sharp.py`, Gurobi)

**Quadratic growth.** The problem is `min x² + y² + a·xy` on `[-1,1.3]×[-1.2,1]`. The product `xy` is relaxed by McCormick, and the convex terms are kept exactly. The cutoff is `U = f* + 1e-6`. Exact LP/QCP-OBBT iterated to its limit gives *linear* convergence with a constant ratio:

| a | Observed ratio | sqrt(\|a\|/2) |
|---|---|---|
| 0.5 | 0.54 | 0.50 |
| 1 | 0.725 | 0.71 |
| 1.5 | 0.87 | 0.87 |
| 1.9 | 0.974 | 0.97 |

The ratio flattens once the width reaches the `sqrt(ε)` floor. The function is convex for |a| < 2, yet OBBT becomes arbitrarily slow as a → 2, because McCormick discards curvature.

**Sharp minimum.** The problem is `min −(x+y)` subject to `xy ≤ 1`, on `[0,3]×[0,2]`, with the optimum at the vertex-like point (3, 1/3). The width reaches 1.13·ε after two rounds, for both ε = 1e-3 and 1e-6.

### 1.4 Probe B: sensitivity of node counts to spatial-branching choices (`probeB.py`, `probeB.csv`)

**Method.** 54 instances that SCIP solves in 0.3–120 s with ≥100 nodes. Nine settings, 300 s:

- default;
- two random-seed shifts;
- branching point `midpull` = 0 (LP value) or 1 (midpoint);
- branching on auxiliary variables (`constraints/nonlinear/branching/aux=0`);
- violation-only scores;
- dual-value weight 1;
- domain-width weight 1.

**Results** on the 48 instances solved by all settings. Ratios are shifted geometric means of nodes against default:

| Group | Node ratio vs default |
|---|---|
| Seed shifts | 1.24 and 0.90 |
| Branching settings | 0.85 (domain weight), 0.85 (dual weight), 0.90 (LP point), 1.01 (midpoint), 0.98 (auxiliary variables), 1.05 (violation only) |

- The virtual best of 3 seeds (0.745) equals the virtual best of 3 branching settings (0.745).
- The standard deviation of the per-instance log node ratio is 0.97 across seeds and 0.87 across branching settings.
- 12 of 48 instances are unaffected by every branching setting.
- **Conclusion.** On MINLPLib-sized samples, node counts under different spatial-branching rules are dominated by performance variability. A branching theorem would need an effect well above about 20%, or an evaluation on several hundred instances with at least 3 seeds. This lowers every branching target (5, 7, 8) relative to bound tightening.

### 1.5 Probe C: fixed-multiplier box-parametric Lagrangian bounds (`probeC.py`, `probeC_out/`, Gurobi LPs)

**Idea tested.** Take the parent McCormick LP with duals `y`. For a sub-box B′, the bound

    Φ_y(B′) = y^T b(B′) + Σ_k min_{z_k∈box_k(B′)} (c − A(B′)^T y)_k z_k

is valid, and its rows are rebuilt for B′. Each McCormick plane is monotone under shrinking the box, so Φ with rebuilt rows dominates the classical reduced-cost bound (rows kept). If Φ were strong, it would give zero-LP child bounds and a relaxation-aware form of marginals-based range reduction.

**Setup.** 108 QCQPs, 10 branching candidates each at the clamped LP point, 1,378 children. Sanity check: Φ equals the LP value at the root on all 108.

**Results.**

- The true child LP bound rises in 857 children.
- Φ with rebuilt rows rises in only 50 (8 instances), and Φ with fixed rows in 27.
- The mean share of the true child gain that Φ captures is 2.3%, with median 0.

**Explanation (a proposition to write up).** With y fixed, the Lagrangian separates by variable. Rebuilding a McCormick row after moving `l_i` to `p` adds `y_r (p − l_i)(x_j − l_j)` to it. This term vanishes at `x_j = l_j`, so the minimization over the partner's interval removes it. The term survives only when the partner is nonbasic at the opposite bound. **Reusing parent duals cannot see relaxation tightening.** At least one dual re-optimization is required, and that is strong branching.

### 1.6 Probe D: what do the disabled SCIP cut families add? (`probeD.py`, `probeD.csv`)

**Root only (140 instances), gap closed compared with the default root:**

- **Quadratic intersection cuts** (`nlhdlr/quadratic/useintersectioncuts`, with monoidal strengthening): +7.6 pp mean. 37 instances gain ≥5 pp and 12 lose ≥5 pp. Top gains: `kall_congruentcircles_c41` +100, `st_iqpbk2` +81, `st_iqpbk1` +78, `supplychain` +78, `pooling_adhya1pq` +76.
- **Edge-concave cuts** (`separating/eccuts/freq=0`): no change on any instance.
- **Flower cuts on continuous products** (`separating/flower/scanproduct`): the root changes on 3 instances; the only gain is `wager`, +9.5 pp.

**Full solves (54 instances), nodes:**

- Intersection cuts: overall ratio 0.974, with 53/54 solved. Large per-instance swings in both directions:

| Instance | Default nodes | With intersection cuts |
|---|---|---|
| `st_m1` | 601 | 1 |
| `st_e03` | 173,671 | 16,535 |
| `sssd08-04persp` | 39,330 | 18,817 |
| `process` | 680 | 13,784 |
| `nous1` | 1,907 | 4,321 |
| `st_fp7a` | 277 | 765 |

- Edge-concave and flower cuts: trees identical to default.
- The run times in probe D are not comparable with probe B, because the machine load differed.

## 2. Research targets

### T1 (rank 1). Contraction theory for iterated OBBT, plus adaptive iterated OBBT

**Statement to prove.**

*Setting:*

- The problem is `min f(x)` subject to `g(x) ≤ 0`, `x ∈ B₀`.
- The relaxation `R(B)` is factorable (McCormick, α-BB, or similar) and inclusion-isotone.
- It has pointwise convergence order 2 with constant τ: for x ∈ B, the relaxed objective and constraint values are within `τ·w(B)²` of the true ones (Bompadre–Mitsos 2012 for McCormick).
- The OBBT operator is `T_U(B) = box-hull{x ∈ B : some lifted point of R(B) over x has relaxed objective ≤ U}`.
- The problem has a unique global minimizer x*, and U = f* + ε.

*Claims:*

- **(a) Sharp minimum.** Assume `f(x) − f* ≥ κ‖x − x*‖` near x*, in the constrained case through an error bound on the constraint violation (the framework of Kannan–Barton 2017). Then `w(T_U(B)) ≤ (2τ/κ)·w(B)² + 2ε/κ`. So iterated OBBT converges quadratically to a box of width O(ε/κ) once `w(B) < κ/(4τ)`.
- **(b) Quadratic growth μ.** `w(T_U(B)) ≤ 2·sqrt((τ w(B)² + ε)/μ)`. This is linear convergence with rate `ρ = 2·sqrt(τ/μ)` when ρ < 1, down to a floor of Θ(sqrt(ε/μ)). If ρ ≥ 1 there is no contraction.
- **(c) Tightness.** For `f = ‖x‖² + a·x₁x₂` with McCormick, the exact rate is ρ(a); numerically ρ(a) ≈ sqrt(|a|/2). So OBBT is arbitrarily slow even on convex f. The goal is a closed form with a proof, and matching lower-bound families in n dimensions.
- **(d) Corollary.** Branch-and-bound that runs iterated OBBT at nodes near the incumbent is cluster-free in case (a), and in case (b) when ρ < 1. The reason is that OBBT then acts as a width-tight reduction. This connects to in-house Theorem 3 (`results/cluster-free-branch-and-bound-constrained-minima.md`) and to Kannan–Barton 2018, open item (iii).

**Algorithm (the implementable output).** Adaptive iterated OBBT:

- After each round, compute the width-contraction ratio.
- Continue while the ratio is ≤ ρ_max (probe: 0.5).
- Restrict later rounds to variables whose bounds moved, and warm-start from the previous basis.
- Re-trigger at the root after each incumbent improvement (ε shrinks), and at nodes whose box is within a small multiple of the incumbent's neighborhood.

**Why it would change solver behavior.**

- SCIP runs OBBT once, at the root (`propagating/obbt/freq=0`).
- Gleixner et al. (JOGO 2017) report that "OBBT alone does not give a significant speedup on average".
- Probe A says a single round captures about half of what the iterated limit gives (31.6% against 42.8% mean gap closed; 10% against 20% fully closed). The value lies in the fixed point.
- The theory supplies the missing stopping rule.

**What is known.**

- Caprara–Locatelli (MP 2010) and Caprara–Locatelli–Monaci (COAP 2016) define the limit and show that reaching it cannot be guaranteed in general.
- Zamora–Grossmann (JOGO 1999), branch-and-contract: a finite contraction operation, with no rate.
- Iteration to a fixed point is used without theory in power systems (Coffrin et al. CP 2015; Gopinath et al., arXiv:1910.03716), in Alpine, and in Couenne's aggressive bound tightening.
- Convergence-order theory (Bompadre–Mitsos; Kannan–Barton 2017/2018) analyzes branch-and-bound, not OBBT iterations.
- Web searches for OBBT rates found nothing.
- Parts (a) and (b) will read as near-folklore once phrased in convergence-order language. **The new content is (c), the constrained version, and the rule in (d) together with the algorithm.**

**Validation plan.**

1. Write proofs for (a) and (b). For (c), prove the closed form for the 2-D family, then n-D.
2. Implement a PySCIPOpt propagator that runs its own OBBT through diving LPs (`startDive`, `chgVarObjDive`, `solveDiveLP`), with warm starts and the contraction trigger. It runs at the root after incumbent changes, and at depth ≤ d near the incumbent.
3. Benchmark on all solved nonconvex MINLPLib instances and on QPLIB QCQPs, with 3 seeds and **no objective limit** (realistic incumbents). Report solved counts and the shifted geometric mean of time. Break results down by the trigger to isolate its effect.
4. Separately, measure how the width of the limit box scales with `U − f*`, which (a) and (b) predict.

**Risks.**

- Probe A2 used the optimal value as the cutoff. With heuristic incumbents the limit box is wider (Θ(ε) or Θ(sqrt ε)).
- The cost of OBBT dominates on easy instances.
- Six hard instances stayed unsolved in both arms.

### T2 (rank 2). A provable activation rule for quadratic intersection cuts

**Statement to prove.** Take an LP vertex x̄ with simplex cone rays r_j, a quadratic constraint S = {q ≤ 0}, and a maximal S-free set C (Muñoz–Serrano; Muñoz–Paat–Serrano). For each ray, let s_j be the step to ∂C and t_j the step to the node box.

- **(i) Box dominance.** If `s_j ≥ t_j` for every ray, the intersection cut is implied by the LP relaxation together with the box (after the cone is truncated at the box).
- **(ii) Depth bound.** In general, the depth of the intersection cut beyond the cut obtained from the box-truncated cone (SCIP's `useboundsasrays` variant) is bounded by an explicit function of `{(t_j − s_j)_+}` and ‖∇q(x̄)‖.
- **(iii) Balanced signs.** Target a structural corollary: if the signed graph of the bilinear terms of q is balanced (switchable to all nonpositive coefficients), the termwise McCormick relaxation is the convex envelope of q over the box. This is the submodular / Lovász-extension case, in the spirit of Crama 1993. Determine when that makes the cut inactive at McCormick vertices.

**The rule.** Separate only where the predicted depth-to-density ratio is above a threshold, per constraint.

**Why it would change solver behavior.**

- SCIP 8 and 9 ship these cuts disabled, stating "it is not clear yet how to decide when it will be beneficial".
- Probe D: +7.6 pp of root gap on average and 10–600× node swings in both directions, yet a neutral total.
- A rule that keeps the wins (`st_m1`, `st_e03`, `sssd08`) and avoids the losses (`process`, `nous1`, `st_fp7*`) would turn on a feature no other solver has.

**What is known.**

- Characterization of maximal quadratic-free sets, closed-form cuts, and monoidal strengthening (Chmiela–Muñoz–Serrano, MP 2023 and 2025).
- There is no selection theory. Cut-selection learning (Paulus et al. ICML 2022; Turner et al.) addresses MILP.

**Validation plan.**

1. Compute the ray statistics at the root inside a PySCIPOpt separator. The nonlinear handler's cuts cannot be toggled per constraint from Python, so start with an instance-level decision made from root statistics. Then implement a per-constraint version as a C patch to `nlhdlr_quadratic`.
2. Correlate the predicted depth with the node change over MINLPLib and QPLIB, with 3 seeds.
3. Success means the rule-on setting beats both always-on and always-off by more than the seed noise measured in probe B.

**Risk.** Probe D already shows that root-gap closure does not predict node savings. The rule may need a node-effect proxy, such as the gap closed at depth-1 children, rather than depth alone.

### T3 (rank 3). Symmetry handling in spatial branch-and-bound: one orbit representative and node bounds

**Statement to prove.**

- **(i) Unique representative.** Take a finite group of signed permutations acting on the variables. Spatial branching uses half-open disjunctions `x_i ≤ p` versus `x_i > p` (closed only in the relaxation). With lexicographic or orbitopal reduction applied to the leaf's original-variable box, every optimal orbit keeps exactly one representative among the leaves of any finite tree. This repairs van Doornmalen–Hojny, Remark 14.
- **(ii) Node bound.** For the in-house S_n-symmetric concave family `P_n`, which needs exponentially many leaves under every coordinate spatial branching without symmetry handling, orbitopal reduction gives poly(n) nodes. The bound should survive symmetry-preserving perturbations.

**Why it would change solver behavior.** Gurobi, BARON, and Xpress do not handle symmetry in nonlinear parts (FICO, arXiv:2605.04850). A theorem with a polynomial node bound is the argument for adding it.

**Evidence.** In-house: SCIP solves `P_30` in 11 nodes with symmetry handling and times out without it.

**Validation.**

- SCIP `misc/usesymmetry` on and off on symmetric MINLPLib families (`kall_*`, `pointpack*`, `graphpart_*`, packing), with 3 seeds.
- Gurobi with static symmetry-breaking constraints generated from SCIP's detected generators, against none.

**Risk.** Detection is the bottleneck in other solvers. The node bounds may hold only for designed families.

### T4 (rank 4). A cheap certificate that the SDP relaxation cannot prune a node

**Statement to prove.**

- From the LP (McCormick+RLT) solution `(x̄, X̄)`, construct in O(n³) an SDP-feasible `(x̃, X̃)`: shift the moment matrix by its negative eigen-part, then repair RLT slacks along a fixed direction.
- Show `obj(x̃, X̃) − z_LP ≤ C·λ₋(M(x̄, X̄))·(1 + ‖slack⁻¹‖)`, where λ₋ is the most negative eigenvalue.
- If `obj(x̃, X̃) < U`, the SDP bound cannot prune the node, so the solver skips the SDP. The certificate is exact in the "no" direction.

**Why it would change solver behavior.** It turns "when to solve the SDP" from ML or heuristics into a certificate with no false negatives.

**Known.**

- BARON solves SDPs "parsimoniously" (Nohra–Raghunathan–Sahinidis).
- Learning-to-relax (arXiv:2501.03954).
- SDP-quality convex quadratic relaxations (arXiv:2106.13721).

**Validation.** QPLIB box-QP and QCQP. Count the SDP solves avoided at equal final trees, in a Python B&B or through Gurobi callbacks plus an external SDP solver.

**Risk.** Limited to QCQPs. Neither SCIP nor Gurobi solves SDPs natively, so the benefit is for SDP-based codes.

### T5 (rank 5). Exact max–min branching point by bisection, and fixed-multiplier blindness

**Statement.**

- **(i) Bisection.** For inclusion-isotone relaxations, the child bounds `v_L(p)` (nonincreasing) and `v_R(p)` (nondecreasing) are monotone in the split point. The point maximizing `min(v_L, v_R)` is found by bisection in O(log(w/δ)) LP solves, each a few warm-started dual simplex pivots.
- **(ii) Non-unimodality.** Give a counterexample showing that the product score `(v_L − z)(v_R − z)` is not unimodal.
- **(iii) Blindness.** The proposition from probe C: with fixed parent multipliers, the child Lagrangian bound equals the parent bound unless some partner variable of the branched variable is nonbasic at the opposite bound.

**Why it matters.** Extreme strong branching (Dey–Han–Wang, arXiv:2510.20650) evaluates a grid of points and has no theory. (i) is the exact version, and (iii) rules out the cheap shortcut.

**Validation.** A PySCIPOpt branching rule using probing LPs (`startProbing`, `chgVarUbProbing`, `solveProbingLP`) on the probe B set extended to about 300 instances, with 5 seeds.

**Risk.** Probe B's noise level. Max–min may not be the right score for tree size.

### T6 (rank 6). Original-space box-flower inequalities for products of continuous variables

**Statement.** Via `x = l + (u − l)∘y`, a multilinear set on a general box is a linear image of the multilinear polytope of the completed hypergraph. Derive original-space 1- and 2-flower inequalities valid for `l > 0` without relaxing lower bounds to 0, and show O(|E|²) separation for fixed rank. This is Q8 in the literature scout, and it addresses SCIP 10's stated reason for disabling the feature.

**Evidence against high impact.** SCIP 10's continuous-product flower separator changes the root bound on only 3 of 140 MINLPLib instances. The application is polynomial and multilinear test sets (BARON's random multilinear tests, parts of QPLIB), not MINLPLib broadly.

**Validation.** A PySCIPOpt separator on multilinear QPLIB and on POLIP-style instances.

**Risk.** Low benchmark coverage; the extended-space part may be folklore.

### T7 (rank 7). A tree-size model for spatial branching with width-dependent gains

**Statement.** In an abstract model where a child's gap is `τ·w^β` and the split point is continuous, find the minimax-optimal variable and point rule. Show when strong branching beats violation or pseudocost rules by a factor that grows with the tolerance. This is the spatial analogue of Le Bodic–Nemhauser and of Dey et al. (MP 2024).

**Why it is low now.** Probe B shows that a 48-instance test cannot separate a 15% rule effect from seed variability. The virtual best over seeds equals the virtual best over rules.

**Validation.** Needs about 300+ instances and 3–5 seeds, or synthetic families where the model's parameters are controlled.

**Risk.** A good theory with little measurable benchmark impact.

### T8 (rank 8). Separation between branching on linear forms or auxiliary variables and coordinate branching

**Statement.** Find a ridge-sum family `Σ_k g_k(a_k^T x)` with concave g_k that needs exponentially many coordinate branches (the in-house lower bounds give this side) but only polynomially many when branching on `z_k = a_k^T x`. Also find a family showing the reverse. The in-house affine-branching barrier note leaves this open.

**Evidence.** SCIP's `constraints/nonlinear/branching/aux=0` changes nodes by 0.98× on 54 instances, with one instance changing ≥2×.

**Risk.** Theory interest only on MINLPLib.

## 3. Caveats

- **Known optimum as cutoff.** Probes A, A2, B and D give SCIP the known optimal value as the objective limit. This removes primal-heuristic noise but overstates what OBBT can do early in a real solve.
- **Presolved bounds.** Bounds in probe A are read from SCIP's transformed variables. Aggregated variables are skipped, and presolve dual reductions keep only some optimal solutions. The iterated-box solves in A2 all found the known optimum.
- **Time measurements.** Times in probes A2 and D come from runs with 17–34 concurrent processes. Treat only node counts as comparable across probes.
- **Probe C scope.** Probe C uses the plain McCormick LP (with secant and endpoint tangents for squares), not SCIP's relaxation. It skips 22 large and 10 unbounded instances.
- **Toy rate.** The rate sqrt(|a|/2) in §1.3 is a numerical observation, not a proof.
- **Novelty.** Novelty levels come from bounded web searches and the repository's scout reports. They are not proofs of novelty.

## 4. Commands run (targeted; no project-wide checks)

All scripts are in `scouting/brainstorm2-solvercore-probe/`, run with `~/miniconda3/envs/exact-quadratic-hull/bin/python`:

- `pass0.py`: default SCIP on the 208-instance pool, 120 s.
- `probeA.py selA.csv`: iterated OBBT, 140 instances.
- `probeA2.py`: full solves, 41 instances × 2 arms × 2 seeds.
- `probeB.py selB.csv`: 54 instances × 9 settings.
- `mkbounds.py selC.txt 2` followed by `probeC.py $(cat selC.txt)`: 142 QCQPs; 108 evaluated.
- `probeD.py 32`: 140 root-only runs × 4 settings, and 54 full solves × 3 settings.
- `toy_obbt.py` and `toy_sharp.py`: Gurobi 13.0.3.
