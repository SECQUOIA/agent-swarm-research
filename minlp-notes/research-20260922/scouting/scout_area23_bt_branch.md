# Scout report, areas A and B: bound tightening and spatial branching

Date: 2026-09-22. Scope: literature on domain reduction and spatial branching for nonconvex MINLP, with emphasis on explicitly stated open problems and missing theory. Sources: the local KB (`literature/papers/<slug>`, cited as [KB:slug]), in-house results and notes in `/workspace/repo/minlp-notes`, and web search. Quotations come from full texts I read (Kannan–Barton 2017 and 2018, Gleixner et al. 2017, Caprara–Locatelli–Monaci 2016 abstract, Dey–Han–Wang 2025) or from KB summaries. "Unsolved" judgments reflect a bounded search. They are not proofs of novelty.

## In-house baseline (what the repository already covers)

- `results/fbbt-monotone-system-hardness.md`: approximating the **FBBT limit** of bilinear systems to constant additive error is PosSLP-hard, even on the unit cube with feasibility promised. The note makes no NP-hardness claim.
- `results/fbbt-doubly-exponential-convergence.md`: primitive FBBT needs at least `2^(2^n-1)` updates on a bilinear system of size `4n+4`, under every schedule. The primitive-iteration theorem is Lean-verified.
- `results/spatial-bb-*-exponential-lower-bound.md` (seven notes): `2^Ω(n)` leaf lower bounds at a fixed gap for coordinate spatial branching. They hold under separable, SDP–RLT, higher-order SOS, product-domain, quadratic-cut, monomial-lift, and relative-gap node oracles. `notes/spatial-bb-affine-branching-barrier.md` shows that the proof method **does not** extend to dense affine (hyperplane) branching. It does not give a short algorithm for that case.
- `results/cluster-free-branch-and-bound-constrained-minima.md`: near a nondegenerate KKT minimizer, the number of unfathomed boxes at a fixed scale is bounded independently of ε. This bypasses the neighborhood question in Kannan–Barton (2018). Its Theorem 3 covers reduced-space schemes with **width-tight** domain reduction, such as interval Newton. Anchoring without width control (Kannan–Barton 2018, Examples 17–18) is explicitly not covered.
- `notes/candidate-directions.md`: item 2, "complexity of the greatest fixed point of FBBT with bilinear nodes", is now covered by the FBBT results. Item 13, "geometric convergence rate of iterated OBBT", is marked low priority and is **not started**.

---

## A. Bound tightening and domain reduction

### A1. OBBT (optimization-based bound tightening)

**State of the art.**
- Gleixner, Berthold, Müller, Weltge, "Three enhancements for optimization-based bound tightening", *J. Glob. Optim.* 67(4) (2017), https://doi.org/10.1007/s10898-016-0450-4 (preprint: https://optimization-online.org/DB_HTML/2016/03/5356.html).
  - Enhancements: filtering with LP solutions to skip bound LPs, greedy ordering for simplex warm starts, and Lagrangian variable bounds (LVBs). LVBs are one-row aggregations obtained from OBBT duals and propagated by FBBT throughout the tree.
  - The conclusion is purely empirical: on average, the cost of OBBT largely offsets the benefit of its smaller B&B trees. Propagating LVBs improves this tradeoff. There is no theory of OBBT strength.
- Caprara & Locatelli, "Global optimization problems and domain reduction strategies", *Math. Program.* 125 (2010) 123–137.
- Caprara, Locatelli, Monaci, "Theoretical and computational results about optimality-based domain reductions", *Comput. Optim. Appl.* 64(2) (2016) 513–533, https://doi.org/10.1007/s10589-015-9818-5. This is the main theoretical OBBT paper. Abstract: although a lower limit on reduction is readily definable, attaining it is not generally guaranteed. They give strategies that reach the limit on a nontrivial problem class, but lose that guarantee on a slightly broader class.
- Puranik & Sahinidis, "Domain reduction techniques for global NLP and MINLP optimization", *Constraints* 22(3) (2017) 338–376, arXiv:1706.08601 [KB:puranik2017-domain-reduction-techniques-for-global].
  - Surveys feasibility-based reduction, which solves a global min/max per variable, or a convex- or LP-relaxation surrogate, and optimality-based reduction.
  - In a solver ablation on 1,740 instances, turning reduction off increases BARON nodes by 261–1,180%, SCIP nodes by 152–417%, and Couenne nodes by 21–186%.
  - Open directions (p. 21): filtering based on **sets** of constraints, fixed-point acceleration with reliability guarantees, principled scheduling of probing and OBBT, and reduction methods that prevent clustering.
- Gómez-Casares, González-Rodríguez, González-Díaz, Rodríguez-Fernández, "Impact of domain reduction techniques in polynomial optimization: A computational study", arXiv:2403.02823 (2024; revised 2025). Covers OBBT with conic relaxations and FBBT with Lagrangian dual information inside RAPOSa's RLT scheme. Future work: machine-learning choice of the reduction technique.
- González-Díaz, González-Rodríguez, Gómez-Casares, "Bound tightening in lifted formulations", arXiv:2509.18731 [KB:diaz2025-bound-tightening-in-lifted-formulations]. RLT bound-factor constraints already imply explicit lifted-variable bounds (Theorem 1), yet keeping the redundant rows changes solver time by −48% to +73% depending on the LP subsolver. Polyhedral equivalence does not imply algorithmic equivalence.

**Power systems and learning OBBT (2021–2026).**
- Coffrin, Hijazi, Van Hentenryck, "Strengthening convex relaxations with bound tightening for power network optimization", CP 2015 (https://www.coffrin.com/preprint/qc_fp.pdf). They iterate QC-relaxation OBBT to a **fixed point**.
- Chen, Atamtürk, Oren, "Bound tightening for the AC OPF problem", *IEEE Trans. Power Syst.* (2016).
- Sundar, Nagarajan, Misra, Lu, Coffrin, Bent, "OBBT using a strengthened QC-relaxation of OPF", arXiv:1809.04565 (journal version about 2023). Its strengthened QC relaxation gives the tightest bounds found, with negligible runtime cost.
- Cengil, Nagarajan, Bent, Eksioglu, Eksioglu:
  - "Learning to accelerate globally optimal solutions to the AC OPF problem", *Electric Power Systems Research* (2022), https://www.sciencedirect.com/science/article/abs/pii/S0378779622004709.
  - "Learning to accelerate tightening of convex relaxations of the AC OPF problem", *Comput. Optim. Appl.* 92 (2025) 761–786, https://doi.org/10.1007/s10589-025-00715-7.
  - The later paper learns a dynamic policy that selects which voltage-magnitude and angle-difference variables to tighten at each OBBT iteration. It reports a 9.3× average and up to 20× speedup, on networks with up to 3,375 buses. The policy is purely empirical, with no guarantee about the fixed point.
- Alpine.jl [KB:nagarajan2026-alpine-jl-v0-5-8] iterates OBBT until the bounds reach a fixed point, then adaptive multivariate partitioning.
  - Kannan, Nagarajan, Deka, "Strong partitioning and a ML approximation for accelerating global optimization of nonconvex QCQPs", *INFORMS J. Comput.* (2025), https://doi.org/10.1287/ijoc.2023.0424, arXiv:2301.00306. They learn the partition points and report a 2–4.5× average reduction in Alpine time. They caution that exact solution of the max-min strong-partitioning problem can be difficult.
- Neural-network verification is a MILP setting that reuses OBBT: Badilla, Goycoolea, Muñoz, Serra, "Computational tradeoffs of OBBT in ReLU networks", arXiv:2312.16699. Also rolling-horizon OBBT, arXiv:2401.05280.

**Solvers.**
- SCIP 8 [KB:bestuzheva2025-global-optimization-of-mixed-integer]: root OBBT on the LP relaxation over the variables that separators use for bounds, with an iteration limit. It learns LVBs at the root and propagates them through the tree. NLP-based OBBT (Müller et al.) is available but off by default.
- BARON: marginals-based reduction (Ryoo & Sahinidis, *J. Glob. Optim.* 8 (1996) 107–138; the 1995 version is in [KB:ryoo1995-global-optimization-of-nonconvex-nlps]), probing, and OBDR (see A3). Belotti et al. 2009 measured BARON spending 77% of its time in probing.
- Couenne: shallow OBBT, and aggressive bound tightening (ABT) around the incumbent [KB:belotti2009-branching-and-bounds-tightening-techniques].
- Alpine: iterated OBBT to a fixed point.
- Gurobi 13 and Octeract: nothing public beyond "spatial B&B with outer approximation".

**Open problems and missing theory.**
1. **Convergence and complexity of iterated OBBT.** The OBBT map `B ↦ box-hull(R(B) ∩ {f ≤ U})` is monotone and deflationary when the relaxation `R(B)` is monotone in the box, so a greatest fixed point exists. I found no theorem on:
   - its convergence rate;
   - whether it terminates finitely;
   - the complexity of computing the fixed point;
   - how far it lies from the box hull of the true feasible set.

   Caprara–Locatelli–Monaci (2016) emphasize the difficulty of guaranteeing attainment of the limit. Puranik–Sahinidis ask for fixed-point acceleration with reliability guarantees. Alpine and power-systems codes iterate to a fixed point without such theory. The in-house FBBT hardness and slow-convergence results **do not** transfer automatically: LP-OBBT combines constraints and may escape the monotone least-fixed-point construction. **Likely open (≈75%).**
2. **Constraint-set filtering** (Puranik–Sahinidis): tractability boundaries for exact bounds over a set of k constraints of a given structure. Belotti 2013 handles pairs of linear inequalities (*J. Glob. Optim.* 56(3) 787–819). For bilinear constraints: Müller, Serrano, Gleixner, "Using two-dimensional projections for stronger separation and propagation of bilinear terms", *SIAM J. Optim.* (2022), https://doi.org/10.1137/19m1249825. Open in general.
3. **Value of OBBT in node count.** No theorem quantifies how much OBBT reduces the B&B tree, for example in convergence-order terms. See B2 and the cluster problem.

### A2. FBBT and constraint propagation

**State of the art.**
- Belotti, Cafieri, Lee, Liberti, "On feasibility based bounds tightening", Optimization Online 3325 (2012); COCOA 2010 [KB:belotti2012-on-feasibility-based-bounds-tightening]. FBBT is a monotone deflationary operator whose limit is the greatest fixed point. For linear constraints the limit is computable by an LP (Theorem 4.1). They give examples where finite convergence fails and state a dimension-drop criterion (Theorem 3.3).
- Bordeaux, Hamadi, Vardi, CP 2007; Bordeaux, Katsirelos, Narodytska, Vardi, *JAIR* 40 (2011): NP-completeness of the **integer** bound-propagation fixed point. The continuous linear case is LP-solvable.
- Sofranac, Gleixner, Pokutta, "An algorithm-independent measure of progress for linear constraint propagation", CP 2021 / *Constraints* (2022), arXiv:2106.07573. Measures propagation progress against the LP-computed limit, including with unbounded domains. Related GPU propagation work is by the same group.
- Domes & Neumaier, *Constraints* (2010), on quadratic propagation with rigorous rounding [KB:domes2010-constraint-propagation-on-quadratic-constraints].
- In-house: PosSLP-hardness of the bilinear FBBT limit, and `2^(2^n)` slow convergence.

**Solvers.** Every solver runs FBBT at every node: SCIP (DAG plus quadratic propagation), BARON, Couenne, ANTIGONE, Gurobi, and interval solvers.

**Open or missing theory.**
- An **upper** complexity bound for the continuous bilinear FBBT limit. The in-house work gives only the PosSLP-hardness lower bound. Membership in the existential theory of the reals (∃R) or in counting classes is not addressed.
- A **quantitative progress measure** for nonlinear propagation, extending Sofranac et al. beyond linear constraints.
- FBBT and OBBT are **incomparable** in general: FBBT is exact per nonlinear constraint, while OBBT combines constraints through a relaxation. This is a standard remark, and no hierarchy theorem exists.

### A3. Duality- and optimality-condition-based reduction

- Ryoo & Sahinidis (1996): marginals-based reduction. For an active bound `x ≤ u` with multiplier `λ > 0`, relaxation value `L`, and incumbent `U`, the reduced lower bound is `x ≥ u − (U − L)/λ`.
- Tawarmalani & Sahinidis, *Math. Program.* 99 (2004) [KB:tawarmalani2004-global-optimization-of-mixed-integer]: unified Lagrangian reduction.
- Gleixner & Weltge, CPAIOR 2013: learning and propagating LVBs.
- Puranik & Sahinidis, "Bounds tightening based on optimality conditions for nonconvex box-constrained optimization", *J. Glob. Optim.* 67 (2017), https://doi.org/10.1007/s10898-016-0491-8.
- Zhang, Sahinidis, Nohra, Rong, "Optimality-based domain reduction for inequality-constrained NLP and MINLP", *J. Glob. Optim.* 77(3) (2020) 425–454 [KB:zhang2020-optimality-based-domain-reduction-for]. Gradient-sign (KKT) exclusion is implemented in BARON. Time falls by 14–25% on unconstrained and one-constraint problems, with about 0% effect on multi-constraint problems.

**Missing theory.** There is no result on the strength of marginals-based reduction compared with full OBBT, in either direction. There is also no analysis of OBDR in terms of convergence order. OBDR removes neighborhoods of non-stationary boundary regions, so it could plausibly affect clustering at non-KKT boundary points.

---

## B. Spatial branching

### B1. Choosing the branching variable and point

**State of the art.**
- Belotti, Lee, Liberti, Margot, Wächter, *Optim. Methods Softw.* 24 (2009) [KB:belotti2009-branching-and-bounds-tightening-techniques].
  - Couenne uses a scaled violation `|x̄_i − θ_i(x̄)|/(1 + ‖∇θ_i‖)`, violation transfer, reliability pseudocosts extended to continuous variables, and strong branching.
  - The comparison identifies no universally dominant branching rule. Full strong branching spends 90–95% of time in its LPs on the `spar-*` instances.
- Tawarmalani & Sahinidis (2004) introduced violation transfer.
- SCIP 8 combines violation scores with pseudocosts, and optionally domain width and fractionality. Its branching point is a convex combination of the LP value and the interval midpoint. Speakman–Lee tabulate the defaults: SCIP uses (α, β) = (1, 0.2) and Couenne (0.25, 0.2). SCIP branches on original variables only by default.
- Speakman & Lee, "On branching-point selection for trilinear monomials in spatial B&B: the hull relaxation", *J. Glob. Optim.* 72 (2018), arXiv:1706.08438 [KB:speakman2018-on-branching-point-selection-for].
  - Minimizing the total child hull volume, the midpoint is optimal for x₂ and x₃, and the optimal x₁ point lies left of the midpoint.
  - Future work: multiple terms and double-McCormick relaxations.
  - Follow-ups compute volumes only: Speakman & Averkov (*Discrete Appl. Math.* 2022); Makhoul & Speakman, arXiv:2512.13964 (2025), which covers general boxes.
- Dey, Santana, Wang, *Optim. Eng.* 20 (2019) [KB:dey2019-new-socp-relaxation-and-branching]: hyperbola and parabola branching for bipartite bilinear programs.
- Dey, Han, Wang, "Extreme strong branching for QCQPs", arXiv:2510.20650 (Oct 2025).
  - Evaluates several points per variable and chooses the variable and point jointly, with bound tightening from infeasible probes.
  - Beats Gurobi 12, BARON, and Couenne on bipartite bilinear and model-updating QCQPs.
  - There are **no theorems**. Stated future work: a variant that incorporates reliability and an explanation of the method's particularly good performance on BBP.
- Chen, Atamtürk, Oren, *Math. Program.* 165 (2017) [KB:chen2016-a-spatial-branch-and-cut]: complex QCQP with rank-one-violation branching. Violation-based rules produced smaller trees than a reliability rule.
- Hübner, Gupte, Rebennack, *INFORMS J. Comput.* 38(2) (2026) [KB:hubner2026-spatial-branch-and-bound-for]: separable piecewise-linear sBB. Breakpoint branching terminates finitely. Largest-error branching converges only in the limit, and no general convergence theorem is given for the discontinuous case.

**Missing theory.**
- **No tree-size guarantee is known for any spatial branching rule.** This includes violation, pseudocost, strong, extreme strong, and volume rules.
- The MILP analogues exist:
  - Dey, Dubey, Molinaro, Shah, "A theoretical and computational analysis of full strong-branching", *Math. Program.* 205 (2024) 303–336, arXiv:2110.10754.
  - Cheng & Basu, "Theoretical challenges in learning for branch-and-cut", arXiv:2601.23249 (2026): local-score rules can produce trees exponentially larger than optimal, and even tiny differences in scores can lead to exponentially different tree sizes.
  - Abstract branching models: Le Bodic & Nemhauser, *Math. Program.* (2017); Anderson, Le Bodic, Morgan, *Math. Program.* 190 (2021); a stochastic lookahead model (2024); Jiang, arXiv:2607.06343 (2026).
- None has a **spatial** version. In spatial branching, gains shrink with box width according to the relaxation's convergence order (gap ≈ τ·w^β), and the split point is continuous. I found no abstract model of that kind.

### B2. Convergence order and the cluster problem

**State of the art.**
- Du & Kearfott, *J. Glob. Optim.* 5 (1994).
- Neumaier, *Acta Numerica* 13 (2004) [KB:neumaier2004-complete-search-in-continuous-global]. Exclusion regions: Schichl, Markót, Neumaier, *J. Glob. Optim.* 59 (2014).
- Wechsung, Schaber, Barton, "The cluster problem revisited", *J. Glob. Optim.* 58 (2014), https://doi.org/10.1007/s10898-013-0059-9. In the unconstrained case, at least second-order convergence is needed to remove the exponential dependence on the tolerance.
- Pointwise convergence order of relaxations: Bompadre & Mitsos, *J. Glob. Optim.* 52 (2012), for McCormick; Najman & Mitsos, *J. Glob. Optim.* 66 (2016), for multivariate McCormick.
- Kannan & Barton, "The cluster problem in constrained global optimization", *J. Glob. Optim.* 69 (2017) 629–676, https://doi.org/10.1007/s10898-017-0531-z.
  - First-order schemes suffice if the objective or the constraint violation grows linearly and the prefactors are small.
  - Second order is required at non-isolated, equality-constrained minimizers.
  - The conclusion states no open problems.
- Kannan & Barton, "Convergence-order analysis of branch-and-bound algorithms for constrained problems", *J. Glob. Optim.* 71 (2018) 753–813 (PDF: https://rohitkannan.github.io/PDFs/papers/KannanBarton_JOGO_ConvergenceOrder.pdf). The conclusion identifies three directions for further work (summarized):
  - (i) whether full-space bounds can converge at second order throughout a neighborhood of constrained minimizers that satisfy the KKT conditions;
  - (ii) the orders attained by additional reduced-space schemes, including [32] [Stuber, Scott, Barton, implicit-function relaxations, *Optim. Methods Softw.* 30 (2015)];
  - (iii) propagation conditions sufficient for second-order reduced-space bounds at constrained minimizers under suitable regularity assumptions.
- Later extensions: a 2024 *J. Glob. Optim.* paper on the convergence order of value-function relaxations in decomposition for stochastic programs (https://doi.org/10.1007/s10898-024-01458-1); Song & Khan (*Math. Program.* 2021) on ODE relaxations with second-order pointwise convergence.

**In-house coverage.**
- (i) is bypassed. The cluster-free note bounds the count at a fixed scale without neighborhood second order. It attributes the key growth inequality to Anitescu (2005) and Bonnans–Shapiro (2000).
- (iii) is partly addressed by Theorem 3 (width-tight reduction, such as interval Newton on equality-determined variables). Anchoring-type reduction without width control is open.
- (ii) is not addressed.

**Missing theory.**
- **Lower bounds in ε.** The whole cluster literature gives upper and heuristic covering estimates. The in-house screen notes that "no lower bounds on node counts exist in this literature". No theorem shows that a first-order scheme **must** visit Ω(ε^{−c·n}) nodes on a natural class. The in-house exponential results are in n at fixed ε, not in ε.
- **Convergence order with OBBT or FBBT.** No theorem gives OBBT's effect on convergence order in quantitative form. Kannan–Barton (2018) show only by example (Examples 16–18) that propagation raises the order. They also note that FBBT does not raise the order for `−xy`, `x + y ≤ 1`.

### B3. Tree-size lower bounds and complexity of spatial B&B

- Dey, Dubey, Molinaro, "Lower bounds on the size of general branch-and-bound trees", *Math. Program.* 198 (2023), arXiv:2103.09807 [KB:dey2023-lower-bounds-on-the-size]. Cross-polytope, perturbed, and TSP families, with arbitrary integer split disjunctions.
- Dey & Shah, *Oper. Res. Lett.* 50 (2022) [KB:dey2022-lower-bound-on-size-of]: lot sizing.
- Jarre (2018) [KB:jarre2018-best-case-exponential-running-time]: exponential B&B even with an optimal SDP bound.
- In-house: seven `2^Ω(n)` spatial lower bounds, with the affine-branching barrier.
- I found no 2021–2026 external paper proving lower bounds for **continuous** spatial B&B. The in-house novelty notes reached the same conclusion. The in-house results appear to be ahead of the published literature here.

**Open.** Lower bounds when branching on arbitrary affine hyperplanes (a continuous analogue of general splits), or on eigen-directions. See the in-house barrier note.

### B4. Non-axis-aligned, eigen, and polytopal branching

- Nohra, Raghunathan, Sahinidis, "Spectral relaxations and branching strategies for global optimization of MIQPs", arXiv:2010.04822 (*SIAM J. Optim.* 2021). Uses eigenvalue-based variable selection, implemented in BARON.
- Lu et al., eigen-decomposition B&B for nonconvex QPs with convex quadratic constraints, *J. Glob. Optim.* (2017), https://doi.org/10.1007/s10898-016-0436-2. Branches along eigendirections of negative eigenvalues.
- Casado, G.-Tóth, Hendrix, Messine, "Polytopal spatial branch and bound", *Informatica* 36(4) (2025) [KB:casado2025-polytopal-spatial-branch-and-bound]. Performs well when optima lie on low-dimensional faces. It gives no complexity bound.
- Mahajan & Ralphs (2009) studied general disjunctions for MILP.

**Missing theory.** No result gives separation, meaning a family where affine or eigen branching is provably exponentially smaller than coordinate branching, or the reverse. The in-house barrier note shows the XOR/moment argument fails. This makes it the natural next question.

### B5. Learned spatial branching (2021–2026)

- Ghaddar, Gómez-Casares, González-Díaz, González-Rodríguez, Pateiro-López, Rodríguez-Ballesteros, "Learning for spatial branching: an algorithm selection approach", *INFORMS J. Comput.* 35(5) (2023), arXiv:2204.10834 [KB:ghaddar2023-learning-for-spatial-branching-an].
  - Static rule selection with quantile-regression forests in RAPOSa improves pace by 9–25%.
  - Future work: dynamic node features, richer portfolios, online learning.
- González-Rodríguez, Gómez-Casares, Ghaddar, González-Díaz, Pateiro-López, "Learning in RLT-based spatial branching: limitations of strong branching imitation", *INFORMS J. Comput.* (2025), arXiv:2406.03626 [KB:rodriguez2025-learning-in-reformulation-linearization-technique]. Per-node experts are "myopic" and do not beat the best static rule.
- Berthold & Geis, "Learning to choose branching rules for nonconvex MINLPs", CPAIOR 2026, arXiv:2602.09996 [KB:berthold2026-learning-to-choose-branching-rules]. Chooses between PreferInt and Mixed in Xpress, for about an 8% speedup.
- Kannan, Nagarajan, Deka (IJOC 2025): learned partitioning points.
- Barros-González et al., arXiv:2606.21483 [KB:gonzalez2026-a-note-on-the-convergence]: a missing strict-width assumption in the standard RLT redundancy claim.

**Missing theory.** Cheng–Basu (2026) formalize why local expert scores can mislead in MILP. The RLT myopia result of González-Rodríguez et al. is its empirical counterpart in spatial branching. **No formal spatial analogue exists.**

---

## Ranked open theoretical questions (with in-house overlap)

1. **Iterated-OBBT fixed point: convergence rate, finiteness, complexity, and gap to the true box hull.**
   - Sources: Caprara–Locatelli–Monaci 2016; Puranik–Sahinidis 2017; Alpine and power-systems practice.
   - Unsolved: ≈75%.
   - In-house: FBBT analogues only; OBBT is candidate-directions item 13, not started.
2. **Abstract or tree-size theory for spatial branching variable and point selection with width-dependent gains**, including strong and extreme strong branching compared with violation branching.
   - Sources: Dey–Han–Wang 2025 future work; Speakman–Lee 2018; Belotti et al. 2009 ("no rule dominates"); MILP analogues (Dey et al. 2024; Cheng–Basu 2026; Le Bodic–Nemhauser).
   - Unsolved: ≈80%.
   - In-house: not touched.
3. **Sufficient conditions on constraint propagation (FBBT/OBBT) for second-order convergence of reduced-space schemes**, and the convergence order of the implicit-function relaxations of Stuber–Scott–Barton.
   - Source: Kannan–Barton 2018, conclusion items (ii) and (iii).
   - Unsolved: ≈65% for the general question.
   - In-house: partly addressed (Theorem 3 with width-tight reduction; anchoring left open).
4. **ε-dependent lower bounds for the cluster problem**: prove that first-order schemes need Ω(ε^{−c·n}) nodes on natural instances.
   - Sources: Du–Kearfott; Wechsung et al.; Kannan–Barton, all of which give upper or heuristic counts only.
   - Unsolved: ≈65%.
   - In-house: lower bounds exist only in n at fixed ε.
5. **Affine or eigen-direction branching: an exponential lower bound, or a separation from coordinate branching**, in the continuous setting.
   - Sources: Dey–Dubey–Molinaro 2023 (a MILP analogue); Nohra et al. 2021 and Lu et al. 2017 (practice only).
   - Unsolved: ≈70%.
   - In-house: the barrier note shows the current proof fails.
