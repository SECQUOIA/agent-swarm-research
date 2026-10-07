# MINLP literature scout: state of the art, solver practice, and open theoretical questions

Date: 2026-09-22. Scope: open literature, mainly 2021–2026 (arXiv, Optimization
Online, Math. Program., IPCO, INFORMS JoC, JOGO, MPC, SIOPT, Oberwolfach
reports). The local knowledge base (`literature/papers/*/paper.md`, about 1,150
entries) was searched first, and the repository's own results
(`results/`, `notes/`) were checked so that questions already settled in-house
are marked.

How to read this report:

- Part I is the synthesis: cross-cutting findings, per-area summaries, the ten
  ranked open questions, runners-up, and the in-house overlap table.
- Part II (appendices A–D) holds the four detailed area reports, each with full
  citations and summaries of the cited open problems.
- "Verified" means the source statement was checked in the full-text PDF.
- "Unsolved" confidence levels are judgments from bounded searches. A failed
  search does not establish that a question is open or that a solution is new.

---

# Part I. Synthesis

## 1. Cross-cutting findings

1. **Theory of the core search loop is thin.** Most 2021–2026 work on bound
   tightening and spatial branching is empirical or learning-based. Examples:
   - learned OBBT for power flow (Cengil et al., EPSR 2022; COAP 92, 2025);
   - learned partition points (Kannan, Nagarajan, Deka, IJOC 2025,
     arXiv:2301.00306);
   - learned branching-rule selection (Ghaddar et al., IJOC 2023; González-Rodríguez
     et al., IJOC 2025, arXiv:2406.03626; Berthold and Geis, CPAIOR 2026,
     arXiv:2602.09996);
   - extreme strong branching (Dey, Han, Wang, arXiv:2510.20650, Oct 2025).

   The theory still rests on older papers: Caprara, Locatelli, Monaci (COAP 2016)
   for OBBT; Belotti et al. (2012) for FBBT; Kannan and Barton (JOGO 2017, 2018)
   for convergence order; Speakman and Lee (JOGO 2018) for branching points. No
   external paper proves tree-size lower bounds for continuous spatial
   branch-and-bound. The in-house `results/spatial-bb-*` notes appear to be ahead
   of the published literature there.

2. **Solvers ship cuts that are off by default because there is no selection
   theory.**
   - SCIP 8 and 9: quadratic intersection cuts and edge-concave cuts are
     implemented but disabled. SCIP 8's stated reason: there is no established policy for deciding when these cuts help (Bestuzheva et al., arXiv:2301.00587;
     arXiv:2402.17702).
   - SCIP 10 (arXiv:2511.18580, §3.5): flower-inequality separation for products
     of *continuous* variables is disabled. It needs nonnegative lower bounds, relaxes them to 0, and performed worse in the reported tests
     (verified in the PDF).
   - Gurobi: RLT cuts carry most of the cut benefit. Triangle-only BQP cuts add
     little (Gurobi 9.0 ablation slides; approximate figures).

3. **Characterization results are ahead of algorithmic use.**
   - Maximal quadratic-free sets are now fully characterized (Muñoz, Paat,
     Serrano, Math. Program. 2024; arXiv:2605.30602, May 2026).
   - The multilinear polytope is understood up to α-acyclicity (Del Pia and
     Khajavirad, CER, arXiv:2507.12831).
   - Hulls of one quadratic over a polytope are SOC-representable (Santana and
     Dey, SIOPT 2020).
   - What is missing is *which* cut or set to use, separation complexity,
     closures, and density control.

4. **MIP-relaxation (discretization) theory now has lower bounds for counts but
   not for strength.**
   - In-house: sawtooth is exactly count-optimal for x², and xy needs
     log2(1/ε)+O(1) binaries.
   - Beach et al. (COAP 2024, arXiv:2211.00876) show that LP strength and MIP
     strength can disagree.
   - Nobody bounds the minimum size of a *sharp* ε-relaxation.
   - Adaptive partitioning (Alpine) has only asymptotic convergence results.

5. **Symmetry handling for nonlinear problems is essentially SCIP-only.** SCIP
   covers expression-graph detection, reflections, and lexicographic and
   orbitopal reduction on arbitrary domains (van Doornmalen and Hojny, Math.
   Program. 212, 2025; Hojny, MPC 2025).
   - FICO authors write that symmetry handling is absent from nonlinear solvers (Berthold et al., arXiv:2605.04850).
   - No theory covers spatial branch-and-bound. Van Doornmalen and Hojny,
     Remark 14, note that one representative per orbit is not guaranteed.

6. **Certified or exact solving stops at MILP.** SCIP 10's exact mode is
   MILP-only and cannot certify presolve. No certified nonconvex spatial
   branch-and-bound exists.

7. **GPU methods have entered solvers.** Gurobi 13 ships PDHG on GPU, and NVIDIA
   open-sourced cuOpt. GPU relaxation kernels exist: Gottlieb and Stuber, MPC
   2026, and GPU interval branch-and-bound in MAiNGO, arXiv:2507.20769. There is
   no theory of warm-started first-order re-solves across nodes, and no theory
   linking first-order accuracy to lost bound strength.

## 2. Per-area summaries

Details, full citations and summaries of the cited questions are in Part II.

### 2.1 Convexification and cuts for quadratic and polynomial problems (Appendix A)

**State of the art**
- Intersection cuts from maximal quadratic-free sets, with monoidal
  strengthening and unique lifting:
  - Chmiela, Muñoz, Serrano, Math. Program. 197 (2023);
  - Chmiela, Muñoz, Serrano, Math. Program. B 210 (2025).
- RLT separation with implicit products and row marking (Bestuzheva, Gleixner,
  Achterberg, Math. Program. 210, 2025).
- Sparse eigenvector cuts (Dey, Kazachkov, Lodi, Muñoz, SIOPT 2022).
- Eigen-CG cuts: the conic closure of two subfamilies equals the Boros–Hammer
  (BH) closure (Dey, Jiang, Kazachkov, Lodi, Muñoz, arXiv:2604.00932, Apr 2026).
- BQP cuts for BoxQP via Burer–Letchford (Bonami, Günlük, Linderoth, MPC 2018).
- Multilinear polytope:
  - flower, running-intersection, β-acyclic extended formulation;
  - CER, exact if and only if the hypergraph is α-acyclic (arXiv:2507.12831);
  - BARON reports about 50% time reduction from running-intersection cuts;
  - SCIP 10 separates 1- and 2-flower inequalities.
- Quadratic aggregations and hidden convexity (Dey, Muñoz, Serrano, SIOPT
  2022; Blekherman, Dey, Sun, SIOPT 2024; Blekherman and Dunbar,
  arXiv:2405.18282).
- Sparse BoxQP hulls (Dey and Khajavirad, Math. Program. 2026,
  arXiv:2508.18435; Khajavirad, arXiv:2601.18545).
- Submodular BoxQP relaxation gaps: Ω(n) with BQP-valid cuts (Zhang and Wang,
  arXiv:2609.03617, Sep 2026).

**Stated open problems (selected; verified where marked)**
- An explicit algebraic description of QP_3 (verified in arXiv:2508.18435).
- Eigen-CG Conjecture 1: Eigen-CG cuts are implied by BH inequalities (verified
  in arXiv:2604.00932 §3).
- Complexity of submodular BoxQP for n ≥ 4 (Burer, Natarajan, Willemsen,
  arXiv:2504.03996).
- Maximal *polyhedral* quadratic-free sets (Muñoz, Paat, Serrano §8).
- Choosing base inequalities for joint-range cuts (Xu and Pokutta,
  arXiv:2608.03318).
- Separation complexity:
  - lifted bilinear cover cuts, conjectured NP-hard (Gu, Dey, Richard,
    arXiv:2208.00345);
  - α-cycle inequalities (CER paper).
- Lower envelope of W_ij for n > 2 (Belotti, Math. Program. 2025).

**In-house correction to Appendix A.** Appendix A lists Blekherman–Dey–Sun
Conjecture 3.1 as open. The repository has already answered it:
`results/infinite-quadratic-aggregation-hhc.md` shows that hidden hyperplane
convexity holds while infinitely many aggregations are needed. That result has
internal reviews and Lean verification, but no external review. Conjectures 3.2
and 3.3 remain open as far as we know.

**Missing theory**
- A selection theory for cuts: which maximal S-free set, and a density versus
  depth tradeoff.
- Closure and rank results for intersection cuts and sparse eigencuts.
- S-free sets for several quadratics.

### 2.2 Bound tightening (Appendix B, part A)

**Solver practice**

| Solver | Bound tightening |
|---|---|
| SCIP | Root OBBT on the LP relaxation plus Lagrangian variable bounds propagated in the tree (Gleixner, Berthold, Müller, Weltge, JOGO 2017) |
| BARON | Marginals-based reduction, probing, gradient-sign reduction (Zhang et al., JOGO 2020) |
| Couenne | Aggressive bound tightening |
| Alpine and power-systems codes | OBBT iterated to a fixed point |

Removing domain reduction increases node counts several-fold. BARON nodes rise
by 261–1,180% (Puranik and Sahinidis, Constraints 2017).

**Open problems**
- Rate, finiteness and complexity of the iterated-OBBT fixed point, and its gap
  to the true box hull. Caprara, Locatelli, Monaci (2016): the limit is difficult to guarantee.
- Fixed-point acceleration and filtering over *sets* of constraints (Puranik
  and Sahinidis 2017).
- An upper complexity bound for the bilinear FBBT limit. In-house has only
  PosSLP-hardness.
- A progress measure for nonlinear propagation, extending Sofranac, Gleixner,
  Pokutta (Constraints 2022) beyond linear constraints.
- Strength of marginals-based reduction versus OBBT.

### 2.3 Spatial branching (Appendix B, part B)

**Solver practice**
- Variable selection: violation-based scores with pseudocosts (SCIP), with
  reliability branching and strong branching available (Couenne).
- Branching point: a convex combination of the LP value and the midpoint. SCIP
  uses (α, β) = (1, 0.2); Couenne uses (0.25, 0.2).
- Belotti et al. (2009): none of the branching rules uniformly outperforms the others.
- Extreme strong branching (Dey, Han, Wang 2025) picks the variable and point
  jointly from several probes. It beats Gurobi 12, BARON and Couenne on
  bipartite bilinear and model-updating QCQPs, and it has no theory.

**Open problems**
- Kannan and Barton (JOGO 2018), conclusion items (ii) and (iii):
  convergence order of Stuber–Scott–Barton implicit-function relaxations, and
  propagation conditions that give second-order convergence in reduced-space
  schemes.
- Tolerance-dependent (ε) lower bounds for the cluster problem. All published
  counts are upper bounds.
- A tree-size theory for spatial variable and point selection.
- Separation between affine or eigen-direction branching and coordinate
  branching.

### 2.4 MIP and piecewise-linear relaxations (Appendix C, part A)

**State of the art**
- Sawtooth relaxations, which are sharp and hereditarily sharp (Beach,
  Hildebrand, Huchette, JOGO 2022).
- HybS, D-NMDT and tightened sawtooth (Beach, Burlacu, Bärmann, Hager,
  Hildebrand, COAP 2024; arXiv:2302.01164).
- Logarithmic and zig-zag ideal formulations (Huchette and Vielma, OR 2023;
  Lyu, Hicks, Huchette, Math. Program. 2023 and OR 2026).
- Optimal triangulations of xy (Burlacu, Hager, Hildebrand, arXiv:2604.04026,
  Apr 2026). Their Conjecture 6.1 on continuous triangulations is open.
- Alpine adaptive partitioning (Nagarajan et al., JOGO 2019), with linking
  constraints (Kim, Richard, Tawarmalani, SIOPT 2024) and strong partitioning
  (Kannan et al., IJOC 2025).
- Gurobi 12–13 defaults to spatial branch-and-bound with dynamically refined
  outer approximations. Static piecewise-linear approximation remains an option.

**Missing theory**
- Minimum size of *sharp* ε-relaxations.
- Iteration and binary complexity of adaptive partitioning, and whether
  adaptivity ever provably beats uniform logarithmic discretization.
- Complexity of the strong-partitioning max–min problem.

### 2.5 Symmetry with continuous variables (Appendix C, part B)

**State of the art**
- Detection through expression graphs, including signed permutations. Detection
  is undecidable in general (Hojny, MPC 2025, arXiv:2405.08379).
- Lexicographic, orbitopal and orbital reduction on arbitrary domains (van
  Doornmalen and Hojny, Math. Program. 2025).
- Geometry of fundamental domains (Verschae, Villagra, von Niederhäusern,
  Math. Program. 2023). Their Q1 and Q2 are open.
- Rotations: only simple fixings exist, which are the strongest possible for
  Givens rotations (Hojny and Liberti, arXiv:2605.02305).
- SCIP 10 added reflection-aware orbitopes and SST cuts.

**In-house evidence.** The fully symmetric concave family P_n is exponential for
every coordinate spatial branch-and-bound without symmetry handling (in-house
lower bounds). Yet SCIP solves P_30 in 11 nodes with symmetry handling and times
out without it (`results/separable-vertex-binarization.md`). No theorem explains
this.

### 2.6 Convex MINLP and GDP (Appendix D, part A)

**Solvers and methods**
- OA, ECP and ESH are implemented in SHOT, MindtPy, DICOPT, Bonmin, Pajarito
  and Boscia.
- Perspective and indicator hulls: rank-one and PSD-plus-polytope descriptions
  (Wei, Atamtürk, Gómez, Küçükyavuz, Math. Program. 2024).
- P-split formulations (Kronqvist, Misener, Tsay, Math. Program. 2026).

**Open problems**
- An iteration bound for OA without constraint qualifications (Tamm and
  Kronqvist, arXiv:2606.26897, June 2026: the authors doubt that such a bound can be established).
- Two-way separation between OA and NLP branch-and-bound.
  - Hijazi, Bonami, Ouorou (IJOC 2014) give a 2^n OA example.
  - That example is also hard for NLP branch-and-bound, so it is not a
    separation.
- OA on polyhedral approximations of conic problems without well-posedness
  (Lubin et al., Math. Program. 2018).
- Easy and hard classes for convex-MINLP certificates (Halbig et al., IJOC
  2024).
- Compact hulls for indicator QPs at treewidth above one (Bhathena et al. 2026).
  In-house: NP-hard at bandwidth 2.

### 2.7 Decomposition and Lagrangian methods (Appendix D, part B)

**State of the art**
- Shapley–Folkman duality-gap bounds (Udell and Boyd, COAP 2016; Dubois-Taine
  and d'Aspremont, Math. Program. 2025; Dey and Xu, arXiv:2601.19003).
- Decomposable zero-gap Lagrangian duals via redundant RLT constraints
  (Cifuentes, Dey, Xu, IPCO 2025, arXiv:2411.12085).
- Exact augmented-Lagrangian duality for nonconvex MINLP (Lefebvre and Schmidt,
  Optimization Online 2024, revised Dec 2025).

**Open problems**
- Complexity of the smallest exact penalty. Lefebvre and Schmidt conjecture it
  is hard (verified in the PDF).
- Polynomial-size penalties for QCQP.
- Tightness of the Cifuentes–Dey–Xu packing and covering bounds.
- Shapley–Folkman bounds for mixed-integer blocks.

### 2.8 New directions, 2024–2026 (Appendix D, part C)

- **Learning.** Learning with guarantees exists only for MILP: Balcan et al.,
  JACM 2024; Cheng and Basu, arXiv:2505.11636 and arXiv:2601.23249. There is no
  sample-complexity theory for continuous branching points.
- **GPU.** See item 7 in Section 1.
- **Exact and certified solving.** VIPR certificates and SCIP 10's exact MILP
  mode exist. Nonconvex MINLP certification is open.
- **Moment-SOS.** Finite convergence holds under nondegeneracy (Huang and Nie,
  arXiv:2403.17241). There are no a-priori order bounds for mixed-integer
  problems with continuous variables.

## 3. The ten most promising open theoretical questions

Selection criteria:

- (a) the question is explicitly open, or evidently unaddressed;
- (b) a solution would plausibly change what solvers implement or substantially
  strengthen bounds;
- (c) it is tractable in weeks for a strong theoretician with computational tools.

Items are roughly ordered by (b) × (c).

### Q1. A tree-size theory for spatial branching: choosing the variable and the point

**Question.** Build an abstract model of spatial branch-and-bound in which the
bound gain from splitting a box shrinks with width according to the
relaxation's convergence order (gap ≈ τ·w^β), with a continuous branching
point. Use it to decide:

- when strong or "extreme strong" branching provably beats violation or
  pseudocost rules;
- what the optimal branching-point rule is. Solvers currently use an ad hoc
  convex combination of the LP value and the midpoint.

**Evidence of the gap**
- Dey, Han, Wang (arXiv:2510.20650) list as future work explaining its especially good performance.
- Belotti et al. (OMS 2009): none of the branching rules uniformly outperforms the others.
- Speakman and Lee (JOGO 2018) solve only single trilinear terms.
- MILP analogues exist, but none is spatial:
  - Le Bodic and Nemhauser (Math. Program. 2017);
  - Dey, Dubey, Molinaro, Shah (Math. Program. 2024);
  - Cheng and Basu (arXiv:2601.23249).

**Impact.** Branching rules are the same in every solver. A model-based rule for
the branching point is directly implementable.

**Confidence unsolved:** about 80%. **In-house:** not touched.

### Q2. The iterated-OBBT fixed point: rate, finiteness, complexity, and distance to the box hull

**Question.** Let OBBT with a McCormick or RLT relaxation be repeated until
bounds stop changing. Answer the following:

- Does the process converge geometrically?
- Can it need exponentially many (or doubly exponentially many) rounds?
- Is the limit computable, for example by a single LP or fixed-point program?
- How far is the limit from the box hull of the feasible set?

**Evidence of the gap**
- Caprara, Locatelli, Monaci (COAP 64, 2016): the limit is difficult to guarantee, and good strategies fail when the problem class is slightly
  enlarged.
- Puranik and Sahinidis (2017) call for dependable acceleration toward a fixed point.
- Alpine and power-flow codes iterate to a fixed point without theory.

**Impact.** The results would give stopping rules and acceleration for OBBT,
the most expensive preprocessing step in Alpine, BARON and SCIP.

**Tractability.** The in-house constructions for FBBT (doubly exponential
iteration counts, PosSLP-hardness) are natural test cases. They may or may not
survive, because LP-based OBBT aggregates constraints.

**Confidence unsolved:** about 75%. **In-house:** candidate direction #13, not
started.

### Q3. Which quadratic-free set gives the best intersection cut, and can density be controlled?

**Question.** All maximal quadratic-free sets are now characterized by
non-expansive maps Γ (Muñoz, Paat, Serrano, Math. Program. 2024;
arXiv:2605.30602). What remains open:

- which Γ gives the deepest or sparsest cut for a given LP vertex and cone;
- whether the closure is polyhedral, and what rank results hold;
- S-free sets that avoid two or more quadratics at once.

**Evidence of the gap**
- SCIP 8 and 9 keep the cuts off by default because of density: there is no established policy for deciding when these cuts help.
- Muñoz, Paat, Serrano §8 leave the polyhedral case open.
- Xu and Pokutta (arXiv:2608.03318) leave base-inequality selection open.

**Impact.** A tractable selection rule or density guarantee could turn a
disabled SCIP feature into a default. No other solver has these cuts.

**Confidence unsolved:** about 80%.

### Q4. Eigen-CG Conjecture 1

**Question.** Is every Eigen-CG inequality implied by nonnegative combinations
of Boros–Hammer inequalities?

**Source.** Dey, Jiang, Kazachkov, Lodi, Muñoz, arXiv:2604.00932 (Apr 2026), §3,
verified: all their computational tests support the conjecture, although a proof is still missing.

**Impact.**
- True: solvers need only BH separation, and Gurobi already separates a subset
  of BQP cuts.
- False: a counterexample identifies a genuinely new cut family.

**Tractability.** The question is finite-dimensional and polyhedral in each n.
Computational search (n ≤ 7) plus proof is feasible.

**Confidence unsolved:** about 85%.

### Q5. Minimum size of sharp (LP-strong) MIP relaxations of xy and x^k

**Question.** What is the fewest number of binaries in an ε-relaxation of xy on
[0,1]² whose LP relaxation projects to McCormick (sharp), or that is
hereditarily sharp? What about x^k with the convex-hull LP? Also open is the
exact additive constant in p_min(ε) for xy.

**Evidence of the gap**
- The in-house count-only bounds are in `results/mip-relaxation-binary-lower-bounds.md`.
- Beach et al. (COAP 2024) show LP and MIP strength can disagree (HybS versus
  Bin2).
- Bärmann et al. (JOGO 2022) show every sharp bivariate formulation projects to
  McCormick.
- No published bound on the size of sharp formulations was found. The question
  is not stated verbatim anywhere.

**Impact.** It would settle which discretization Gurobi-style and Alpine-style
MIP relaxations should use.

**Confidence unsolved:** about 70%.

### Q6. Complexity of adaptive partitioning (Alpine / AMP)

**Question.**
- How many iterations and binaries does AMP need for ε-optimality on bilinear
  or multilinear programs?
- Is adaptive partitioning ever provably better than uniform logarithmic
  (sawtooth or NMDT) discretization?
- How hard is Kannan et al.'s strong-partitioning max–min problem?

**Evidence of the gap**
- Nagarajan et al. (JOGO 2019) and Burlacu, Geißler, Schewe (OMS 2020) prove
  only asymptotic convergence.
- Schmidt, Sirvent, Wollner (Optim. Lett. 2022) give only exponential bounds for
  Lipschitz oracles.
- Kannan, Nagarajan, Deka (IJOC 2025) §7 ask for methods for the max–min
  problem.

**Impact.** This would decide whether MIP-based global solvers should partition
adaptively or uniformly.

**Confidence unsolved:** about 75%. **In-house:** the spatial branch-and-bound
lower bounds do not cover AMP. The count-optimal sawtooth result is a natural
baseline.

### Q7. Node complexity of spatial branch-and-bound with symmetry handling on continuous variables

**Question.**
- For the S_n-symmetric concave family P_n, which is exponential for every
  coordinate spatial branch-and-bound, do lexicographic or orbitopal reduction
  give polynomially many nodes?
- Does this survive symmetry-preserving perturbations and relaxations?
- Can one orbit representative be guaranteed when spatial branching does not
  partition the feasible set?
- Can rotation × permutation groups (packing, distance geometry) be handled
  beyond simple fixings?

**Evidence of the gap**
- Van Doornmalen and Hojny (Math. Program. 2025), Remark 14 and §6.
- Hojny and Liberti (arXiv:2605.02305): only basic rotation-handling methods are available for rotations.
- In-house: P_30 is solved by SCIP in 11 nodes with symmetry handling and times
  out without it.

**Impact.** It would give a rationale for adding symmetry handling to Gurobi,
BARON and Xpress for nonlinear problems. FICO says none is present.

**Confidence unsolved:** about 80%.

### Q8. Multilinear cuts for products of continuous variables on general boxes

**Question.** SCIP 10 disables flower cuts for continuous products because it
must relax positive lower bounds to 0. An observation made in this scout
(checked against the CER definition, **not** independently reviewed):

- A multilinear set over a box [l, u] has the same convex hull as its vertex
  images (Rikun 1997).
- Under x = l + (u − l)∘y, each monomial becomes a linear combination of 0/1
  sub-monomials.
- So the hull is a linear image of MP(cl(G)), the multilinear polytope of the
  *completion* of G.
- Del Pia and Khajavirad define CER(G) = CER(cl(G)) and prove it is exact if and
  only if G is α-acyclic (arXiv:2507.12831, Theorem 2).
- Hence α-acyclic multilinear sets on *arbitrary* boxes appear to have exact
  extended formulations of size 2^r·|E_max|.

What stays open:

- original-space ("box-flower") inequalities;
- separation complexity for them;
- how the ratio u/l affects the value of the cuts;
- non-α-acyclic cases. Completing G creates β-cycles, so flower-type results for
  [0,1] do not transfer directly.

**Impact.** This directly targets a feature SCIP ships disabled, and it may
matter for BARON's running-intersection cuts on continuous products.

**Confidence unsolved:** about 60%. The extended-space corollary may be
folklore. The original-space and separation questions look open.

### Q9. Complexity of the smallest exact augmented-Lagrangian penalty for MINLP

**Question.** Is computing the smallest penalty that closes the
augmented-Lagrangian duality gap NP-hard? Do polynomial-size exact penalties
exist for QCQPs?

**Source.** Lefebvre and Schmidt, "Exact augmented Lagrangian duality for
nonconvex MINLP" (Optimization Online 2024/07, revised Dec 2025), §6, verified (summarized):
the authors ask whether the least penalty closing the duality gap can be computed in polynomial time, and conjecture that it cannot. They also leave unresolved whether quadratically constrained quadratic problems admit polynomial-size exact penalties.

**Impact.** Moderate: it governs penalty choice in augmented-Lagrangian
decomposition for structured MINLP.

**Tractability.** High. It is a natural reduction target.

**Confidence unsolved:** about 80%. **In-house:** not addressed. The in-house
augmented-Lagrangian branch-and-bound prototype studies a different question.

### Q10. Linearization methods versus NLP branch-and-bound for convex MINLP

**Question.** Is there a two-way exponential separation between OA, ECP, ESH
and LP/NLP branch-and-bound on one side and NLP branch-and-bound on the other?
Can OA have iteration bounds without constraint qualifications, in terms of a
Slater-type conditioning measure?

**Evidence of the gap**
- Tamm and Kronqvist (arXiv:2606.26897, June 2026): the authors doubt that such a bound can be established.
- Hijazi, Bonami, Ouorou (IJOC 2014) give a 2^n example, but it is hard for
  both methods.
- Bonami et al. (2008) and Grossmann (2002) leave open an a-priori criterion for
  choosing OA or NLP branch-and-bound.

**Impact.** It would give a principled choice between single-tree OA and NLP
branch-and-bound, which SHOT, Bonmin, Knitro-MINLP and Pajarito all have to
make.

**Confidence unsolved:** about 70%. **In-house:** candidate direction #2, not
started.

## 4. Runners-up

Each item is strong on some criteria and weaker on others.

- **QP_3 explicit hull.** Open since Anstreicher and Burer (2010); restated in
  arXiv:2508.18435 and arXiv:2601.18545 (verified). High value, but probably not
  a matter of weeks.
- **Submodular BoxQP complexity for n ≥ 4.** Burer, Natarajan, Willemsen,
  arXiv:2504.03996, together with the Zhang–Wang Ω(n) cut gap
  (arXiv:2609.03617).
- **Continuous optimal triangulation of xy.** Conjecture 6.1 of Burlacu, Hager,
  Hildebrand (arXiv:2604.04026), plus the bounded-domain and n ≥ 3 versions.
  Tractable, but the solver impact is a constant factor.
- **ε-dependent lower bounds for the cluster problem.** Also Kannan–Barton
  (2018) items (ii) and (iii) on reduced-space and propagation conditions.
  In-house Theorem 3 covers only width-tight reduction.
- **Decomposable zero-gap Lagrangian duals with easier subproblems.** Also
  whether the packing and covering bounds are tight (Cifuentes, Dey, Xu,
  IPCO 2025).
- **Easy and hard classes for convex-MINLP certificates** (Halbig et al., IJOC
  2024).
- **Fundamental domains for symmetry breaking.** Verschae et al., Q1 and Q2:
  polynomially many facets with unique binary representatives.
- **Blekherman–Dey–Sun Conjectures 3.2 and 3.3** on aggregations. Conjecture 3.1
  is answered in-house.
- **Multilinear exactness classes.** When the running-intersection or extended
  running-intersection relaxation is exact; α-cycle separation; recognizing a
  bounded nest-set gap (Del Pia and Khajavirad, 2021–2026).
- **Spatial learning theory.** Sample complexity for choosing continuous
  branching points. Balcan et al. (JACM 2024) cover only discretized MILP
  settings.

## 5. In-house overlap (do not re-propose)

| Topic | Status in repository |
|---|---|
| FBBT limit complexity and convergence | PosSLP-hard; doubly exponential primitive iterations (Lean-verified) |
| Coordinate spatial branch-and-bound lower bounds | 2^Ω(n) under separable, SDP–RLT, SOS, cut and lift node oracles. The affine-branching barrier note shows the proof fails for hyperplane branching |
| Kannan–Barton item (i) and clustering at KKT minima | Bypassed by the cluster-free theorem; attribution corrected to Anitescu and Bonnans–Shapiro |
| MIP relaxation binary counts | x² exact; xy within an additive constant of 2; powers and polynomials covered |
| McCormick versus hull gaps (Boland et al.; Luedtke–Namazifar–Linderoth Conjecture 1) | Resolved or strengthened |
| Blekherman–Dey–Sun Conjecture 3.1 | Answered: hidden hyperplane convexity with infinitely many aggregations |
| Indicator QP beyond trees | NP-hard at bandwidth 2; smoothed dynamic programming |
| P-split Theorem 6 | Counterexample and repair |
| Geoffrion Property (P′) | Refuted in its precise form |

## 6. Caveats

- Confidence figures are subjective, based on searches of arXiv, Optimization
  Online and publisher pages up to September 2026. Paywalled full texts
  (several Math. Program. papers) were read only through abstracts or preprints.
- A web summarizer produced one fabricated quote, attributed to van Doornmalen
  and Hojny. It was detected and excluded.
- Q8's extended-formulation observation is this scout's own derivation. It needs
  checking before use.
- Q5 and Q6 are gap-evident, not explicitly stated as open in the literature.
- Gurobi, BARON and Octeract internals are largely undocumented. Statements
  about what they "do not implement" mean "no public documentation found".

---

# Part II. Detailed area reports (appendices)

The appendices below are the per-area scout reports, unchanged except for
headings. Their citations use `[KB:slug]` for local knowledge-base entries.


## Appendix A. Convexification and cutting planes

### Scout report, Area 1: convexification and cutting planes for nonconvex quadratic and polynomial MINLP

Date: 2026-09-22. Scope: 2021-2026 work, with older anchors where needed.
Sources: the local KB (`/workspace/repo/minlp-notes/literature/papers/<slug>/paper.md`, cited as `[KB:slug]`) plus web and arXiv (cited by arXiv id or DOI). Statements and summaries draw on full texts: the KB `fulltext.md` or the arXiv PDFs saved under `/tmp/scout1/*.txt`. "Not found" means I searched for the item and did not find it. It does not mean the item is proven absent.

---

## 1. Intersection cuts and maximal quadratic-free sets

**State of the art**
- Muñoz & Serrano, "Maximal quadratic-free sets", IPCO 2020 and Math. Prog. 2022 (doi 10.1007/s10107-021-01738-8, arXiv 1911.12341). This was the first construction of maximal S-free sets for S = {x : q(x) <= 0} with q a general quadratic. The construction runs through a homogenization to the set {||x|| <= ||y||}.
- Chmiela, Muñoz & Serrano, "On the implementation and strengthening of intersection cuts for QCQPs", IPCO 2021 (LNCS 12707) and Math. Prog. 197:549-586 (2023) (doi 10.1007/s10107-022-01808-5). They give closed-form cut formulas, add Glover-style strengthening, and implement both in SCIP.
- Chmiela, Muñoz & Serrano, "Monoidal strengthening and unique lifting in MIQCPs", IPCO 2023 and Math. Prog. B 210:189-222 (2025) (doi 10.1007/s10107-024-02112-0). They show unique lifting, so monoidal strengthening gives the best possible coefficients for the integer variables.
- Muñoz, Paat & Serrano: "Towards a characterization of maximal quadratic-free sets" (IPCO 2023), then "A characterization of maximal homogeneous-quadratic-free sets" (Math. Prog. 2024, doi 10.1007/s10107-024-02092-1, arXiv 2211.05185), then "A characterization of maximal inhomogeneous-quadratic-free sets" (arXiv 2605.30602, May 2026). Together these give a **complete characterization** of full-dimensional maximal quadratic-free sets through non-expansive maps Γ. The 2026 paper: the authors state that the characterization now covers every maximal quadratic-free set.
- Related constructions:
  - Bienstock, Chen & Muñoz, outer-product-free sets and oracle-based cuts, Math. Prog. 183 (2020) [KB:bienstock2020-outer-product-free-sets-for].
  - Serrano, intersection cuts for factorable MINLP via concave underestimators, IPCO 2019, arXiv 1812.03073.
  - Modaresi, Kılınç & Vielma, intersection cuts for nonlinear integer programming [KB:modaresi2016-intersection-cuts-for-nonlinear-integer].
  - Xu & Liberti, submodular maximization through an intersection-cut lens, Math. Prog. 2024 (arXiv 2302.14020).
  - Xu & Pokutta, "Joint-range inequalities for nonconvex QCQPs", arXiv 2608.03318 [KB:xu2026-joint-range-inequalities-for-nonconvex]. They project two valid inequalities onto a 2-D joint range, convexify there, and lift back. The result is sparse cuts and a four-ray intersection cut.

**Solvers**
- SCIP 8 has quadratic intersection cuts in `nlhdlr_quadratic`, but they are **off by default**. SCIP 8's reason: dense cuts can be costly, and there is no established policy for deciding when generating them will help; consequently their separation is disabled by default [KB:bestuzheva2025-global-optimization-of-mixed-integer].
- SCIP 9 (arXiv 2402.17702) added monoidal strengthening and cut sparsification. Intersection cuts are still disabled in the default configuration. SCIP 9 reports that monoidal strengthening, when applicable, makes the strengthened cuts substantially more effective than the pure cuts.
- I found no evidence that Gurobi, BARON or Xpress implement quadratic-free intersection cuts.

**Stated open problems**
- Muñoz & Serrano (1911.12341): the practical effectiveness of the cuts needs evaluation. They also list comparing their approach with Bienstock et al., both theoretically and computationally and developing additional constructions of quadratic-free sets. Their 3-D conjecture was later settled by the Muñoz-Paat-Serrano full paper.
- Muñoz, Paat & Serrano (2211.05185, §8): characterizing which point sets in D^m define maximal Q-free polyhedra is left open. The polyhedral case and the choice of Γ remain open.
- Serrano (1812.03073): practical effectiveness is untested, and the cost of strengthening may outweigh its benefits
- Xu & Pokutta (2608.03318): automatically choosing an effective pair of base inequalities is a future direction. Their mixed cuts exclude the punctured Δ=0 cases.

**Missing theory**
- The characterization tells us which S-free sets are maximal. It says nothing about which maximal set yields the strongest or deepest cut for a given LP vertex and cone. With a whole family of Γ available, choosing Γ is an optimization problem that nobody has studied.
- I found no closure result, meaning no statement on whether the intersection-cut closure over all quadratic-free sets, or over the monoidally strengthened cuts, is polyhedral.
- I found no rank or convergence result for iterated quadratic intersection cuts. The only finite-convergence scheme I found is the oracle-based one of Bienstock, Chen & Muñoz, which uses a different set family.
- Every construction handles **one** quadratic at a time. Maximal S-free sets for intersections of two or more quadratics are open, apart from the 2-D projected case of Xu & Pokutta.
- I found no dimension-free density or sparsity guarantee, although density is the stated reason the cuts are disabled in SCIP.

## 2. Convex hulls of one or a few quadratics: aggregation, rank-one sets, hidden convexity

**State of the art**
- Santana & Dey, SIOPT 30(4) (2020), arXiv 1812.10160 [KB:santana2020-the-convex-hull-of-a]. The convex hull of one quadratic equality intersected with a bounded polytope is SOC-representable, with no sign or rank assumptions. The construction can be exponential in size.
- Modaresi & Vielma, Math. Prog. 164 (2017) [KB:modaresi2017-convex-hull-of-two-quadratic]: two quadratics, or one conic quadratic and one quadratic.
- Burer & Kılınç-Karzan, Math. Prog. 162 (2017) [KB:burer2017-how-to-convexify-the-intersection]: SOC cone intersected with one nonconvex quadratic.
- Dey, Muñoz & Serrano, SIOPT 32(2) (2022), arXiv 2106.12629 [KB:dey2022-on-obtaining-the-convex-hull]. Under PDLC, aggregations give the hull of three quadratics, but possibly through infinitely many aggregations.
- Blekherman, Dey & Sun, SIOPT 34(1) (2024), arXiv 2210.01722 [KB:blekherman2024-aggregations-of-quadratic-inequalities-and]: hidden hyperplane convexity (HHC) is sufficient for any number of quadratics.
- Blekherman & Dunbar, arXiv 2405.18282 (2024). Under PDLC, no points at infinity and nonempty interior, **at most 4** good aggregations suffice for three quadratics. This is a partial answer to the finiteness question.
- Exactness of the SDP relaxation in the convex-hull sense:
  - Wang & Kılınç-Karzan, Math. Prog. 193 (2022) [KB:wang2021-on-the-tightness-of-sdp].
  - Kılınç-Karzan & Wang, arXiv 2107.06885.
  - Wang & Kılınç-Karzan, ORL 2024 (arXiv 2403.04752).
  - Kojima, Kim & Arima, arXiv 2504.03204 and 2604.02968 (separable QCQPs).
- Rank-one based sets:
  - Dey, Kocuk & Santana, JOGO 77 (2020) [KB:dey2020-convexifications-of-rank-one-based].
  - Anstreicher, Burer & Park, bounded products, JOGO 80 (2021) [KB:anstreicher2021-convex-hull-representations-for-bounded].
  - Choi, Cepeda, Gómez & Han, rank-one convexification with step penalties, arXiv 2504.16330.
- Hidden convexity with bilinear terms: Gorissen, den Hertog & Reusken, OR 2026 [KB:gorissen2026-hidden-convexity-in-a-class]. Topological view: Chandrasekaran, Duff, Rodriguez & Shu, arXiv 2510.06112.

**Stated open problems**
- Dey, Muñoz & Serrano: whether finitely many aggregations always suffice to recover the convex hull remains unresolved. They also ask how to relax the absence of low-dimensional components condition and the PDLC condition.
- Blekherman, Dey & Sun, Conjecture 3.1: some sets S may require infinitely many good aggregations despite hidden hyperplane convexity. Conjecture 3.2 claims that examples needing more than four good aggregations exist. Conjecture 3.3 states that whenever conv(S)=R^n, aggregations supply certificates. Blekherman & Dunbar 2024 prove r <= 4 under extra assumptions and do not settle instances with more defining inequalities or with a nonempty variety. So Conjecture 3.2 remains open for the strict or general setting.
- Dey, Kocuk & Santana: they conjecture NP-hardness of linear optimization over U^row ∩ U^col. I found no resolution.
- Kılınç-Karzan & Wang (2107.06885): the conjectured equality V(G^⊥) = V(G^4) may hold without the facially exposed assumption. Wang & Kılınç-Karzan 2022: exactness criteria for strengthened QCQP SDP relaxations [e.g., SDP+RLT] are a research direction.
- Burer & Kılınç-Karzan 2017: evaluating the technique’s theoretical strength and practical effectiveness remains future work.
- Resolved example: Burer's conjecture that the lifted ball-QCQP relaxation dominates Kronecker RLT was proved by Kılınç-Karzan & Sun [KB:sun2025-on-the-strength-of-burers].

**Missing theory**
- Santana-Dey is an existence result. I found no separation-complexity result for conv{x ∈ P : quadratic} with P given by inequalities, and no compact (polynomial-size) version except in special cases.
- I found no bound on the number of aggregations as a function of n and m.

## 3. RLT, SDP/eigenvector cuts and sparse cuts

**State of the art**
- RLT separation in solvers: Bestuzheva, Gleixner & Achterberg, Math. Prog. 210 (2025), arXiv 2211.13545 [KB:bestuzheva2025-efficient-separation-of-rlt-cuts]. They detect implicit products, apply row marking, and report results in both SCIP and Gurobi.
- Sparse eigenvector cuts: Dey, Kazachkov, Lodi & Muñoz, "Cutting plane generation through sparse principal component analysis", SIOPT 32(2) (2022) [KB:dey2022-cutting-plane-generation-through-sparse]. Separating a k-sparse eigen-cut is NP-hard (it is sparse PCA). Hybrid sparse+dense cuts work best in practice.
- Quality of k-PSD closures:
  - Blekherman, Dey, Molinaro & Sun, "Sparse PSD approximation of the PSD cone", Math. Prog. 2022 (arXiv 2002.02988).
  - Bhardwaj, Kothari & Narayanan, arXiv 2105.11920.
  - Bhardwaj, Narayanan & Pathapati, arXiv 2405.01208.
- **Eigen-CG cuts**: Dey, Jiang, Kazachkov, Lodi & Muñoz, arXiv 2604.00932 (Apr 2026). They apply CG rounding to eigenvector inequalities and transfer the result to continuous variables through Burer-Letchford.
  - The conic closure of two of their subfamilies equals the Boros-Hammer (BH) closure.
  - They prove that dense Eigen-CG cuts are ineffective on top of SDP+McCormick.
  - BH / Eigen-CG capture only 3,676 of the 116,764 facets of BQP_6.
- Outer-product-free and oracle cuts: [KB:bienstock2020-outer-product-free-sets-for].
- Recent strengthening schemes for nonconvex QP:
  - Qu et al., DNN cutting planes, arXiv 2510.02948.
  - Lambert & Porumbel, convex quadratic cuts that converge to Shor+RLT, JOGO 2025/26 (doi 10.1007/s10898-025-01513-5).
  - Strahl, Raghunathan, Sahinidis & Gounaris, tight quadratic relaxations II (d.c.), arXiv 2408.13058.
  - González-Rodríguez et al., RLT branch-and-bound with SOCP/SDP constraints, JOTA 2025 [KB:rodriguez2025-polynomial-optimization-tightening-rlt-based].
- Exact and inexact RLT: Qiu & Yıldırım, JOGO 2024 and Math. Prog. 2025 [KB:qiu2024-on-exact-and-inexact-rlt; KB:qiu2025-polyhedral-properties-of-rlt-relaxations].
- Bipartite bilinear programs:
  - Dey, Santana & Wang, SOCP relaxation for bipartite bilinear programs, Optim. Eng. 2019 [KB:dey2019-new-socp-relaxation-and-branching].
  - Gu, Dey & Richard, lifting convex inequalities (arXiv 2106.12625) and lifted bilinear cover cuts (arXiv 2208.00345).

**Stated open problems**
- Eigen-CG, **Conjecture 1**: for any (v0, v), E-CG(v0, v) is implied by a nonnegative combination of BH inequalities. All reported computational tests support the conjecture, but no proof is given.
- Blekherman et al. (2002.02988): sharper bounds depending on the ratio [k/n] remain unresolved.
- Gu, Dey & Richard (2208.00345): they conjecture NP-hardness of separation, but anticipate difficulty in proving it. They also leave open whether the cuts help inside QCQP relaxations.
- Qu et al. (2510.02948): finite convergence of GMC for indefinite QP is unresolved; a rigorous convergence analysis remains future work.
- Tawarmalani (2026) [KB:tawarmalani2026-new-finite-relaxation-hierarchies-for]: RLT has no known guarantee of reaching the convex hull after finitely many steps for disjoint bilinear programs, in contrast with the new disjunctive-decomposition hierarchy.

**Missing theory**
- I found no approximation guarantee for sparse eigen-cut closures relative to the full SDP bound with McCormick/RLT included. Blekherman et al. bound only the distance from the PSD cone alone.
- I found no complexity result for separating Boros-Hammer inequalities in the continuous BoxQP setting beyond the known results for the BQP polytope.

## 4. Boolean quadric polytope and BoxQP

**State of the art**
- Burer & Letchford, SIOPT 20(2):1073-1089 (2009). The projection of QP_n = conv{(x, xx^T): x ∈ [0,1]^n} onto (x, off-diagonal X) is the Boolean quadric polytope (BQP) (Padberg 1989 [KB:padberg1989-the-boolean-quadric-polytope-some]). So every BQP inequality is valid for BoxQP.
- Bonami, Günlük & Linderoth, MPC 10:333-382 (2018) (doi 10.1007/s12532-018-0133-x). BQP cuts plus integrality-based preprocessing in spatial branch-and-cut make an LP-based solver competitive with SDP solvers on small and sparse BoxQP.
- Anstreicher & Burer 2010 [KB:anstreicher2010-computable-representations-for-convex-hulls]: PSD+RLT is exact for QP_n only when n=2.
- Recent structure-based exact formulations:
  - Dey & Khajavirad, "A second-order cone representable class of nonconvex QPs", arXiv 2508.18435 / Math. Prog. 2026 (doi 10.1007/s10107-026-02364-y) [KB:dey2025-a-second-order-cone-representable].
  - Khajavirad, "Tight SDP relaxations for sparse box-constrained QPs", arXiv 2601.18545 (2026). An RLT-SDP relaxation that exploits sparsity, with an exact extended formulation under tree-decomposition conditions.
- Submodular BoxQP:
  - Burer, Natarajan & Willemsen, arXiv 2504.03996 [KB:burer2025-on-the-semidefinite-representability-of]: an SDP with RLT is exact for n <= 3 and has a counterexample at n=4.
  - Zhang & Wang, arXiv 2609.03617 (Sep 2026): for n >= 4, **no finite family of instance-independent linear cuts** closes the SDP gap. With BQP-valid cuts the gap is Ω(n); with m arbitrary cuts it is Ω(n/m²).
- Other: Xia, Vera & Zuluaga, INFORMS JoC (arXiv 1511.02423); Fix-and-Bound for BoxQP, MPC 2024 (arXiv 2211.08911).

**Stated open problems**
- Dey & Khajavirad (2508.18435) and Khajavirad (2601.18545): an explicit algebraic description of QP_3 is still unknown.
- Khajavirad (2601.18545): it is open whether their SDP relaxation is an extended formulation of QP(G) for a complete graph with three nodes and three plus loops. The analogous result for |V+| > 2 is also open. [18] leaves unresolved the polynomial-time construction of a tree decomposition satisfying (I)-(III).
- Dey & Khajavirad: it is unknown whether SOC-representability of QP(G) requires the plus-loop nodes to form a stable set. They also leave open the computational difficulty of testing (C1)-(C3).
- Burer, Natarajan & Willemsen: the computational complexity of submodular quadratic minimization on [0,1]^n is unresolved for n >= 4. Zhang & Wang (2609.03617): a systematic method for constructing non-BQP-valid gap-reducing cuts is still sought. In one construction they write this construction does not settle the open problem.
- Gupte et al. [KB:gupte2020-extended-formulations-for-convex-hulls]: they conjecture extension of the observation to all wheels W_{n-1} with n >= 6, n even. Halin graphs are posed as an open question.
- Xia, Vera & Zuluaga (1511.02423): general bounds of this kind that can be computed effectively remain a research question.

## 5. Multilinear polytope (Del Pia, Khajavirad and others)

**State of the art**
- Acyclicity ladder:
  - Berge-acyclic: the standard linearization is exact.
  - γ-acyclic: flower inequalities.
  - Kite-free β-acyclic: running-intersection inequalities (MOR 2021) [KB:pia2021-the-running-intersection-relaxation-of].
  - β-acyclic: polynomial-size extended formulation (Math. Prog. 2024) [KB:pia2024-a-polynomial-size-extended-formulation].
  - α-acyclic: the complete edge relaxation (CER) is exact **iff** G is α-acyclic, with size 2^r|E_max| (Math. Prog. 2026, arXiv 2507.12831) [KB:pia2026-the-complete-edge-relaxation-for].
- Overview with a characterization of the acyclic hypergraphs that admit a polynomial-time-constructible polynomial-size extended formulation: Del Pia & Khajavirad, arXiv 2501.04805 (2025).
- Pseudo-Boolean polytope and limits of tractability [KB:pia2024-the-pseudo-boolean-polytope-and; KB:pia2025-beyond-hypergraph-acyclicity-limits-of].
- Knowledge compilation: Capelli, Del Pia & Di Gregorio [KB:capelli2026-a-knowledge-compilation-take-on].
- Simple odd β-cycle inequalities with strongly polynomial separation: Del Pia & Walter [KB:pia2023-simple-odd-cycle-inequalities-for].
- Recursive McCormick versus flower:
  - Khajavirad, ORL 2023 [KB:khajavirad2023-on-the-strength-of-recursive].
  - Schutte & Walter [KB:schutte2023-relaxation-strength-for-multilinear-optimization].
  - Raghunathan et al., arXiv 2207.08955.
- Decision-diagram cut generation: Cooper & Castro, arXiv 2607.28511 [KB:cooper2026-beyond-hand-derived-inequalities-decision]. Davarnia's graphical framework: arXiv 2409.19794.
- Continuous multilinear relaxations: piecewise polyhedral relaxations [KB:kim2024-piecewise-polyhedral-relaxations-of-multilinear]; symmetric multilinear polynomials [KB:xu2021-polyhedral-analysis-of-symmetric-multilinear].

**Solvers**
- BARON: running-intersection cuts gave about a 50% average time reduction on random multilinear/polynomial instances (Del Pia, Khajavirad & Sahinidis, MPC 12:165-191, 2020).
- SCIP 10 (arXiv 2511.18580) [KB:hojny2025-the-scip-optimization-suite-10] added `sepa_flower`, which separates k-flower inequalities for k=1,2 over AND constraints and products. Extending it to products of continuous variables caused worse performance, leading to its exclusion from the default configuration.

**Stated open problems**
- Characterize the hypergraphs with MP = MP^RI (2021) and with MP = MP^ERI (2024). The 2024 paper's Example 5 shows the extended running-intersection (ERI) inequalities are not enough for all β-acyclic hypergraphs.
- 2501.04805: an original-space description of the multilinear polytope for β-acyclic hypergraphs remains unknown (the authors doubt it would matter in practice).
- CER (2507.12831): open directions include extending inequalities (40) to arbitrary-length α-cycles, determining their separation complexity, and identifying the hypergraphs on which the new relaxation equals the multilinear polytope.
- Beyond acyclicity (2410.23045): the complexity of deciding bounded nest-set gap for a hypergraph remains unresolved. The complexity of constructing an elimination ordering with nsw_N(G) <= k is also open. The paper states two extension-complexity claims whose truth is unresolved.
- Pseudo-Boolean polytope (2309.08693): a full characterization of the signed hypergraphs in question remains unavailable.
- Del Pia & Walter, Conjecture 12: redundancy of non-simple odd closed walks.
- Schutte & Walter: the relationship between strengthened intersected recursive linearizations and running-intersection inequalities has yet to be determined.
- Cooper & Castro: polynomial-size compact DDs for β-acyclic hypergraph classes are not known to exist.
- Rank-one Boolean tensor factorization (2202.07053): recovery guarantees for the complete LP remain to be established.

## 6. Bilinear, trilinear and edge-concave/vertex-polyhedral envelopes

**State of the art**
- Classical:
  - Rikun 1997 [KB:rikun1997-a-convex-envelope-formula-for].
  - Sherali 1997 [KB:sherali1997-convex-envelopes-of-multilinear-functions].
  - Meyer & Floudas, trilinear facets and edge-concave envelopes (Math. Prog. 2005).
  - Tardella, vertex-polyhedral envelopes.
  - Tawarmalani, Richard & Xiong, envelopes via polyhedral subdivisions, Math. Prog. 138 (2013) [KB:tawarmalani2013-convex-envelopes-of-products-of].
  - Bao et al., multiterm polyhedral relaxations [KB:bao2009-multiterm-polyhedral-relaxations-for-nonconvex].
- Edge-concave cuts: Misener & Floudas (GloMIQO / GloMIQO 2, JOGO 2012-2013). Available in SCIP since 3.2, but no general-MINLP benefit has been established, so the separator is disabled [KB:bestuzheva2025-global-optimization-of-mixed-integer].
- Recent results:
  - Belotti, envelopes of bounded monomials on two-variable cones, Math. Prog. 211 (2025) [KB:belotti2025-convex-envelopes-of-bounded-monomials].
  - Makhoul & Speakman, volume of the trilinear hull over general boxes, IJOO 2026 (arXiv 2512.13964) [KB:makhoul2026-volume-formulae-for-the-convex].
  - Khademnia & Davarnia, bilinear terms over network polytopes, MOR 2024 (arXiv 2302.14151).
  - Davarnia & Rahimian, arXiv 2510.15861.
  - Dey, Han & Wang, aggregation of bipartite bilinear equalities, JOGO 94 (2026) [KB:dey2026-aggregation-of-bilinear-bipartite-equality].
  - Locatelli, envelopes of quadratics on the simplex [KB:locatelli2015-convex-envelopes-of-some-quadratic].
  - Karmarkar & Lucet, envelope of bivariate piecewise linear-quadratic functions in linear time, arXiv 2609.19343.
  - He & Tawarmalani, MIP relaxations of composite functions, SIOPT 2024 [KB:he2024-mip-relaxations-in-factorable-programming].

**Stated open problems**
- Belotti: for n > 2, the lower envelope of W_ij is unknown.
- Makhoul & Speakman: closed-form volumes for the alternative McCormick relaxations P1-P3 over general boxes are not yet known. They also ask whether the tightness ranking known for nonnegative bounds persists when bounds have mixed signs.
- Dey, Han & Wang: they suggest that intersecting the convex hulls of finitely many aggregated sets might recover the hull for broader choices of n1 and n2.
- Xu, Adams & Gupte: the general convex envelope of a supermodular function is unknown, and separation over it is NP-hard. An explicit hull for symmetric multilinear polynomials in general is also missing.

**Missing theory**
- I found no guarantee that relates edge-concave decomposition choices to the resulting bound; the decomposition is chosen heuristically.
- I found no volume or strength ranking for vertex-polyhedral cuts beyond trilinear monomials.

## 7. Solver implementations (summary)

| Solver | Quadratic/polynomial convexification and cuts |
|---|---|
| SCIP 8 (JOGO 91, 2025; arXiv 2301.00587) | Expression DAG with nonlinear handlers (quadratic, bilinear, SOC, convex/concave, perspective, quotient). McCormick, RLT (implicit and explicit products), 2x2 SDP minor cuts. Intersection cuts and edge-concave cuts implemented but **off by default**. |
| SCIP 9 (arXiv 2402.17702) | Monoidal strengthening of intersection cuts (still off by default), signomial handler with DC cuts (off by default), sparsification. MINLP about 4% faster and 13% fewer nodes than SCIP 8. |
| SCIP 10 (arXiv 2511.18580) | `sepa_flower` (1- and 2-flower inequalities). Handling of continuous products is off by default. MINLP gains exceed MILP gains. |
| Gurobi 9.0 (2019-20) | Nonconvex quadratics become bilinear terms. McCormick with local bounds, spatial branching. **RLT cuts** and **BQP cuts** (only triangle inequalities at that point). The 9.0 slides state PSD cuts were absent. |
| Gurobi 9.5+ | `PSDCuts` parameter; also `BQPCuts` and `RLTCuts` parameters. |
| Gurobi 11-13 | General MINLP through outer approximation and spatial B&B (11). Nonlinear expressions (12). NL barrier local solver and a claimed speedup exceeding 2x for MINLP (13). Cut internals are not published. |
| BARON | Multiterm polyhedral relaxations, running-intersection cuts (MPC 2020), tight quadratic relaxations (Strahl et al. 2024). |

## 8. Computational evidence on which cuts help

- Gurobi 9.0 webinar ablation, 444 models (values read from a slide, so treat them as approximate): timeouts were 21 by default, 110 without RLT cuts, 20 without BQP cuts, 165 without RLT+BQP, and 187 with no cuts. **RLT cuts carry most of the gain; triangle-only BQP cuts add little.**
- Bestuzheva, Gleixner & Achterberg: explicit RLT cuts solved 4,434 → 4,557 instances, with time ratio 0.85 and node ratio 0.81 on MINLP. Row marking cut RLT separation time share from 16.7% to 2.6% (MINLP) and from 54.6% to 2.8% (MILP).
- Bonami, Günlük & Linderoth: BQP cuts are highly effective on BoxQP.
- Dey et al. 2022: sparse cuts are cheaper but weaker at n=200-250 (75% vs 85% gap closed); the hybrid is the best compromise.
- Eigen-CG 2026: density makes the cuts less effective rapidly, while sparse cuts beyond triangles help.
- Intersection cuts: useful when monoidal strengthening applies (SCIP 9), but density prevents default use.
- Bienstock, Chen & Muñoz: oracle cuts complement SDP+OA; neither dominates.
- Running-intersection cuts: about 50% time cut in BARON on random polynomial instances. Simple odd β-cycle cuts: separation frequently too costly to be practical [KB:pia2023-simple-odd-cycle-inequalities-for].
- Perspective cuts: convex ones give consistent gains; nonconvex ones help root bounds but can hurt hard instances [KB:bestuzheva2023-a-computational-study-of-perspective].
- Cross-cutting gap: I found **no published cross-solver ablation** that isolates each cut family (RLT, BQP, PSD, intersection, edge-concave, flower) on QPLIB or MINLPLib under a common protocol. Evidence is solver-internal and version-specific.

## 9. Where theory is missing (cross-cutting)

1. **Cut selection theory for nonlinear cut families.** Density-versus-depth tradeoffs are the stated reason cuts are disabled (SCIP 8/9), yet no guarantee exists. The Eigen-CG "dense cuts are ineffective" theorem is the first such result.
2. **Closures.** I found closure results only for Eigen-CG (via BH) and for flower/RMC relaxations. I found none for quadratic intersection cuts, monoidally strengthened cuts, sparse eigen-cuts with McCormick, or joint-range cuts.
3. **Separation complexity.** Most separation problems are open or only conjectured hard: BH in the continuous setting, lifted bilinear cover cuts (conjectured NP-hard), α-cycle inequalities, and SOC conditions (C1)-(C3). Sparse eigen-cut separation is known to be NP-hard.
4. **Multiple-constraint S-free sets.** Only single-quadratic and 2-D joint-range results exist.
5. **Finite-convergence and rank results** for iterative quadratic/DNN cutting schemes: open, per Qu et al. and Tawarmalani.

## 10. Ranked shortlist of open questions (for the summary)

1. Explicit description of QP_3 (BoxQP hull, n=3) and more generally SDP/SOC-representability boundaries for QP(G). Stated in 2508.18435 and 2601.18545.
2. Eigen-CG Conjecture 1 (Eigen-CG closure = Boros-Hammer closure) (2604.00932).
3. Complexity of submodular BoxQP for n >= 4, combined with the Ω(n) cut-gap result (Burer et al. 2504.03996; Zhang-Wang 2609.03617).
4. Finiteness of aggregations for three or more quadratics (Dey-Muñoz-Serrano; Blekherman-Dey-Sun Conjectures 3.1-3.3; partial answer by Blekherman-Dunbar 2405.18282).
5. Quadratic-free intersection cuts: characterizing maximal *polyhedral* Q-free sets, choosing Γ for the strongest cut, closure and density theory, and extension to several quadratics (Muñoz-Paat-Serrano 2211.05185 §8; SCIP 8/9 default-off rationale).
6. Multilinear polytope: exactness classes for RI/ERI relaxations, α-cycle inequalities and their separation complexity, and recognition of a bounded nest-set gap (Del Pia-Khajavirad 2021-2026).

## Appendix B. Bound tightening and spatial branching

### Scout report, areas A and B: bound tightening and spatial branching

Date: 2026-09-22. Scope: literature on domain reduction and spatial branching for nonconvex MINLP, with emphasis on explicitly stated open problems and missing theory. Sources: the local KB (`literature/papers/<slug>`, cited as [KB:slug]), in-house results and notes in `/workspace/repo/minlp-notes`, and web search. Source statements draw on full texts I read (Kannan–Barton 2017 and 2018, Gleixner et al. 2017, Caprara–Locatelli–Monaci 2016 abstract, Dey–Han–Wang 2025) or from KB summaries. "Unsolved" judgments reflect a bounded search. They are not proofs of novelty.

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
  - Open directions (p. 21): filtering based on **sets** of constraints, dependable acceleration toward a fixed point, principled scheduling of probing and OBBT, and reduction designed to prevent clustering.
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
- Alpine.jl [KB:nagarajan2026-alpine-jl-v0-5-8] runs repeated OBBT until the bounds reach a fixed point, then adaptive multivariate partitioning.
  - Kannan, Nagarajan, Deka, "Strong partitioning and a ML approximation for accelerating global optimization of nonconvex QCQPs", *INFORMS J. Comput.* (2025), https://doi.org/10.1287/ijoc.2023.0424, arXiv:2301.00306. They learn the partition points and report a 2–4.5× average reduction in Alpine time. They note that exact solution of the max-min partitioning problem is computationally difficult.
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

   Caprara–Locatelli–Monaci (2016) say explicitly that the limit is difficult to guarantee. Puranik–Sahinidis ask for dependable acceleration toward a fixed point. Alpine and power-systems codes iterate to a fixed point without such theory. The in-house FBBT hardness and slow-convergence results **do not** transfer automatically: LP-OBBT combines constraints and may escape the monotone least-fixed-point construction. **Likely open (≈75%).**
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
  - None of the rules uniformly outperforms the others. Full strong branching spends 90–95% of time in its LPs on the `spar-*` instances.
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
  - There are **no theorems**. Stated future work: a variant based on reliability, and explaining the particularly strong results for BBP is a future direction.
- Chen, Atamtürk, Oren, *Math. Program.* 165 (2017) [KB:chen2016-a-spatial-branch-and-cut]: complex QCQP with rank-one-violation branching. Violation-based rules produced smaller trees than a reliability rule.
- Hübner, Gupte, Rebennack, *INFORMS J. Comput.* 38(2) (2026) [KB:hubner2026-spatial-branch-and-bound-for]: separable piecewise-linear sBB. Breakpoint branching terminates finitely. Largest-error branching converges only in the limit, and there is no general theorem guaranteeing convergence for the discontinuous case.

**Missing theory.**
- **No tree-size guarantee is known for any spatial branching rule.** This includes violation, pseudocost, strong, extreme strong, and volume rules.
- The MILP analogues exist:
  - Dey, Dubey, Molinaro, Shah, "A theoretical and computational analysis of full strong-branching", *Math. Program.* 205 (2024) 303–336, arXiv:2110.10754.
  - Cheng & Basu, "Theoretical challenges in learning for branch-and-cut", arXiv:2601.23249 (2026): local-score rules can produce trees exponentially larger than optimal, and even tiny score differences can lead to exponential differences in tree size.
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
   - Sources: Dey–Han–Wang 2025 future work; Speakman–Lee 2018; Belotti et al. 2009 (none of the rules uniformly outperforms the others); MILP analogues (Dey et al. 2024; Cheng–Basu 2026; Le Bodic–Nemhauser).
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

## Appendix C. MIP relaxations and symmetry

### Scout report: (A) MIP / piecewise-linear relaxations of MINLP, (B) symmetry handling with continuous variables

Date: 2026-09-22. Sources: local knowledge base, in-house `results/`, web search, and arXiv PDFs fetched to `/tmp/scout/`. Source statements were checked against PDF text I extracted myself; a web-summarizer "quote" attributed to the unified framework paper was fabricated and is not used. A failed search does not prove that a problem is open.

---

## Part A. MIP relaxations and piecewise-linear (PWL) relaxations

### A1. Sawtooth, separable, and NMDT relaxations for quadratic terms

**State of the art.**
- Beach, Hildebrand, Huchette, "Compact mixed-integer programming formulations in quadratic optimization", JOGO 84(4):869–912 (2022), arXiv 2011.08823. This paper introduced the Yarotsky sawtooth formulation for `y=x^2`. Error is `2^{-2L-2}` with O(L) binaries, rows, and auxiliary variables. The reflected Gray-code version is sharp and **hereditarily sharp**. The sawtooth *epigraph* relaxation (lower side) needs no binaries. KB: `beach2022-compact-...`.
- Beach, Burlacu, Bärmann, Hager, Hildebrand, "Enhancements of discretization approaches for non-convex MIQCQP", Part I: COAP 87:835–891 (2024), arXiv 2211.00876. It covers sawtooth, tightened sawtooth (TSR), Bin2/Bin3, and HybS. HybS needs `nL` binaries, against about `(n²+n)L/2` for Bin2/Bin3. HybS has a tighter LP relaxation than Bin2/Bin3, but its MIP relaxation is not always tighter. Part II: arXiv 2302.01164 introduces D-NMDT (doubly discretized NMDT), which reaches the same error as NMDT with fewer binaries and has a better LP relaxation.
- Bärmann, Burlacu, Hager, Kleinert, JOGO 85(4):789–819 (2022). For small ε, univariate reformulations of `xy` use fewer simplices than bivariate triangulations. Lemma 8 gives a simplex lower bound of `⌈area/(2√5 ε)⌉` for bivariate triangulations. The projection of every sharp bivariate formulation is exactly McCormick.
- NMDT/MDT: Teles, Castro, Matos (2013); Castro (2015, tightened piecewise McCormick); Castro, I&EC Res. 62(28):11053–11066 (2023, base-2 NMDT with OBBT in spatial B&B).
- Göß, Burlacu, Martin, JOGO (2026), arXiv 2407.06143: MIP-computed paraboloid estimators for Lipschitz functions.

**Stated open problems and future work.**
- Beach et al. 2022 (§7, App. C), on higher-order monomials: the authors observe that approximating x³ comparably appears to need many basis functions; they ask whether this is unavoidable or whether higher-order monomials admit compact approximations. They also leave an iterative implementation with a guaranteed prescribed approximation error as future work.
- Part II conclusion: proposed extensions include adaptive approximation and MIQCQP-specific valid cuts that the MIP solvers do not generate themselves.

**Already addressed in-house.**
- `results/mip-relaxation-binary-lower-bounds.md`: every MIP relaxation of `x²` with `p` binaries has error at least `2^{-2p-2}`, so sawtooth is exactly optimal. For `xy`, `p_min(ε)=log2(1/ε)+O(1)`, with the additive constant known only up to an interval of length 2.
- `bilinear-graph-binary-complexity.md`: graph-LP bounds for simultaneous bilinear terms.
- `quadratic-rank-integer-complexity.md`: integer dimension is half the Hessian rank.
- Pure powers, positive polynomials, and smooth maps: `positive-pure-power-linear-dimension-precision.md`, `rational-power-compiled-integer-precision.md`, `positive-polynomial-loglog-degree-precision.md`, `polynomial-graph-binary-integer-degree-gap.md`, `smooth-map-local-rank-integer-complexity.md`, and related files.

These in-house results largely settle the **binary-count** part of Beach et al.'s x³ question. For positive powers, O(log 1/ε) integers suffice, within an additive constant of optimal. They do **not** settle whether a formulation can be both count-optimal and sharp or hereditarily sharp for x³ or `xy`.

**Where theory is missing.**
1. **Count and LP strength together.** Is there a formulation of `xy` on `[0,1]²` with `log2(1/ε)+O(1)` binaries that is sharp, meaning its LP projection is McCormick? The same question applies to hereditary sharpness, and to x³ with the convex-hull LP. The in-house lower bounds ignore LP strength. Part I shows that LP and MIP tightness can disagree (HybS vs Bin2). Confidence open: **medium-high**. I found no theorem on the minimum binaries for a sharp ε-relaxation of `xy`.
2. **Exact constant for `xy`.** The in-house gap of 2 on the additive constant is open in-house.
3. **Constraint and auxiliary-variable counts** for a fixed binary budget. The in-house bounds let rows be unlimited.

### A2. Logarithmic and ideal formulations of PWL functions and combinatorial disjunctive constraints (CDCs)

**State of the art.**
- Vielma and Nemhauser, Math. Prog. 128:49–72 (2011): logarithmic formulations.
- Vielma, SIAM Review survey (2015).
- Huchette and Vielma, "Nonconvex piecewise linear functions: advanced formulations and simple modeling tools", OR 71(5):1835–1856 (2023), arXiv 1708.00050. Zig-zag ZZI/ZZB formulations are ideal and logarithmic and branch in a more balanced way. For bivariate grids, independent-branching depth is `⌈log d1⌉+⌈log d2⌉+6`. Implemented in PiecewiseLinearOpt.jl.
- Lyu, Hicks, Huchette, Math. Prog. 204:385–413 (2023), arXiv 2205.06916: junction-tree CDCs and an ideal SOS_k formulation. **Minimum biclique cover remains hard.**
- Lyu, Hicks, Huchette, OR 74(1):484–499 (2026), arXiv 2304.14542: shared SOS2 encodings for PWL lower and upper bounds, plus generalized nD-ordered CDCs.
- Related 2025 work: Dobrovoczki and Kis, arXiv 2503.10405 (triangulation heuristics and compact MILPs). Ploussard, Li, Pavičević, arXiv 2508.09395 (tightening DC-based continuous PWL MILPs).

**Stated open problems.**
- Vielma and Nemhauser 2011, concluding section: necessary conditions for logarithmic formulations are open. This is recorded in the in-house note `mip-relaxation-binary-lower-bounds.md`.
- Lyu et al. 2026, §8: they ask for faster formulations for generalized 1D-ordered CDCs, computational comparisons of multivariate piecewise-linear relaxations, and efficient construction of relaxations of multivariate nonlinear functions that fit generalized nD-ordered CDCs.

**Where theory is missing.** There is no theory relating branching balance (Huchette and Vielma's metrics) to B&B tree size. There are also no lower bounds on the constraint count of ideal logarithmic formulations for general CDCs.

### A3. Optimal triangulations

**State of the art.** Pottmann et al. (2000) found optimal interpolating triangulations and conjectured they are optimal among all approximations. Atariah, Rote, Wintraecken (2018) refuted that conjecture. Bärmann, Burlacu, Hager, Kutzer, JOTA 199(2):569–599 (2023), give a constant-factor "crossing swords" triangulation for `xy`. **Burlacu, Hager, Hildebrand, arXiv 2604.04026 (Apr 2026)** give the global optimum for discontinuous ε-approximations of `xy` on the plane: density `3√3/(32ε)`. They also give one-sided density `3√3/(16ε)` and prove optimality among parallelogram tilings for continuous approximations: density `√3/(8ε)`, with constant deviation `ε/3`.

**Stated open problems (summarized, §7).** the open directions are Conjecture 6.1 (whether the parallelogram-tiling optimum holds for every continuous triangulation), optimal simplicial approximations in R^n, and bounded domains, where boundary effects might allow smaller densities. Bärmann et al. 2022 add: ε-optimal bivariate triangulation for approximating F on a rectangle remains unresolved.

### A4. Adaptive partitioning (Alpine / AMP) and piecewise polyhedral relaxations (PPR)

**State of the art.**
- Nagarajan, Lu, Yamangil, Bent (CP 2016), arXiv 1606.05806. Nagarajan, Lu, Wang, Bent, Sundar, JOGO 74(4):639–675 (2019), arXiv 1707.02514 (AMP in Alpine.jl). The method refines partitions sparsely around the incumbent and runs OBBT. Convergence is proved only asymptotically, through exhaustive refinement. At iteration k there are at most `3+2(k−1)` partitions per variable.
- Sundar, Nagarajan, Linderoth, Wang, Bent, ORL 49:144–149 (2021), arXiv 2001.00514: an SOS2-based PPR for one multilinear term. It is locally sharp, but the recursive R-PPR depends on how terms are grouped.
- **Kim, Richard, Tawarmalani, SIOPT 34(4):3167–3193 (2024).** Linking constraints across overlapping multilinear terms on regular partitions give about 10× speedups in Alpine. The paper also gives the first locally ideal polynomial-size formulation for non-regular (decision-tree) partitions. Regular partitions can have exponentially more cells than non-regular ones. The linking system is not the full convex hull in general.
- He and Tawarmalani, SIOPT 34(3):2856–2882 (2024), arXiv 2310.07168: ideal MIP relaxations of discretized composites. They close about 60–70% of the McCormick gap.
- Kannan, Nagarajan, Deka, IJOC (2025), arXiv 2301.00306, "strong partitioning": a max–min problem that chooses partition points. An ML approximation gives 2–4.5× speedups in Alpine.

**Adaptive refinement with convergence guarantees.** Burlacu, Geißler, Schewe, OMS 35(1):37–64 (2020), classify refinement rules that guarantee convergence. They also show that earlier schemes may fail to terminate. Schmidt, Sirvent, Wollner, Math. Prog. (2019), and Optim. Lett. 16:1355–1372 (2022), treat Lipschitz nonlinearities and prove a **worst-case iteration bound** in the oracle setting.

**Stated open problems.**
- Kannan et al. §7 raise optimal allocation of partition points under a budget, which leads to a max–min problem with binary outer variables that calls for new solution techniques.

**Where theory is missing.** I found **no convergence-rate or iteration-complexity theory for AMP/Alpine-style adaptive partitioning of explicit polynomial terms**. Existing results give asymptotic convergence only, apart from the Lipschitz-oracle bounds, which are exponential in dimension. Open questions:
- How many AMP iterations, or how many total binaries, are needed for ε-optimality, compared with uniform or dyadic partitioning?
- Is adaptivity ever provably better than a uniform logarithmic (sawtooth/NMDT) discretization?
- What is the complexity of the strong-partitioning max–min problem?

The in-house spatial-B&B lower bounds do not cover AMP.

### A5. Solvers
- **Gurobi 11–13**: general nonlinear constraints. Gurobi documentation says function constraints were approximated by static PWL before Gurobi 11, and that since Gurobi 12 the default is spatial B&B with dynamically refined outer approximations. Static PWL (`FuncNonlinear=0`, `FuncPieces`/`FuncPieceError`) remains an option. Source: Gurobi 13 manual (KB `optimization2026-nonlinear-constraints-gurobi-optimizer-13`).
- **Alpine.jl** (AMP/PPR) and **PiecewiseLinearOpt.jl** (logarithmic and zig-zag formulations).
- **SCIP and BARON** use spatial B&B, not MIP-relaxation-based schemes.
- Ploussard et al., arXiv 2608.27312 (2026): Square/Triangle/DC PWL MILPs can beat QP solvers on long-horizon sequentially coupled bilinear programs.

---

## Part B. Symmetry handling in MINLP with continuous variables

### B1. Detection

**State of the art.**
- Liberti, "Reformulations in mathematical programming: automatic symmetry detection and exploitation", Math. Prog. 131:273–304 (2012): formulation groups found through expression-DAG automorphisms, plus static symmetry-breaking constraints. Applied to MINLPLib/GlobalLib with Couenne.
- Kouyialis, Wang, Misener, arXiv 1712.05222 (Processes 2019): binary layered graphs for QCQP symmetry detection.
- **SCIP 8** (arXiv 2112.08872) added detection of permutation symmetries through expression graphs, plus "complementary" symmetries for quadratic problems (attributed to Wegscheider's work).
- **SCIP 9 and Hojny, MPC (2025), arXiv 2405.08379**: symmetry detection graphs (SDGs) for signed permutations and reflections, with gadgets for sums, `(x_i−x_j)²`, bilinear terms, and even functions. The paper states that detecting general MINLP symmetries is undecidable, and that detection is NP-hard even for binary LPs.
- Wiese (MOSEK), "Symmetry detection in mixed-integer conic programming", MPC (2025/26).

**Stated open problems (Hojny 2025, §7.4, summarized).** future work could reduce the dependence of row/column-symmetry detection on generator structure. Exact detection would be desirable, but is as hard as graph isomorphism. Also, another direction is to use symmetry restrictions in B&B while allowing heuristics to operate without them. Reflection symmetries appear in only 6/486 MINLPLib instances.

### B2. Handling with binary variables: polyhedral and propagation methods

**State of the art.**
- Orbitopes and orbitopal fixing (Kaibel, Peinhardt, Pfetsch).
- Hojny and Pfetsch, "Polytopes associated with symmetry handling", Math. Prog. (2019): symretopes, symresacks, and almost-linear-time separation of symresack cover inequalities.
- Hojny, "Packing, partitioning, and covering symresacks", DAM (2020).
- Bendotti, Fouilhoux, Rottner, Math. Prog. (2021): orbitopal fixing for full (sub-)orbitopes, with an application to unit commitment.
- Schreier–Sims (SST) cuts: Liberti and Ostrowski, "Stabilizer-based symmetry breaking constraints for mathematical programs", JOGO 60:183–194 (2014), and Salvagnin (2018).
- **van Doornmalen and Hojny, IJOC 36(3):868–883 (2024), arXiv 2203.00992**: complete propagation for cyclic groups, under the assumption that generators are monotone and ordered.

**Stated open problems (summarized).**
- van Doornmalen and Hojny 2024, intro: the structure of lexicographically maximal points for cyclic groups has been unresolved for at least ten years. Conclusion: Algorithm 3 has a completeness guarantee for permutations γ that are both monotone and ordered; extending that guarantee after dropping either condition is an open direction.
- Deciding lexicographic maximality in an orbit is coNP-complete for generator-given groups.

### B3. General (continuous) variables: unified framework, fundamental domains, rotations

**State of the art.**
- **van Doornmalen and Hojny, "A unified framework for symmetry handling", Math. Prog. 212:217–271 (2025), arXiv 2211.01295.** Symmetry-handling constraints (SHCs) with node-dependent lexicographic orders unify orbital fixing, LexFix, orbitopal fixing, and isomorphism pruning. The paper generalizes them to arbitrary domains as *lexicographic reduction*, *orbitopal reduction*, and *orbital reduction*. These methods are implemented in SCIP 9/10.
  - Theorem 8 guarantees exactly one representative per orbit in finite B&B trees whose branchings partition the feasible region.
  - Remark 14, summarized: spatial B&B may have an infinite tree and branchings that do not partition the feasible region. Symmetry handling through (2) still applies, but the depth-pruned tree can retain multiple leaves with symmetric copies of a feasible solution.
  - Remark 15: the theorem survives for some infinite groups, such as rotations.
  - §6 future work: the framework permits future methods for rotations and reflections, plus separation routines for SHCs, packing/partitioning structure, and overlapping orbitopal subgroups in the same component.
- **Verschae, Villagra, von Niederhäusern, "On the geometry of symmetry breaking inequalities", Math. Prog. (2023), IPCO 2021, arXiv 2011.09641.** A *fundamental domain* is a minimal closed symmetry-breaking polyhedron for a finite orthogonal group acting on Rⁿ. The paper introduces generalized Dirichlet domains (GDDs).
  - Every permutation group has a fundamental domain with at most n−1 facets.
  - The closure of the lexicographically-maximal set equals the SST cuts.
  - SST cuts can over-represent a binary orbit by `2^{Ω(n)}` points, while a GDD with O(n) facets can give unique binary representatives.
  - Only reflection groups admit fundamental domains with a unique representative for every orbit in Rⁿ.
  - §6, summarized: **Q1:** whether GDDs cover every possible fundamental domain of an isometry group; **Q2:** whether each such group has a fundamental domain with polynomially many facets and exactly one representative per binary orbit. The authors also propose variants based on extension complexity or separation complexity, and characterizing the groups with O(1) representatives per orbit in Rⁿ.
- **Hojny and Liberti, "A computational comparison of handling distance constraints in MINLP", arXiv 2605.02305 (2026).** On rotations: applications such as kissing-number and sphere-packing problems currently have only basic methods for handling rotational symmetry. They prove the simple fixings `X_{i,j}=0 (j>i)`, `X_{1,j}≥0` are maximally strong within the class of Givens rotations.
- **SCIP 10** (arXiv 2511.18580) extends SST cuts and orbitopes to reflections and adds a heuristic for double-lex block matrices (disk packing).
- **Other solvers.** Berthold, Kamp, Mexi, Pokutta, Pólik (FICO), arXiv 2605.04850 (2026), footnote: symmetry handling is absent from nonlinear solvers because such symmetry is rarer and harder to detect. SCIP is the documented exception. I found no documentation of symmetry handling for nonlinear constraints in Gurobi or BARON; this is uncertain.

### B4. Symmetry, relaxation strength, and reformulation in continuous nonconvex problems

- Costa, Hansen, Liberti, DAM 161(1):96–106 (2013): symmetry-breaking constraints in spatial B&B for circle packing.
- **Khajavirad, ORL 57:107197 (2024), arXiv 2404.03091**: compares LP, RLT, and SDP relaxations with symmetry-breaking constraints for circle packing. It proves Anstreicher's conjectures, which also appear in-house in `point-packing-relaxations-anstreicher-conjecture-4.md` as known results.
- **Qu, Lu, Wu, Li, Deng, Fang, JOTA 209:71 (2026)**: exact variable-aggregation reformulations of separable (MI)QPs with symmetric variable groups. In the convex case the optimum has equal components. In the concave case all but one component sit at a bound. In the indefinite case the reformulation keeps first and second aggregate moments. Gurobi gains more from aggregation than from symmetry-breaking inequalities.
- **Timofte (2003) and Riener, arXiv 1001.4464 (JPAA 2012)**: the (half-)degree principle. Timofte's form: a symmetric degree-d polynomial is nonnegative on Rⁿ if and only if it is nonnegative on points with at most `max(⌊d/2⌋,2)` distinct coordinates. Riener derives this from a more general statement about symmetric optimization problems. Moustrou, Riener, and coauthors extend this to reflection groups. As far as I found, this is **not used in any MINLP solver**.
- Faenza et al., arXiv 2511.07766 (IPCO 2026): under (k+1)-transitive symmetry, level k of Sherali–Adams, Lovász–Schrijver, and lift-and-project are equally strong; whether the same holds for SoS is left open.
- **In-house link.** The spatial-B&B exponential lower bounds (`spatial-bb-*-exponential-lower-bound.md`) explicitly exclude symmetry handling: "Symmetry-breaking constraints, general branching disjunctions, and stronger moment hierarchies require separate analysis." `separable-vertex-binarization.md` records that SCIP solves the *symmetric* family `P_30` in 11 nodes through symmetry handling, and times out when `misc/usesymmetry = 0`. No theorem explains this.

---

## Candidate open theoretical questions (ranked)

1. **Continuous optimal triangulation of `xy` (Burlacu–Hager–Hildebrand Conjecture 6.1)**, plus bounded-domain and n≥3 versions. The conjecture is explicit and recent (Apr 2026), so it is very likely unsolved. Candidate optimum: `√3/(8ε)`.
2. **Fundamental domains with unique binary representatives and polynomially many facets (Verschae et al. Q2)**, and whether GDDs exhaust all fundamental domains (Q1). The questions are explicit (2021/2023), and I found no follow-up.
3. **Size and strength trade-off for MIP relaxations of `xy` and x^k.** What is the minimum number of binaries for a *sharp* or *hereditarily sharp* ε-relaxation, compared with the in-house count-only optimum? Also, what is the exact additive constant for `xy`? Not stated verbatim in the literature; no theorem found; extends in-house results.
4. **Iteration and binary complexity of adaptive partitioning (AMP/Alpine, Burlacu-type refinement).** Rates, lower bounds, and a comparison with uniform logarithmic discretization. There is no theory beyond asymptotic convergence and exponential Lipschitz-oracle bounds.
5. **Spatial B&B with symmetry handling for continuous variables.**
   - (a) Node-count theory: can lexicographic or orbitopal reduction make spatial B&B polynomial on S_n-symmetric nonconvex separable families (the in-house `P_n`)? What happens under group-preserving perturbations?
   - (b) Symmetry handling for rotation × permutation groups (point configurations) that are compatible with spatial branching (unified framework Remark 14 and §6; Hojny–Liberti 2026).
   - (c) Automatic use of the degree principle or orbit-space aggregation (Riener; Qu et al.) for non-separable invariant QCQPs.
6. Structure of lexicographically maximal binary points under cyclic groups. Described as open for a decade or longer.
7. Necessary conditions and constraint-count lower bounds for logarithmic ideal formulations (Vielma–Nemhauser 2011; Lyu et al.).

## Appendix D. Convex MINLP, decomposition, new directions

### Scout: convex MINLP, decomposition/Lagrangian methods, and 2024–2026 directions

Date: 2026-09-22. Scratch scout; not a result. Sources are primary papers or arXiv abstracts unless marked "(local KB)", meaning a summary in `literature/papers/<slug>/paper.md`. A failed search does not establish that a question is open. "In-house" refers to `/workspace/repo/minlp-notes/{results,notes,paper-*}`.

---

## A. Convex MINLP

### A1. OA, ECP, ESH, SHOT: state of the art

- **Methods.** OA (Duran–Grossmann 1986; Fletcher–Leyffer 1994), ECP (Westerlund–Pettersson 1995), ESH (Kronqvist, Lundell, Westerlund, JOGO 2016, [link](https://link.springer.com/article/10.1007/s10898-015-0322-3)), and single-tree LP/NLP-B&B (Quesada–Grossmann 1992). Serrano, Schwarz and Gleixner, JOGO 2020 ([link](https://link.springer.com/article/10.1007/s10898-020-00906-y)), show that ESH is Kelley's cutting-plane method applied to a gauge reformulation.
- **Regularization.** Kronqvist, Bernal and Grossmann, MP 2020 ([link](https://link.springer.com/article/10.1007/s10107-018-1356-3)); Bernal, Peng, Kronqvist and Grossmann, JOGO 2022 ([link](https://link.springer.com/article/10.1007/s10898-022-01178-4)). Both are implemented in MindtPy as ROA.
- **Nonsmooth OA.** Wei, Liu and Zeng, arXiv:2602.04122 (2026) ([link](https://arxiv.org/html/2602.04122)), strengthen OA cuts with constraint-derived parameters ρ_j. They note that the maximum used to choose these parameters cannot generally be computed at a practical cost.
- **Constraint qualifications and cycling.** Tamm and Kronqvist, arXiv:2606.26897 (June 2026) ([link](https://arxiv.org/abs/2606.26897)). Their Theorem 3: when Slater's condition nearly fails, gradient cuts at near-exact NLP solutions need not separate the MILP iterate. Their Theorem 7: adding ECP cuts at suboptimal integer assignments gives finite convergence without CQs at non-optimal subproblems. The paper establishes finite convergence, but no iteration-count bound is given; the authors doubt that such a bound can be established.
- **Polyhedral OA for MISOCP.** Dai, arXiv:2608.10055 (local KB `dai2026-...`) proves that cut-depth gains per new supporting direction vanish linearly with angular proximity, and proposes progressive-integrality OA.
- **Solvers.** SHOT ([Lundell, Kronqvist, Westerlund, JOGO 2022](https://link.springer.com/article/10.1007/s10898-022-01128-0)) supports CPLEX, Gurobi, Cbc and HiGHS; single-tree mode requires CPLEX or Gurobi (local KB `lundell2026-...`). Other implementations: MindtPy (OA, ECP, LP/NLP, GOA, ROA, FP), DICOPT, Bonmin, AOA (AIMMS), and Minotaur. Boscia.jl solves node relaxations with Frank–Wolfe over the mixed-integer hull through a MILP linear-minimization oracle ([Hendrych et al., MPC 2025](https://link.springer.com/article/10.1007/s12532-025-00288-w); [tutorial arXiv:2511.01479](https://arxiv.org/pdf/2511.01479)). Gurobi 13 treats general MINLP with spatial B&B over refined OA and documents no convex-specific path (in-house `notes/scout-20260912-convex-gdp-algorithms.md`).
- **Complexity.** Hijazi, Bonami and Ouorou, INFORMS JoC 2014 ([preprint](https://optimization-online.org/wp-content/uploads/2011/06/3050.pdf)), give a ball example on which OA needs 2^n iterations. Any polyhedral outer approximation of the ball needs 2^n hyperplanes before it excludes all lattice points. Their example is also hard for NLP-B&B, because the relaxation stays feasible until every variable is fixed. It is therefore **not** a separation between the two methods. Fletcher–Leyffer (1994) give an OA instance that visits all integer points. Basu, Jiang, Kerger and Molinaro, MP 2025 (local KB `basu2025-...`), prove information-complexity lower bounds. They state Conjectures 1–3: constrained transfer of lower bounds, Ω(d² log …) for general binary queries, and upper-bound transfer.

**Stated open problems or theory gaps**
1. An a priori criterion for choosing OA or NLP-B&B (Bonami et al. 2008; Grossmann 2002). This is in-house open-problem table item #30. A *two-way exponential separation* between NLP-B&B and every linearization master (OA/ECP/ESH/LP-NLP) is proposed as in-house candidate direction #2 (`notes/candidate-directions-2026-09-05.md`), marked "None started". No literature was found that settles it.
2. Iteration bounds for OA under CQ failure (Tamm–Kronqvist 2026, quoted above).
3. Rates for ESH/ECP in the mixed-integer setting. Only finite or asymptotic convergence exists. A rate would require bounds on the number of MILP rounds in terms of the gauge's conditioning. None was found.

### A2. Perspective reformulations and indicator hulls

- **Foundations.** Frangioni and Gentile, MP 2006; Günlük and Linderoth, MP 2010 (local KB). Bestuzheva, Gleixner and Vigerske, MPC 2023, give a computational study of perspective cuts in SCIP (local KB).
- **Rank-one and indicator hulls.** Atamtürk and Gómez, MP 2018 (M-matrices) and MP 2023 (supermodularity, [arXiv:2012.14633](https://arxiv.org/pdf/2012.14633)). Han, Gómez and Atamtürk, 2×2 convexifications, MP 2023. Wei, Gómez and Küçükyavuz, ideal formulations for constrained convex problems with indicators, MP 2022 ([arXiv:2007.00107](https://arxiv.org/abs/2007.00107)). **Wei, Atamtürk, Gómez and Küçükyavuz**, MP 204:703–737 (2024) ([arXiv:2201.00387](https://arxiv.org/abs/2201.00387)): the epigraph hull of a convex quadratic with indicators equals one PSD constraint plus linear constraints over an inverse-principal polytope. Han and Gómez, MOR 2025 (low-rank compact extended formulations). Shafiee and Kılınç-Karzan, MP 2024 ([link](https://link.springer.com/article/10.1007/s10107-023-02047-y)). Lee, Gómez and Atamtürk, MP 2026, multi-period QPs ([arXiv:2412.17178](https://arxiv.org/abs/2412.17178)). Rank-one convexification with step-function penalties ([arXiv:2504.16330](https://arxiv.org/pdf/2504.16330)). Stieltjes matrices with indicators ([arXiv:2404.04236](https://arxiv.org/pdf/2404.04236)).
- **Algorithms over graphs.** Bhathena, Fattahi, Gómez and Küçükyavuz give an O(n²) algorithm on trees (MP 2025) and a parametric method under treewidth, volume growth and a margin condition ([arXiv:2603.02103](https://arxiv.org/html/2603.02103v1)). Xu, Fattahi, Gómez and Küçükyavuz, "Coordinate Optimality Reformulation (CORe)", [arXiv:2608.01385](https://arxiv.org/abs/2608.01385) (Aug 2026). Choi, Fattahi, Han, Gómez and Lozano use decision diagrams, O(n^{k+1}) for trees with k leaves ([arXiv:2608.22815](https://arxiv.org/html/2608.22815v1)).
- **Solvers.** CPLEX and Gurobi apply internal perspective strengthening. Bhathena et al. 2026 conjecture that Gurobi uses perspective-based strengthening more effectively internally than a manual reformulation. SCIP strengthens estimators for semicontinuous variables. MOSEK solves perspective reformulations as conic problems.

**Open problems**
- Bhathena et al. 2026 (arXiv:2603.02103 §2.2): for general ω>1, it is unresolved whether f_u admits a compact representation. **In-house:** `results/indicator-quadratic-treewidth-two-hardness.md` proves NP-hardness at bandwidth 2, even with near-identity Hessians. `results/smoothed-indicator-block-dp.md` and `results/smoothed-spectral-indicator-messages.md` give smoothed polynomial exact algorithms. The remaining target is a conic extension-complexity lower bound for tree-structured epigraph hulls (`notes/research-20260922-frontier-scout.md`).
- Hull of conic-quadratic sets with indicators and bounded continuous variables (Gómez 2021; in-house table item #20, flagged).
- Compact hull of on/off constraints with non-monotone functions (Hijazi et al. 2017; item #19).
- **In-house:** `results/perspective-integer-precision.md` is a transfer lemma, not a new reformulation.

### A3. Mixed-integer conic optimization (MICP)

- Lubin, Yamangil, Bent and Vielma, IPCO 2016 ([arXiv:1511.06710](https://arxiv.org/abs/1511.06710)) and MP 2018 ([arXiv:1607.03566](https://arxiv.org/pdf/1607.03566)): extended formulations and disaggregation for OA.
- Coey, Lubin and Vielma, MPC 2020 ([arXiv:1808.05290](https://arxiv.org/abs/1808.05290)): K* cuts from conic certificates in Pajarito. Pajarito.jl v0.8 is current. Hypatia provides natural-cone interior-point solves ([IJOC 2022](https://dx.doi.org/10.1287/ijoc.2022.1202)).
- Lubin, Zadik and Vielma, MICP representability (MOR 2022), with Zadik 2024 on recession cones (local KB).
- Dai 2026 (above); warm-startable progressive-integrality outer-inner approximation for AC unit commitment ([arXiv:2603.19012](https://arxiv.org/pdf/2603.19012)).

**Open problems**
- Lubin et al. 2018, §8: the unresolved questions are how to guide modelers away from polyhedral-approximation failures and whether DCP can address those failures automatically. Coey et al. 2020 assume well-posed conic primal–dual pairs at every node; strong-duality failures can prevent convergence. This is in-house table item #22. Tamm–Kronqvist 2026 address only the smooth NLP-OA analogue, and only through an ECP fallback.
- MICP representability: sufficiency of the midpoint lemma, rationality, and the diameter assumption (item #33, partly addressed by Zadik 2024).
- Efficient conic disjunctive-cut separation and monoidal strengthening for conic MIPs (Lodi et al. 2023; item #21).

### A4. GDP, P-split, and hull size

- **State of the art.** Pyomo.GDP and GDPopt: LOA, GLOA, LBB, RIC, LD-SDA (Chen et al., Optim. Eng. 2022). LD-SDA: [arXiv:2405.05358](https://arxiv.org/html/2405.05358). DisjunctiveProgramming.jl ([arXiv:2304.10492](https://arxiv.org/pdf/2304.10492)). Hierarchy of relaxations via basic steps (Ruiz and Grossmann, EJOR 2012; Trespalacios and Grossmann 2014–2016). Conic GDP (Bernal Neira and Grossmann, COAP 2024, [arXiv:2109.09657](https://arxiv.org/abs/2109.09657)). "Between steps" (Kronqvist, Misener and Tsay, CPAIOR 2021 best paper, [arXiv:2101.12708](https://arxiv.org/abs/2101.12708)) led to the P-split paper (MP 218:57–94, 2026, [arXiv:2202.05198](https://arxiv.org/pdf/2202.05198)). Exact hull reformulation for quadratically constrained GDP (Gusev and Bernal Neira, [arXiv:2508.16093](https://arxiv.org/abs/2508.16093); the user's own work). Reaggregated hull for linear disjunctions with common coefficients (Lee and Bernal Neira, [arXiv:2601.11782](https://arxiv.org/abs/2601.11782), I&EC Res. 2026). Infinite-dimensional GDP ([arXiv:2608.27707](https://arxiv.org/abs/2608.27707)). Survey: Kronqvist, Bernal Neira and Grossmann, "50 years of MINLP and disjunctive programming", EJOR 2025 ([link](https://www.sciencedirect.com/science/article/pii/S0377221725005417)).
- **Open problems.** P-split paper, intro: the most effective MIP encoding of a disjunctive program remains unresolved. Also open for P-split: weak (interval) bounds, strict monotonicity, adaptive partitioning (item #5). When big-M equals the hull for intersecting disjuncts (Vecchietti 2003; item #4, open). Basic-step selection is exponential (2^r combined disjuncts), and there is no theory for choosing basic steps. In-house candidate: NP-hardness of choosing bound-improving basic steps (not started).
- **In-house coverage.** P-split Theorem 6 counterexample and repair (`notes/common-factor-p-split-correction.md`); an unbounded coordinate effect (`notes/common-factor-p-split-rotation-gap.md`); scaling-disjunction hulls (`results/scaling-disjunctions-hull.md`); LB-ESH, a computational study of radial versus point separation in convex GDP (`paper-lbesh/`). The LB-ESH literature audit concludes that the method is a cut-selection policy within established perspective-cut OA (`notes/lbesh-development-literature.md`).

---

## B. Decomposition and Lagrangian methods for structured MINLP

### B1. Lagrangian duality gaps (Shapley–Folkman line)

- Udell and Boyd, "Bounding duality gap for separable problems with linear constraints" (COAP 2016, [arXiv:1410.4158](https://arxiv.org/pdf/1410.4158)). Kerdreux, Colin and d'Aspremont, MOR 48(2) 2023. Dubois-Taine and d'Aspremont, MP 2025 ([arXiv:2406.18282](https://arxiv.org/abs/2406.18282)): constructive Frank–Wolfe with Shapley–Folkman, gap at most 2D_C/√(K+1) + (m+1)·max ρ(f_i). **Dey and Xu**, [arXiv:2601.19003](https://arxiv.org/abs/2601.19003) (2026): OPT(b+E·1) − E ≤ DUAL(b) ≤ OPT(b), and E→0 for sparse smooth blocks under a projection-factor condition. Hübner, [arXiv:2503.02464](https://arxiv.org/abs/2503.02464): probabilistic gap bounds for partially nonconvex blocks.
- **Decomposable zero-gap duals.** Cifuentes, Dey and Xu, [arXiv:2411.12085](https://arxiv.org/abs/2411.12085), IPCO 2025. Redundant RLT-type constraints make the Lagrangian dual exact while keeping it decomposable over tree decompositions. They give multiplicative bounds for packing and covering. **Stated open questions:** whether simpler iteration subproblems can retain a decomposable Lagrangian dual with zero gap, and whether the bounds in Theorem 9 and Theorem 10 are tight is also unresolved.
- **Theory gap.** Dey–Xu need smoothness and hidden convexity, which excludes integer blocks. A non-asymptotic Shapley–Folkman gap bound for *mixed-integer* blocks, with integrality-aware nonconvexity measures, remains missing. **In-house:** `results/geoffrion-property-p-conjecture.md` refutes the precise common-optimizer form (P′) of Geoffrion's 1972 Property (P) without compactness. The informal Property (P) is not refuted. The Shapley–Folkman papers are used in-house as aggregation theory (`notes/research-20260922-aggregation-*`).

### B2. Augmented Lagrangian (AL) duality

- **Chain.** Boland and Eberhard, MP 2015 (IP). Feizollahi, Ahmed and Sun, MP 2017 (MILP, any norm, finite ρ). Gu, Ahmed and Dey, SIOPT 30(1) 2020 (MIQP, polynomially bounded ρ). Bhardwaj, Narayanan and Pathapati, SIOPT 34(2) 2024 ([arXiv:2209.13326](https://arxiv.org/abs/2209.13326)): mixed-integer convex problems with sharp augmenting functions. **Lefebvre and Schmidt**, "Exact AL duality for nonconvex MINLP" (Optimization Online 2024/07, revised Dec 2025, [link](https://optimization-online.org/2024/07/exact-augmented-lagrangian-duality-for-nonconvex-mixed-integer-nonlinear-optimization/)). Norm penalties close the gap at finite ρ, and a finite ρ is computable in polynomial time for MILP.
- **Explicit open questions (Lefebvre–Schmidt, §6, summarized):** can a polynomial-time algorithm find a smaller exact penalty parameter? They also ask whether the least parameter that closes the duality gap is polynomial-time computable, and **conjecture that it is not**. A further question is whether polynomial-size exact penalty parameters, known for MIQPs, also exist for quadratically constrained quadratic problems. No follow-up resolving these was found (searched Sep 2026).
- **Algorithms.** MIX-ALM (Cristofari, Di Pillo, Liuzzi and Lucidi, JOTA 2026): local AL with primitive integer directions (local KB). Generalized Dual Decomposition (Zhang and Jiang, [arXiv:2605.14273](https://arxiv.org/abs/2605.14273), May 2026): a nonlinear regularizer gives strong duality for two-stage MIPs while keeping parallelism.
- **In-house:** `code/augmented_lagrangian_bb/albb.py` is a prototype of AL-based exact local bounds in αBB spatial B&B. It targets the cluster problem and is related to `results/cluster-free-branch-and-bound-constrained-minima.md`. Its docstring cites `results/augmented-lagrangian-exact-local-bounds.md`, **which does not exist in the repository**.

### B3. Column generation, ADMM, Benders, stochastic MINLP

- **Decogo.** Muts, Nowak and Hendrix: DECOA, JOGO 2020 (local KB); column and disjunctive-cut generation, Optim. Eng. 2021 ([link](https://link.springer.com/article/10.1007/s11081-020-09576-x)). Wu, Muts, Nowak and Hendrix, overlapping convex-hull relaxations, JOGO 2024/25 (local KB). The FW-CG convex-hull relaxation feeds heuristics. DECOA: extensions to large-scale and nonconvex settings remain to be developed.
- **ADMM and penalty-ADM.** Geißler, Morsi, Schewe and Schmidt, SIOPT 2017 (penalty ADM as a feasibility pump). Takapoui et al. (heuristic). Mix-CALADIN (Han et al., [arXiv:2604.14897](https://arxiv.org/pdf/2604.14897), 2026) claims convergence for Boolean variables under Lipschitz assumptions; the claims are unverified. ADMM for MINLP has **no global-optimality guarantee** in general. Guarantees exist only through exact-AL penalty arguments (B2).
- **Benders and stochastic.** Li and Grossmann, JOGO 2019: GBD branch-and-cut with Lagrangian and Benders cuts, convergent in the limit (local KB). Cao and Zavala, JOGO 2019 ([link](https://link.springer.com/article/10.1007/s10898-019-00769-y)): reduced-space B&B that branches only on first-stage variables. Füllner and Rebennack's SDDP review (SIAM Rev. 2025) lists open problems: deterministic stopping, cheaper nonconvex cuts, and high-dimensional regularization. Rathi et al., JOGO 2025: column generation for multistage stochastic MINLP with discrete states. Lou, Luo, Wächter and Wei, [arXiv:2501.11700](https://arxiv.org/abs/2501.11700): barrier-smoothed nonconvex two-stage decomposition with local stationarity only. Guan et al., Proxy Benders ([arXiv:2606.07403](https://arxiv.org/abs/2606.07403)): learned duals are projected to feasibility, so the cuts remain valid.
- **Open.** Finite exact termination for decomposition with continuous first-stage variables (Ogbe and Li 2019; Ahmed 2004; item #36). Monotone scenario-group bounds (item #12). A-priori regularization and efficient Lagrangian duals in nonconvex SDDP (item #27).

---

## C. New 2024–2026 directions

### C1. Learning-augmented global optimization

- Ghaddar et al., IJOC 2023 (spatial-branching rule selection for RLT). González-Rodríguez et al., [arXiv:2406.03626](https://arxiv.org/abs/2406.03626): strong-branching imitation is weak in spatial B&B. Berthold and Geis, [arXiv:2602.09996](https://arxiv.org/abs/2602.09996): PreferInt versus Mixed branching. Kannan, Nagarajan and Deka, "Strong partitioning", IJOC 2025 ([arXiv:2301.00306](https://arxiv.org/abs/2301.00306)): ML approximates max–min partition points while Alpine keeps global optimality. Learned OBBT variable selection; NN-embedded MINLP relaxations (Carrasco and Muñoz, MP 2026, [arXiv:2410.23362](https://arxiv.org/pdf/2410.23362)).
- **Guarantees.** Balcan, Dick, Sandholm and Vitercik, JACM 2024, "Learning to Branch: Generalization Guarantees and **Limits of Data-Independent Discretization**" ([link](https://dl.acm.org/doi/10.1145/3637840)). Cheng and Basu, [arXiv:2505.11636](https://arxiv.org/abs/2505.11636): sample complexity for piecewise-polynomial B&C policies, MILP only.
- **Theory gap.** No sample-complexity or generalization result exists for *spatial* branching. There the policy chooses a continuous branching point, and node bounds depend on relaxation geometry. No learned policy has been shown to improve worst-case node counts. Correctness is inherited: learned components only affect choices, never validity.

### C2. GPU first-order methods and GPU relaxations

- **LP.** PDLP (Applegate et al., [arXiv:2501.07018](https://arxiv.org/abs/2501.07018)); cuPDLP.jl ([arXiv:2311.12180](https://arxiv.org/pdf/2311.12180)); cuPDLPx ([arXiv:2507.14051](https://arxiv.org/pdf/2507.14051)); D-PDLP multi-GPU ([arXiv:2601.07628](https://arxiv.org/pdf/2601.07628)). Survey: Lu and Yang, [arXiv:2506.02174](https://arxiv.org/pdf/2506.02174). Its open items include FOM-specific presolve (has not yet been settled) and unreliable primal-weight rules. Presolve for GPU FOMs: [arXiv:2604.23951](https://arxiv.org/pdf/2604.23951). NVIDIA open-sourced cuOpt in 2025, and GAMS offers it ([link](https://www.gams.com/blog/2025/09/gpu-accelerated-optimization-with-gams-and-nvidia-cuopt/)). Gurobi ships a GPU PDHG. Batched PDHG for LPs inside MIP B&B (Blin, Gualandi, Maes, Lodi and Stellato, [arXiv:2601.21990](https://arxiv.org/pdf/2601.21990)). Fix-and-propagate from low-precision FOM solutions ([arXiv:2503.10344](https://arxiv.org/pdf/2503.10344)).
- **NLP.** MadNLP and ExaModels ([arXiv:2403.15913](https://arxiv.org/abs/2403.15913)); GPU second-order LP/NLP ([arXiv:2508.16094](https://arxiv.org/pdf/2508.16094)).
- **Global optimization.** Gottlieb and Stuber, "Automatic generation of GPU kernels for evaluators of McCormick-based relaxations and subgradients", MPC 2026 ([doi](https://link.springer.com/article/10.1007/s12532-026-00339-w)); their STOGO 2025 talk covers GPU B&B with a specialized PDLP. Zhang et al. (KU Leuven/RWTH/FZJ), GPU mean-value-form interval B&B in MAiNGO ([arXiv:2507.20769](https://arxiv.org/abs/2507.20769)): a speedup spanning three orders of magnitude over CPU interval arithmetic. B3-PWL GPU-batched B&B for SOS2 ([arXiv:2608.28988](https://arxiv.org/html/2608.28988)).
- **Theory gaps.** (i) No complexity theory for warm-started PDHG re-solves across B&B nodes or OA rounds. (ii) Safe dual bounds from low-accuracy FOM duals are straightforward with finite boxes (Neumaier–Shcherbina 2004), but no analysis relates bound loss to FOM accuracy. (iii) Mass-parallel box subdivision trades node count for bound quality with no guarantee. **In-house:** `results/fbbt-doubly-exponential-convergence.md` and `results/fbbt-monotone-system-hardness.md` bear on GPU FBBT; the `results/spatial-bb-*-exponential-lower-bound.md` results bound what parallel subdivision can gain.

### C3. Exact and certified solving

- Cheung, Gleixner and Steffy (VIPR, 2017). Eifler and Gleixner, MP 2023 (exact rational MIP). Eifler and Gleixner, safe GMI cuts, 2024. Borst, Eifler and Gleixner, certified propagation and dual proof analysis ([arXiv:2403.13567](https://arxiv.org/abs/2403.13567)). **SCIP 10** (Hojny et al., [arXiv:2511.18580](https://arxiv.org/pdf/2511.18580)): exact mode applies only to mixed-integer linear programs. Its certificates cover B&C only after presolve: these certificates do not establish correctness of presolve. Presolve can be certified separately only for binary programs with integer data. Exact mode is about 10× slower than default. Hoen and Gleixner, [arXiv:2412.14710](https://arxiv.org/abs/2412.14710): exact audit of floating-point B&B decisions. Wood et al., SMT verification of VIPR ([arXiv:2312.10420](https://arxiv.org/abs/2312.10420)). CakeML/HOL4 VIPR checker.
- **Convex MINLP certificates.** Halbig, Hümbs, Rösel, Schewe and Weninger, IJOC 36(6) 2024. **Stated open question:** the authors seek special problem classes where certificate construction, verification, or both are provably easy or provably hard. Also open: exploiting non-unique certificate half-spaces to shrink certificates.
- **Gap.** No certified or exact solver exists for **nonconvex** MINLP spatial B&B. That would require certificates for bound tightening, relaxations and branching over reals. discopt reports such certification bugs (issue #1301).
- **In-house:** `paper-certified-minlp/` gives checkable lower bounds for convex MINLP through rational OA and VIPR replay. The audit `notes/certified-minlp-literature-audit.md` rules out priority claims. Nonconvex certification and certificate-size theory are not addressed in-house.

### C4. Other emerging directions

- **Moment-SOS.** Finite convergence for polynomial matrix optimization under nondegeneracy, strict complementarity and SOSC (Huang and Nie, [arXiv:2403.17241](https://arxiv.org/abs/2403.17241)). Rate O(1/r²) on bounded sets ([arXiv:2402.00436](https://arxiv.org/pdf/2402.00436)). Mixed-integer versions with continuous variables beyond binary lifting lack a-priori order bounds (item #28).
- **NN-verification MINLP.** P-split for ReLU networks (Kronqvist, Misener and Tsay); Carrasco and Muñoz 2026.
- **Axis-aligned polyhedral relaxations.** Zhu, He and Tawarmalani, [arXiv:2603.18458](https://arxiv.org/abs/2603.18458): multilinear hulls over axis-aligned regions depend only on corner values.
- **Quantum and quantum-inspired methods.** No guarantee-bearing MINLP results were found. Not pursued.

---

## Summary table: what is addressed in-house

| Open question | Source | In-house status |
|---|---|---|
| Compact representation for indicator QPs at treewidth > 1 | Bhathena et al. 2026 | Largely addressed: NP-hard at bandwidth 2; smoothed exact DP. Extension-complexity lower bound open |
| P-split behaviour and exactness | Kronqvist et al. 2026 | Theorem 6 counterexample and rotation gap; weak-bounds question open |
| Geoffrion Property (P) | Geoffrion 1972 | Precise (P′) refuted; informal (P) open |
| Convex MINLP certificates | Halbig et al. 2024 | Replay pipeline built; easy/hard certificate classes open |
| OA vs NLP-B&B criterion | Bonami 2008; item #30 | Candidate #2, not started |
| Minimal exact AL penalty | Lefebvre–Schmidt | Not addressed (AL B&B prototype is a different question) |
| Conic OA without well-posedness | Lubin 2018; Coey 2020 | Not addressed |
| Decomposable zero-gap duals | Cifuentes–Dey–Xu 2024 | Not addressed |
