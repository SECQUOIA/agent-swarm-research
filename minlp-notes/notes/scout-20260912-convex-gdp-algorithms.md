# Scout: algorithmic directions for convex MINLP and convex GDP solution methods (2026-09-12)

Status: exploratory scout, not a result. Web novelty checks were run for every
candidate; an unsuccessful search does not establish novelty. Scores are
1–10 for importance (I), feasibility in Python within days (F), and novelty
confidence (N).

## Scope and repository overlap

Target: decomposition, cutting-plane, OA/ESH, master-problem and
NLP-subproblem methods for convex MINLP and convex GDP, implementable in
Pyomo with Gurobi 13, GAMS 54 (BARON, SCIP, DICOPT, SBB, CONOPT, IPOPT,
KNITRO) and testable on the MINLPLib convex subset and GDPlib.

Repository check (`grep -ril` over `notes/` and `results/` for outer
approximation, ESH, hull relaxation, P-split, MindtPy, GDPopt, LP/NLP,
branch-and-cut, lift-and-project, cut selection, Lagrangean, basic steps):
the repository has no completed work on solution algorithms for convex
MINLP/GDP. Related but distinct entries:

- [`candidate-directions-2026-09-05.md`](candidate-directions-2026-09-05.md)
  item 2 (OA versus NLP-B&B exponential separation), item 8 (Hausdorff order
  of big-M versus hull under bound tightening), item 9 (NP-hardness of
  choosing bound-improving basic steps). None started.
- [`open-problems-from-literature.md`](open-problems-from-literature.md)
  item 4 (when does the big-M relaxation equal the hull relaxation; open),
  item 5 (P-split behaviour under weak bounds; open), item 30 (a priori OA
  versus B&B criterion; open).
- [`common-factor-p-split-balls.md`](common-factor-p-split-balls.md) and
  [`common-factor-p-split-rotation-gap.md`](common-factor-p-split-rotation-gap.md):
  P-split relaxation theory, not algorithms.
- [`research-20260912-algorithm-opportunities.md`](research-20260912-algorithm-opportunities.md):
  conflict-driven convex aggregation for nonconvex MIQCQP; it rejected
  certified inexact OA/Benders cuts as insufficiently distinct from prior work.

The user's own arXiv:2508.16093 (Gusev and Bernal Neira, exact hull
reformulation for quadratically constrained GDP) is the natural anchor for
candidates A, B and F below.

## Baseline software facts used below

- GDPopt (Pyomo) offers LOA, GLOA, LBB, RIC and LD-SDA; the discrete problem
  uses `discrete_problem_transformation` (default `gdp.bigm`, hull allowed);
  OA cuts are added inside disjuncts with slacks; no ESH, single-tree or
  regularization option exists
  ([GDPopt docs](https://pyomo.readthedocs.io/en/stable/explanation/solvers/gdpopt.html),
  [config source](https://raw.githubusercontent.com/Pyomo/pyomo/main/pyomo/contrib/gdpopt/config_options.py)).
- MindtPy offers OA, ECP, LP/NLP-B&B (single tree via `gurobi_persistent`
  or `cplex_persistent` lazy callbacks), GOA, ROA (level and Lagrangian
  regularizations), FP, solution pools, no-good cuts and `quadratic_strategy`
  ([MindtPy docs](https://pyomo.readthedocs.io/en/stable/explanation/solvers/mindtpy.html)).
- Pyomo.GDP transformations: `gdp.bigm`, `gdp.mbigm`, `gdp.hull`,
  `gdp.cuttingplane` (experimental, linear GDP only)
  ([Pyomo.GDP solving docs](https://pyomo.readthedocs.io/en/stable/explanation/modeling/gdp/solving.html)).
- Gurobi 13 (Nov 2025) solves MINLP with general nonlinear constraints by
  spatial branch-and-bound with dynamically refined linear outer
  approximations; it reports over 2x speedups on MINLP relative to 12.0 and
  no convex-specific pathway is documented
  ([release note](https://www.gurobi.com/news/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities/),
  [MINLP FAQ](https://www.gurobi.com/resources/faq/minlp-faq-practical-mixed-integer-nonlinear-modeling)).
- Independent MINLPLib benchmark of BARON, Gurobi, LINDO, SCIP, SHOT and
  XPRESS, February 2026 ([Mittelmann](https://plato.asu.edu/ftp/minlp.html)).
- GDPlib exposes about 40 GDP models (batch_processing, jobshop, cstr,
  biofuel, kaibel, methanol, mod_hens, modprodnet, stranded_gas, syngas,
  water_network, and others) through `build_model` functions
  ([GDPlib](https://github.com/SECQUOIA/gdplib)).

## Notation

Convex GDP:

```
min  f(x) + sum_i c_i
s.t. h(x) <= 0
     OR_{k in K_i} [ Y_ik ; g_ik(x) <= 0 ; c_i = gamma_ik ]   for i in I
     Omega(Y) = True,   x^L <= x <= x^U
```

with f, h, g_ik convex and differentiable. Hull relaxation of disjunction i:
`x = sum_k nu_ik`, `sum_k lambda_ik = 1`, `lambda_ik x^L <= nu_ik <= lambda_ik x^U`,
`cl(lambda_ik g_ik(nu_ik / lambda_ik)) <= 0`. An affine inequality
`a^T x <= b` inside disjunct (i,k) hull-transforms exactly to
`a^T nu_ik <= b lambda_ik` (no epsilon approximation).

## Candidates

### A. Logic-based extended supporting hyperplane (LB-ESH)

**Idea.** Replace LOA's NLP-generated linearizations by ESH supporting
hyperplanes generated per disjunct in the original x-space. Once per
disjunct compute a strict interior point `xbar_ik` (solve
`min t s.t. g_ik(x) <= t, x in box`; skip disjuncts with only linear
constraints). Master: linear GDP (hull or big-M transformed) with
per-disjunct cuts. Each iteration: solve the master (LP relaxation first,
then MILP, as in ESH). Read the disaggregated point
`p_ik = nu_ik / lambda_ik` for `lambda_ik > 0` (hull master) or
`p_ik = x_hat` (big-M master). If `max_j g_ikj(p_ik) > 0`, bisection on
`[xbar_ik, p_ik]` gives a boundary point `z_ik` with
`max_j g_ikj(z_ik) = 0`; for each active j add

```
g_ikj(z_ik) + grad g_ikj(z_ik)^T (x - z_ik) <= 0     inside disjunct (i,k),
```

which is a supporting hyperplane of the disjunct and transforms exactly to
`grad g^T nu_ik + (g(z) - grad g^T z) lambda_ik <= 0`. Global constraints
`h` use standard ESH with a global interior point. Reduced NLP subproblems
(only active disjuncts, as in LOA) are used for incumbents, not for cuts.
Convergence: polyhedral outer approximations of each compact convex disjunct
converge, so the hull of the linearized disjunction converges to the hull of
the disjunction; the ESH argument then applies to the master sequence.

**Bottleneck addressed.** LOA needs one NLP per linearization point and a
set-covering initialization of `max_i |K_i|` NLPs before the first useful
master; cuts sit at NLP optima, not where the master relaxation is weak.
Running plain ESH on the hull-reformulated MINLP requires gradients of
perspective functions `lambda g(nu/lambda)`, which are singular at
`lambda = 0` and force an epsilon approximation (the defect that
arXiv:2508.16093 removes for quadratic constraints); LB-ESH does the line
search in x-space and the exact affine perspective, so no epsilon appears.

**Closest prior work.**
- Kronqvist, Lundell, Westerlund (2016), ESH for convex MINLP, J. Global
  Optim. ([link](https://link.springer.com/article/10.1007/s10898-015-0322-3));
  no disjunctive structure.
- Lundell, Kronqvist, Westerlund (2022), SHOT, J. Global Optim.
  ([link](https://link.springer.com/article/10.1007/s10898-022-01128-0));
  ESH/ECP with single-tree, no GDP input.
- Kronqvist and Misener (2021), disjunctive cut strengthening for convex
  MINLP, Optim. Eng. ([Optimization Online](https://optimization-online.org/2020/08/7957/));
  strengthens an ESH cut's right-hand side per term of an integer-variable
  disjunction; does not generate cuts per disjunct from disjunct interior
  points.
- Türkay and Grossmann (1996), LOA
  ([link](https://www.sciencedirect.com/science/article/abs/pii/0098135495002197));
  Nguyen and Pulsipher (2026) generalize LOA, cutting planes, P-split and
  multiple big-M to infinite-dimensional GDP, not ESH
  ([arXiv:2608.27707](https://arxiv.org/abs/2608.27707)).
- Three targeted searches found no ESH variant for GDP.

**Risk already known.** Moderate-low. The construction is simple enough that
Lundell or Kronqvist may have tried it informally; nothing published found.

**Effort.** 3–5 days for a GDPopt-style prototype (reuse GDPopt's subproblem
and discrete-problem utilities); 1–2 weeks for benchmarks. Compare with
GDPopt LOA/LBB, MindtPy OA and LP/NLP on the big-M and hull MINLPs, SHOT (if
available through GAMS), DICOPT, SBB, BARON, SCIP, Gurobi 13 native.

**Scores.** I 7, F 8, N 7.

### B. Single-tree logic-based branch-and-cut (LP/NLP-based LOA)

**Idea.** One Gurobi branch-and-cut tree over the linearized GDP master
(hull or big-M). Lazy-constraint callback at integer-feasible nodes: fix
the Boolean assignment, solve the reduced NLP with only active disjuncts,
add OA cuts inside the active disjuncts (hull-transformed exactly, or
big-M with M computed over the other disjuncts' relaxations), update the
incumbent; on infeasible reduced NLP, add cuts from the feasibility NLP plus
a no-good cut on the Boolean vector. User-cut callback at fractional nodes:
LB-ESH cuts from candidate A (globally valid, so safe as user cuts).
Branching priorities on indicator variables of disjunctions with largest
`lambda` fractionality, following the LBB rule. Regularization of the
incumbent search (candidate G) is an optional add-on.

**Bottleneck addressed.** Multi-tree LOA re-solves a growing MILP from
scratch each iteration. LP/NLP-B&B is the standard remedy in convex MINLP
(MindtPy, SHOT, BONMIN B-QG), but GDPopt has no single-tree strategy, so
GDP users lose either the reduced-space NLPs (if they go through MindtPy on
the MINLP reformulation) or the single tree (if they use GDPopt).

**Closest prior work.**
- Quesada and Grossmann (1992), LP/NLP-B&B
  ([link](https://www.sciencedirect.com/science/article/abs/pii/0098135492800288)).
- Bernal, Peng, Kronqvist, Grossmann (2022), regularized single-tree OA in
  MindtPy ([link](https://link.springer.com/article/10.1007/s10898-022-01178-4)).
- Lee and Grossmann (2000), logic-based B&B with disjunctive branching
  ([link](https://www.sciencedirect.com/science/article/abs/pii/S0098135400005810)).
- GDPopt strategies LOA, GLOA, LBB, RIC, LD-SDA
  ([docs](https://pyomo.readthedocs.io/en/stable/explanation/solvers/gdpopt.html));
  LD-SDA: Ovalle, Liñán, Lee, Gómez, Ricardez-Sandoval, Grossmann, Bernal
  Neira (2024/2025) ([arXiv:2405.05358](https://arxiv.org/abs/2405.05358)).
- Searches for "single-tree" or "branch-and-cut" logic-based OA found
  nothing.

**Risk already known.** Medium. It is a natural extension and Bernal
Neira's group maintains both MindtPy and GDPopt; check open Pyomo pull
requests and issues before starting. Publication value comes mainly from
the combination with A (cheap valid user cuts at fractional nodes) and
from a careful benchmark rather than from the single tree alone.

**Effort.** 3–6 days (adapt MindtPy's `gurobi_persistent` callback code to
GDPopt's subproblem machinery).

**Scores.** I 7, F 8, N 5.

### C. LP-based K-term disjunctive cuts from outer-approximated disjuncts

**Idea.** For disjunction i keep polyhedral outer approximations
`P_ik = {x : A_ik x <= b_ik} ∩ box` (accumulated OA/ESH cuts). Given a
master relaxation point `x_hat`, solve Balas's cut-generating LP over the
K-term disjunction `OR_k P_ik`:

```
max  alpha^T x_hat - beta
s.t. alpha = A_ik^T u_k,  beta >= b_ik^T u_k,  u_k >= 0   for all k
     normalization (e.g. sum_k ||u_k||_1 = 1)
```

The cut `alpha^T x <= beta` is valid for `conv(union_k P_ik)`, hence for
the disjunction, and lives in x-space with no disaggregated variables. If
the CGLP violation is small, refine: for the disjunct k with largest
`u_k`, add an OA cut at the Euclidean projection of `x_hat` onto
`{g_ik <= 0}` (one small NLP over a single disjunct) and repeat; in the limit
the cut is as strong as the nonlinear CGLP cut of Stubbs–Mehrotra /
Ceria–Soares, which coincides with Trespalacios–Grossmann's hull cut. The
same LP with `K_i K_j` terms over `P_ik ∩ P_jl` gives cuts from the
intersection of two disjunctions, a polyhedral emulation of a basic step
for separation only, without DNF blow-up of the master. Lifting the cut to
`(x, lambda)` with per-term right-hand sides recovers Kronqvist–Misener
type-2 cuts as a special case.

**Bottleneck addressed.** Hull cuts of Trespalacios–Grossmann need an NLP
over the full hull relaxation (all disaggregated variables) and are used
only at the root; here separation is an LP in x-space usable at every node
of a branch-and-cut, and basic-step strength is obtained locally per pair.

**Closest prior work.**
- Sawaya and Grossmann (2005), cutting planes for linear GDP by projection
  onto the hull relaxation (Comput. Chem. Eng. 29, 1891–1913; implemented
  as Pyomo `gdp.cuttingplane`, linear only,
  [docs](https://pyomo.readthedocs.io/en/stable/explanation/modeling/gdp/solving.html)).
- Trespalacios and Grossmann (2016), cutting-plane algorithm for convex
  GDP with basic steps, INFORMS J. Comput. 28(2)
  ([KiltHub](https://kilthub.cmu.edu/articles/journal_contribution/Cutting_planes_algorithm_for_convex_Generalized_Disjunctive_Programs/6466871));
  nonlinear separation, root only.
- Kılınç, Linderoth, Luedtke (2017), lift-and-project cuts for convex
  MINLP via iterated LP CGLPs, Math. Prog. Comput. 9
  ([link](https://link.springer.com/article/10.1007/s12532-017-0118-1));
  two-term split disjunctions on integer variables only.
- Stubbs and Mehrotra (1999)
  ([link](https://link.springer.com/article/10.1007/s101070050103)) and
  Ceria and Soares (1999)
  ([link](https://link.springer.com/article/10.1007/s101070050106)):
  nonlinear CGLP for convex disjunctions.
- Kronqvist and Misener (2021), right-hand-side strengthening only
  ([Optimization Online](https://optimization-online.org/2020/08/7957/)).
- Lodi, Tanneau, Vielma (2023), disjunctive cuts in mixed-integer conic
  optimization ([arXiv:1912.03166](https://arxiv.org/abs/1912.03166)); split
  disjunctions.

**Risk already known.** Medium. The pieces are classical; the combination
(K-term logical disjunctions, OA refinement, pairwise basic-step
emulation, in-tree use) was not found. Reviewers may view it as
incremental over Kılınç et al. unless the pairwise cuts show clear gains.

**Effort.** 4–7 days; the CGLP size is `sum_k m_ik` multipliers, small on
GDPlib instances. Normalization choice matters (Balas–Perregaard).

**Scores.** I 6, F 7, N 6.

### D. Dual-certified adaptive hybrid formulation (per-disjunction big-M / hull / P-split)

**Idea.** Start with big-M (or P-split) for every disjunction. Solve the
continuous relaxation with optimal multipliers `pi`. For each disjunction i,
a guaranteed lower bound on the relaxation value after upgrading only
disjunction i to its hull is

```
z_i^LB = min { f(x) + pi^T r(x) : x in hull_i ∩ box },
```

where `r(x) <= 0` collects all other relaxed constraints (fixed
multipliers, Lagrangian relaxation), a single small convex program over one
disjunction's hull. `z_i^LB - z(BM)` is a certified gain (it can be
negative, in which case no claim is made). Upgrade disjunctions whose
certified gain per added variable exceeds a threshold, re-solve, repeat;
optionally use P-split as the intermediate rung. Theory: `z_i^LB = z(BM)`
for the optimal multipliers of the big-M relaxation is a sufficient
condition for no gain, which gives a checkable partial answer to the open
question of when big-M and hull relaxations coincide (repository open
problem 4, from Vecchietti–Lee–Grossmann 2003). Within LOA the choice is
made once and inherited by every OA cut (hull disaggregates each cut K
times, so the size saving compounds).

**Bottleneck addressed.** Uniform hull bloats LOA masters; uniform big-M
is weak; P-split is uniform by construction. No published rule selects per
disjunction with a certified bound.

**Closest prior work.**
- Vecchietti, Lee, Grossmann (2003), characterization of disjunction
  relaxations ([link](https://www.sciencedirect.com/science/article/abs/pii/S009813540200220X));
  qualitative guidelines.
- Trespalacios and Grossmann (2015), improved big-M
  ([ResearchGate](https://www.researchgate.net/publication/273579739_Improved_Big-M_reformulation_for_generalized_disjunctive_programs)).
- Kronqvist, Misener, Tsay (2021/2025), Between steps and P-split
  ([arXiv:2101.12708](https://arxiv.org/abs/2101.12708),
  [Math. Prog.](https://link.springer.com/article/10.1007/s10107-025-02232-1)).
- Papageorgiou and Trespalacios (2018), pseudo basic steps: Lagrangian
  decomposition multipliers bound the gain of basic steps
  ([arXiv:2501.15345](https://arxiv.org/abs/2501.15345)); the same tool is
  not applied to the big-M-versus-hull decision.
- Lee and Bernal Neira (2026), reaggregated hull for special structures
  ([arXiv:2601.11782](https://arxiv.org/abs/2601.11782)); structural, not
  adaptive.
- Pyomo `gdp.mbigm` computes tight M values by subproblems, no hull choice.

**Risk already known.** Medium-low for the certified-gain rule; the
"strong-branching" exact variant (solve |I| relaxations) is obvious and
should be the baseline, not the contribution.

**Effort.** 2–4 days for the rule and the LOA integration; theory 1–2 days.

**Scores.** I 6, F 8, N 6.

### E. Multiplier-guided pseudo-basic-step selection delivered as Lagrangian cuts

**Idea.** Papageorgiou and Trespalacios evaluate pseudo basic steps for
all pairs of disjunctions, strong-branching style, and state that
heuristics for choosing pairs are needed. Proposal: rank pairs (i,j) by a
cheap proxy (multiplier-weighted overlap of shared variables times
indicator fractionality in the current relaxation), evaluate only the top
m pairs, and add the resulting bound `L_ij` as the Lagrangian cut
`lambda_i^T v_i + lambda_j^T v_j >= L_ij` to the hull master instead of
performing the basic step (which multiplies disjunct counts). Update
multipliers as the master relaxation changes.

**Bottleneck addressed.** Basic steps are the only known way to go beyond
hull strength, but DNF growth and pair selection make them impractical;
cuts avoid the growth and the proxy avoids the quadratic evaluation.

**Closest prior work.** Papageorgiou and Trespalacios (2018), EURO J.
Comput. Optim. 6, 55–83 ([arXiv:2501.15345](https://arxiv.org/abs/2501.15345));
Trespalacios and Grossmann (2016) basic-step rules (above); Ruiz and
Grossmann (2012) hierarchy of relaxations
([link](https://www.sciencedirect.com/science/article/abs/pii/S037722171100899X)).

**Risk already known.** Medium. The Lagrangian-cut delivery may be implicit
in Papageorgiou–Trespalacios's "techniques to exploit this information";
read their Section on MINLP use before investing.

**Effort.** 3–5 days. Test on k-means and strip-packing/jobshop GDPs where
basic steps are known to matter.

**Scores.** I 5, F 7, N 5.

### F. Conic-master LOA for quadratically constrained GDP (CEHR in the master)

**Idea.** Keep the exact conic hull (CEHR, rotated second-order cones) of
every convex quadratic disjunct constraint inside the master, which Gurobi
13 solves as an MISOCP; apply OA or LB-ESH cuts only to non-quadratic
convex constraints; reduced NLPs for incumbents. Variants: (i) MISOCP
master with lazy OA cuts in a single tree (with B); (ii) polyhedral
K*-cut outer approximation of the same cones, Pajarito style, to test
whether native SOC or refined polyhedra win inside a decomposition.

**Bottleneck addressed.** Linearizing rotated cones in hull space needs
many cuts and suffers at `lambda = 0`; MindtPy's `quadratic_strategy`
passes quadratics to the master for MINLP but has no GDP counterpart, and
Bernal–Grossmann's conic GDP study used direct MICP solvers, not
decomposition.

**Closest prior work.**
- Bernal Neira and Grossmann (2022/2024), conic GDP
  ([arXiv:2109.09657](https://arxiv.org/abs/2109.09657)).
- Gusev and Bernal Neira (2025), exact hull reformulation for QC-GDP
  ([arXiv:2508.16093](https://arxiv.org/abs/2508.16093)).
- Coey, Lubin, Vielma (2020), Pajarito conic OA
  ([arXiv:1808.05290](https://arxiv.org/abs/1808.05290)).
- Dai (2026), polyhedral OA for MISOCP: angular cut selection and
  progressive integrality ([arXiv:2608.10055](https://arxiv.org/abs/2608.10055)).
- MindtPy `quadratic_strategy`
  ([docs](https://pyomo.readthedocs.io/en/stable/explanation/solvers/mindtpy.html)).

**Risk already known.** Medium-low as a decomposition study; low as a
formulation study (already done). Contribution is algorithmic only if the
decomposition beats direct MISOCP/MINLP solves on constrained layout,
k-means and CSTR-network instances.

**Effort.** 2–4 days; the user already owns the CEHR code.

**Scores.** I 5, F 9, N 5.

### G. Regularized LOA (level or Lagrangian regularization with reduced NLPs)

**Idea.** Port MindtPy's ROA projection problem (level sets, `grad_lag`,
`hess_lag`) to the LOA master so that the next Boolean assignment is
chosen near the last reduced-NLP solution, keeping reduced-space NLPs.

**Closest prior work.** Kronqvist, Bernal, Grossmann (2020)
([link](https://link.springer.com/article/10.1007/s10107-018-1356-3));
Bernal et al. (2022) ([link](https://link.springer.com/article/10.1007/s10898-022-01178-4)).
No GDP version found, but the extension is direct and the group that owns
both codes is the most likely to have it in progress.

**Scores.** I 5, F 8, N 3. Not recommended standalone; useful as an add-on
to A or B.

## Ideas considered and discarded as known

- Cut-specific tight M for OA cuts inside big-M masters: this is the
  per-term right-hand-side strengthening of Kronqvist and Misener (2021)
  and the multiple big-M of Trespalacios and Grossmann (2015).
- Analytic-center or central linearization points: center-cut algorithm of
  Kronqvist, Lundell, Westerlund (2017/2018)
  ([Optimization Online](https://optimization-online.org/2018/02/6456/)).
- Cut selection by angular novelty and progressive integrality of the
  master: Dai (2026), arXiv:2608.10055.
- Nonsmooth OA with KKT-subgradient cuts: Wei, Liu, Zeng (2026),
  [arXiv:2602.04122](https://arxiv.org/abs/2602.04122).
- Warm-starting cuts across parameterized instances: Tamm, Eichfelder,
  Kronqvist (2025), [arXiv:2507.08595](https://arxiv.org/abs/2507.08595).
- Early-terminated NLP subproblems with valid bounds: Leyffer (2001), and
  the repository already rejected certified inexact cuts.
- MIQP masters with Hessian information and Benders trust regions:
  Ghezzi, Van Roy, Sager, Diehl (2024), S-B-MIQP in CAMINO
  ([arXiv:2404.11786](https://arxiv.org/abs/2404.11786)).
- Hull cuts by nonlinear separation with basic steps: Trespalacios and
  Grossmann (2016).
- Separable OA cut disaggregation, solution pools, feasibility pump,
  regularized OA, lift-and-project OA, P-split, conic GDP, ESH: excluded
  by the task statement.

## Recommendation

1. **A (LB-ESH)** first: highest novelty confidence among the feasible
   items, a clean theoretical story (exact affine perspective, no epsilon,
   convergence inherited from ESH), and a direct link to the user's CEHR
   paper. Deliverable: GDPopt-style prototype and a benchmark against LOA,
   MindtPy OA/LP-NLP on big-M and hull MINLPs, SHOT (if available in GAMS
   54), DICOPT, SBB, BARON, SCIP, Gurobi 13 native, on GDPlib convex
   instances (batch_processing, jobshop, cstr, stranded_gas, modprodnet,
   constrained layout, k-means, process synthesis) and the GDP-derived
   MINLPLib convex instances (clay*, syn*, procsel, enpro*, batch*).
2. **B (single-tree LB-B&C)** second, implemented on the same code base
   so that A's cuts serve as user cuts; check Pyomo pull requests first.
3. **D (dual-certified hybrid formulation)** third: cheap, self-contained,
   with a theoretical corollary on big-M-versus-hull equality that touches
   an open item already recorded in this repository.

C is a good fourth if time allows; E and F are lower-risk continuations
that depend on reading Papageorgiou–Trespalacios in full (E) or on the
decomposition beating direct MISOCP solves (F). G only as an add-on.

## Sources

- Kronqvist, Lundell, Westerlund (2016), ESH: https://link.springer.com/article/10.1007/s10898-015-0322-3
- Lundell, Kronqvist, Westerlund (2022), SHOT: https://link.springer.com/article/10.1007/s10898-022-01128-0
- Kronqvist, Misener (2021), disjunctive cut strengthening: https://optimization-online.org/2020/08/7957/
- Kronqvist, Lundell, Westerlund, center-cut: https://optimization-online.org/2018/02/6456/
- Kronqvist, Bernal, Grossmann (2020), regularized OA: https://link.springer.com/article/10.1007/s10107-018-1356-3
- Bernal, Peng, Kronqvist, Grossmann (2022), alternative regularizations: https://link.springer.com/article/10.1007/s10898-022-01178-4
- Kronqvist, Bernal Neira, Grossmann (2025), 50 years of MINLP and GDP: https://www.sciencedirect.com/science/article/pii/S0377221725005417
- Türkay, Grossmann (1996), LOA: https://www.sciencedirect.com/science/article/abs/pii/0098135495002197
- Lee, Grossmann (2000), LBB: https://www.sciencedirect.com/science/article/abs/pii/S0098135400005810
- Quesada, Grossmann (1992), LP/NLP-B&B: https://www.sciencedirect.com/science/article/abs/pii/0098135492800288
- Vecchietti, Lee, Grossmann (2003): https://www.sciencedirect.com/science/article/abs/pii/S009813540200220X
- Trespalacios, Grossmann (2015), improved big-M: https://www.researchgate.net/publication/273579739_Improved_Big-M_reformulation_for_generalized_disjunctive_programs
- Trespalacios, Grossmann (2016), cutting planes for convex GDP: https://kilthub.cmu.edu/articles/journal_contribution/Cutting_planes_algorithm_for_convex_Generalized_Disjunctive_Programs/6466871
- Ruiz, Grossmann (2012), hierarchy of relaxations: https://www.sciencedirect.com/science/article/abs/pii/S037722171100899X
- Papageorgiou, Trespalacios (2018), pseudo basic steps: https://arxiv.org/abs/2501.15345
- Kılınç, Linderoth, Luedtke (2017), lift-and-project for convex MINLP: https://link.springer.com/article/10.1007/s12532-017-0118-1
- Stubbs, Mehrotra (1999): https://link.springer.com/article/10.1007/s101070050103
- Ceria, Soares (1999): https://link.springer.com/article/10.1007/s101070050106
- Lodi, Tanneau, Vielma (2023), conic disjunctive cuts: https://arxiv.org/abs/1912.03166
- Kronqvist, Misener, Tsay, Between steps: https://arxiv.org/abs/2101.12708 ; P-split (Math. Prog. 2025): https://link.springer.com/article/10.1007/s10107-025-02232-1
- Bernal Neira, Grossmann, conic GDP: https://arxiv.org/abs/2109.09657
- Gusev, Bernal Neira (2025), exact hull reformulation: https://arxiv.org/abs/2508.16093
- Lee, Bernal Neira (2026), reaggregated hull: https://arxiv.org/abs/2601.11782
- Ovalle et al., LD-SDA: https://arxiv.org/abs/2405.05358
- Nguyen, Pulsipher (2026), infinite-dimensional GDP methods: https://arxiv.org/abs/2608.27707
- Dai (2026), polyhedral OA for MISOCP: https://arxiv.org/abs/2608.10055
- Wei, Liu, Zeng (2026), nonsmooth OA: https://arxiv.org/abs/2602.04122
- Tamm, Eichfelder, Kronqvist (2025), warm-starting OA: https://arxiv.org/abs/2507.08595
- Ghezzi, Van Roy, Sager, Diehl (2024), S-B-MIQP: https://arxiv.org/abs/2404.11786
- Coey, Lubin, Vielma (2020), Pajarito: https://arxiv.org/abs/1808.05290
- GDPopt docs: https://pyomo.readthedocs.io/en/stable/explanation/solvers/gdpopt.html
- GDPopt config source: https://raw.githubusercontent.com/Pyomo/pyomo/main/pyomo/contrib/gdpopt/config_options.py
- MindtPy docs: https://pyomo.readthedocs.io/en/stable/explanation/solvers/mindtpy.html
- Pyomo.GDP transformations: https://pyomo.readthedocs.io/en/stable/explanation/modeling/gdp/solving.html
- GDPlib: https://github.com/SECQUOIA/gdplib
- Gurobi 13 release: https://www.gurobi.com/news/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities/ ; MINLP FAQ: https://www.gurobi.com/resources/faq/minlp-faq-practical-mixed-integer-nonlinear-modeling
- Mittelmann MINLPLib benchmark (Feb 2026): https://plato.asu.edu/ftp/minlp.html
