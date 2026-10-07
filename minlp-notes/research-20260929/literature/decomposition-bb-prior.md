# Prior work on decomposition-aware spatial branch-and-bound

Date: 2026-09-29. Workstream 1 (literature and novelty audit) of the
[program](../PROGRAM.md). Status: literature audit, not peer reviewed. An
unsuccessful search does not establish novelty.

## Summary

The shape of every claim has a close antecedent, but none of the four
claims is stated anywhere we looked in the form the program needs:
continuous (spatial) branching, relaxation-based pruning, and node or
certificate counts.

- **C1 (single-tree lower bound): partially known.** The cluster-problem
  literature already says, as estimates, that boxes near a nondegenerate
  minimizer can grow exponentially with dimension unless the relaxation's
  second-order prefactor is small (Neumaier 2004, Section 15;
  Wechsung–Schaber–Barton 2014, Theorems 1–2). Those estimates ignore
  sparsity, so they apply to paths. Two-stage papers say informally that
  full-space B&B is exponential in the number of scenarios (Kannan 2018;
  MUSE-BB 2025). In MILP, rigorous exponential lower bounds for LP-based
  B&B exist on bounded-treewidth instances: Basu–Conforti–Di Summa–Jiang
  (2023, Theorems 2.2 and 3.11; disjoint triangles, `2^{m+1} - 2` nodes) and
  Dey–Shah (2022, Theorem 1; lot-sizing, `2^{n/2-1}` leaves, which transfers
  to a treewidth-2 formulation, Section 1.7). Both instances have many
  optimal solutions. Not found: a rigorous lower bound for spatial B&B, for
  every adaptive tree, with per-factor relaxations on a bounded-treewidth
  continuous problem with a unique nondegenerate minimizer.
- **C2 (decomposition-aware upper bound): partially known.** Worst-case
  bounds of this shape are known by other methods: Bienstock–Muñoz LPs of
  size `O((2 pi/eps)^{omega+1} n log(pi/eps))` with accuracy scaled by
  coefficient norms (2018), grid DPOP for continuous DCOPs (Hoang et al.
  2020), and, for stage-structured problems, Zhang–Sun's nested
  decomposition bound `T(1 + 2LDT/eps)^d` (2022). With absolute accuracy
  the achievable form is `(C n/eps)^{O(w)}`, not `poly(n) * g(w, eps)`
  (Section 2). The discrete version of the algorithm itself
  (search on separators, cached lower bounds per separator value) is
  textbook: AND/OR branch-and-bound, BTD+. Branching only on complicating
  variables with Lagrangian bounds is classical for two-stage problems
  (Dür–Horst 1997; Cao–Zavala 2019; Kannan 2018; Li–Grossmann 2019).
  Not found: an instance-dependent bound such as `O(n log(1/eps))` at a
  nondegenerate minimizer, and any recursive (depth > 1) spatial
  decomposition B&B over a general tree decomposition with a complexity
  theorem. Robertson–Cheng–Scott (2025) show that the child bounds such a
  result needs are second order when the value functions are C^2, but at
  most first order when they are only Lipschitz, and below first order in
  general.
- **C3 (lower bounds in treewidth): partially known.** Known: ETH-based
  running-time bounds for discrete CSP (Marx 2010), approximation hardness
  and extension-complexity bounds in treewidth (Faenza–Muñoz–Pokutta 2022),
  Bienstock–Muñoz's `P != NP` result that `1/eps` dependence cannot become
  `log(1/eps)` even at treewidth 2, and algorithm-specific lower bounds for
  nested decomposition, `(DLT/(4 eps))^d` (Zhang–Sun Theorem 4). Not found:
  a lower bound on the size of decomposition *certificates* (or any B&B
  certificate) of the form `(C/eps)^{Omega(w)}`.
- **C4 (exponential separation): partially known in discrete settings, not
  found for spatial B&B.** Exponential gaps between plain tree search and
  decomposition-aware search are known for unpruned search spaces
  (Dechter–Mateescu 2007, Theorem 30) and for model counting
  (Bacchus–Dalmao–Pitassi, Theorem 4, branch width 0). For pruned MILP
  B&B, Basu et al. Theorem 3.11 already gives, with a one-line upper bound,
  an exponential gap between single-tree B&B and branching on a size-1
  binary separator followed by component decomposition, at treewidth 2; and
  Dey–Shah plus a reformulation gives an exponential gap between LP-based
  B&B and DP at treewidth 2. Both rely on instances with many optimal
  solutions. Nothing was found with continuous separators, which spatial
  branching never fixes, or with a unique nondegenerate minimizer.

The strongest competitor depends on the referee: AND/OR branch-and-bound
and BTD for an AI/CP referee; Zhang–Sun plus Robertson–Cheng–Scott and
MUSE-BB for an optimization or process-systems referee; Basu et al. and
Dey–Shah for a MIP-theory referee; Bienstock–Muñoz for a complexity
referee. Section 3 states how the program must differ from each. Two
further findings affect the program's statements: with absolute accuracy,
the worst-case form `poly(n) * g(w, eps)` is false under ETH (Section 2,
C2), and SCIP's component detection during the tree search is off by
default (Section 1.7).

## Method and what was checked

The auditor read key sources directly and delegated five literature sweeps to
helper agents, then spot-checked their load-bearing claims. Every source is
listed in Section 5 with the depth of reading. Claims marked **[derived]**
are our arguments, not statements in any source. Targeted commands only:
`grep`/`sed` on local full texts, `pdftotext` on downloaded PDFs, web search
and fetch. No project-wide checks were run; no CI was inspected.

## 1. Frontier map

### 1.1 Single-tree spatial B&B: the cluster problem

- **Du & Kearfott, JOGO 5 (1994).** Interval B&B with the midpoint test.
  Theorems 1–2 are *upper* bounds on the number of boxes left near a
  nondegenerate global minimizer, as a function of the order of the
  inclusion function. Remark 1: their corollary says "there may" rather
  than "there must" "because the theorem gives an upper bound, and not a
  precise value, for the number of boxes".
- **Neumaier, Acta Numerica 13 (2004), Section 15.** Heuristic count of boxes
  near a minimizer, exponential in `n` even with second-order bounds; "`n`
  replaced by `n - a`" with active constraints. No sparsity.
- **Wechsung, Schaber, Barton, JOGO 58 (2014).** Assumption 1: unique
  unconstrained minimizer with positive definite Hessian. Theorem 1 bounds
  the number of width-`delta` boxes needed to cover the `eps`-level set.
  Section 3: with second-order convergence, exponential growth in `n` is
  avoided only if the prefactor satisfies `K <= 9 lambda_1 / 4`. Theorem 2:
  alphaBB has `beta = 2` and `K <= alpha n / 4` (width = longest edge). The
  introduction: "even with second-order convergence, the number of boxes
  still has exponential dependence on the problem dimension as Neumaier
  claims". The analysis assumes the convergence-order bound is sharp and
  that boxes can be centred on the minimizer; it is an estimate, not a lower
  bound for every tree.
- **Kannan & Barton, JOGO 69 (2017); Kannan thesis (MIT 2018).** Constrained
  cluster analysis (upper estimates). Thesis, Section 2.3.2.3: "the
  worst-case running time of all known branch-and-bound algorithms is
  exponential in the dimension of the variables partitioned", the stated
  reason for reduced-space methods.
- **Repository.** Theorem 3.1 of
  `research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`
  is a rigorous lower bound for every adaptive tree when the gap is at least
  `alpha q_B`; its Section 10 compares it with the sources above.

None of these sources mention sparsity, separability or treewidth in a
node-count bound. They apply to paths only because they ignore structure.

### 1.2 Discrete search along tree decompositions (AI and constraint programming)

- **Dechter & Mateescu, "AND/OR search spaces for graphical models", AIJ 171
  (2007).** Preprint https://www.ics.uci.edu/~dechter/publications/r126.pdf;
  auditor read the theorem statements of Sections 4–6; a helper read them in full.
  - Theorem 30: with domain size `k` and a DFS tree of depth `m`, the AND/OR
    search tree has size `O(n k^m)`; "In contrast the size of its OR search
    tree along any ordering is `O(k^n)`. The above bounds are tight and
    realizable for fully consistent graphical models."
  - Proposition 37: minimal pseudo-tree depth `m <= w log n`. Theorem 38:
    AND/OR tree `O(n k^{w log n})`.
  - Theorem 67 and Corollary 68: the context-minimal AND/OR graph has size
    `O(n k^w)`; OR search graphs are bounded exponentially by pathwidth only.
    After Theorem 69: minimal AND/OR graph `O(n k^w)` versus minimal OR graph
    `O(n k^{w log n})` (upper bounds).
  - Remark 70: a chain has a pseudo tree with `m = n, w = 1` and a balanced one
    with `m = log n, w = log n`, but not both.
  - Theorems 81–82: AND/OR tree search in linear space and time `O(n k^m)`;
    AND/OR graph search in time and space `O(n k^w)`.
  - All sizes are of *unpruned* search spaces; the only exponential lower
    bound is the tightness of `O(k^n)` for fully consistent models.
- **Marinescu & Dechter, AIJ 173 (2009), two papers** (helper, full text).
  AOBB Theorem 3: time `O(n k^m)`, linear space, and `O(n k^{w log n})` at
  treewidth `w`, "from the size of the AND/OR search tree explored". AOBB-C
  (context caching) Theorem 6: `O(n k^w)`. The heuristic is a constant lower
  bound for the subproblem given the context. No node-count lower bounds; no
  proof that AOBB expands fewer nodes than OR B&B with the same heuristic.
  **Marinescu & Dechter, Constraints 15 (2010), 0/1 ILP:** LP relaxation as
  heuristic, `O(n 2^w)`; only suggests extension to MILP, never branches on
  continuous variables.
- **Mini-bucket heuristics** (Kask & Dechter, AIJ 129 (2001), Theorems 2.4,
  3.3–3.4; helper): mini-bucket messages are lower-bounding functions over
  subsets of the separator, admissible and monotone. Cost-shifting
  (Lagrangian reparameterization) heuristics: Ihler, Flerova, Dechter, Otten
  (UAI 2012; abstract). These are the discrete analogues of "Lagrangian
  child minorants".
- **BTD and relatives.**
  - Jégou & Terrioux, AIJ 146 (2003) (helper, full text): goods/nogoods on
    separators; time `O(n s^2 m log(d^s) d^{w+1})` (Theorem 5); BTD develops
    at most as many nodes as backtracking (Theorem 6, dominance, not
    separation).
  - de Givry, Schiex, Verfaillie, AAAI 2006
    (https://miat.inrae.fr/degivry/Schiex06a.pdf; auditor spot-check):
    without recording, visited nodes `O(d^h)` (tree height `h`), "This covers
    Pseudo-Tree or AND-OR tree search"; with recording `O(d^{w+1})`; BTD+
    solves a child with an inherited upper bound, records a lower bound per
    separator assignment on failure, and visits `O(k d^{w+1})` nodes
    (`k` = maximum integer cost), "better than branch and bound in `O(d^n)`".
    This is the closest discrete analogue of C2's child-bound mechanism.
  - Allouche et al., CP 2015 (BTD-HBFS; helper): `O(k n d^{w+1})` with cached
    lower and upper bounds per separator assignment.
  - Kitching & Bacchus, CP 2008 / IJCAI 2009 (helper): decomposition reduces
    worst-case time from `2^{O(n)}` to `n^{O(1)} 2^{O(w)}`, but separate
    recursions "can significantly reduce the strength of the bounds".
- **#SAT and DPLL with caching.** Bacchus, Dalmao, Pitassi, ECCC TR03-003
  (2002; auditor read) and JAIR 34 (2009; helper).
  - ECCC Theorem 4: "There exist families of CNF formulas with underlying
    branch width 0 such that counting satisfying assignments using #DPLL on
    these formulas takes exponential time" (disjoint clauses).
  - JAIR Theorems 1–3 (helper): simple caching `2^{O(w log n)}`; component
    caching `n^{O(1)} 2^{O(w)}`; linear space `2^{O(w log n)}`.
  - JAIR Theorems 6–7 (helper): search tied to a fixed decomposition can lose
    super-polynomially to dynamic variable ordering.
  - Darwiche, recursive conditioning, AIJ 2001 (abstract): `O(n exp(w log n))`
    time in linear space, `O(n exp(w))` with caching.
  - Knowledge compilation: Razgon (KR 2014; helper) gives CNFs of treewidth
    `<= k` with OBDD size `>= f(k) n^{k/4}` (OR-type representations are
    XP in treewidth, not FPT).
- **Nonserial DP.** Bucket elimination, Dechter AIJ 113 (1999) (helper):
  elim-opt, the nonserial DP of Bertelè–Brioschi, is exponential in induced
  width (Theorem 11). Section 2.3 warns that Fourier elimination for linear
  inequalities is *not* bounded exponentially by induced width: continuous
  messages have no width-bounded exact representation. Morin–Marsten
  (Oper. Res. 1976; abstract) fathom DP states with relaxation bounds.
  Bertelè–Brioschi (1972) was not accessed.

### 1.3 Continuous domains with tree structure (constraints and DCOP)

- **Faltings 1994** (local `faltings1994-arc-consistency-for-continuous-variables`;
  helper): on tree-structured continuous networks, two passes reach arc
  consistency, and arc consistency equals global consistency only on trees
  (Theorem 3.2). Feasibility only.
- **Sam-Haroud & Faltings, Constraints 1 (1996)** (abstract): relational
  consistency for a class of continuous CSPs.
- **Vu, Schichl, Sam-Haroud 2009** (local): propagation on expression DAGs; no
  decomposition of the search.
- **Inter-block backtracking** (Bliek, Neveu, Trombettoni CP 1998; Neveu,
  Trombettoni, Chabert, Constraints 15 (2010); helper): search over a DAG of
  equation blocks for square systems; no optimization, no complexity theorem.
- **Hoang, Yeoh, Yokoo, Rabinovich, AAMAS 2020, arXiv 1905.13275**
  (abstract checked by auditor; theorems by helper): exact algorithms for
  tree-structured continuous DCOPs with binary linear or quadratic
  functions; Grid DPOP Theorem 1: error at most `|F| m delta` (cell size `m`,
  gradient bound `delta`); Theorem 4: message size `O(d^w)`. Together these
  give the worst-case grid bound `poly(n) (C |F| / eps)^{O(w)}`.
- **Ye, Say, Sanner, CPAIOR 2018** (abstract): symbolic bucket elimination for
  piecewise-linear or quadratic functions; no complexity bound.

### 1.4 Bounded-treewidth polynomial optimization and treewidth hardness

- **Bienstock & Muñoz, SIOPT 28 (2018)** (local, full text).
  - Problem: linear objective, polynomial constraints, variables in
    `{0,1}^p x [0,1]^{n-p}`; `omega` = treewidth of the constraint
    intersection graph; `pi` = degree.
  - Theorems 4 and 15: an LP with `O((2 pi/eps)^{omega+1} n log(pi/eps))`
    variables and constraints; feasibility tolerance `F eps` (scaled by the
    coefficient 1-norm), optimality tolerance `||c||_1 eps`.
  - Theorem 7: network version `O((D pi/eps)^{O(Delta omega)} n log(pi/eps))`.
  - Theorem 9: exact LP of size `O(2^omega n)` for binary problems; "`2^omega m`
    is a lower bound on the number of oracle queries that any algorithm for
    solving GB must perform" (stated, proof not in the main text).
  - Appendix A (subset sum at treewidth 2): unless `P = NP`, neither an
    unscaled tolerance nor running time polynomial in `log(1/eps)` is
    possible.
  - No B&B.
- **Faenza, Muñoz, Pokutta, Math. Prog. 191 (2022)** (local; helper full
  text). Theorem 3.3: the same LP size for degree-`rho` polynomial problems.
  Theorem 3.6: for fixed `eps < 1/10`, a QCQP algorithm running in
  `T(k) poly(|I|)` on graph families indexed by treewidth `k` forces `T`
  superpolynomial unless `NP ⊆ BPP`. Theorem 4.24: 0/1 sets with SDP extension
  complexity nearly exponential in treewidth.
- **Marx, Theory of Computing 6 (2010)** (abstract): under ETH, binary CSP
  has no `f(G) n^{o(k/log k)}` algorithm on any graph class of unbounded
  treewidth `k`. Cohen-Addad, Colin de Verdière, Marx, de Mesmay (JACM 2021),
  Theorem 2.7 (helper, full text): `|D|^{o(tw/log tw)}` is impossible for
  every fixed `G` with `tw >= 2`.
- **Sparse moment/SOS hierarchies.** Waki et al. 2006 and Lasserre 2006
  (local): convergence under the running intersection property, no rates;
  Laurent 2009 survey Sections 8.1–8.2 (helper); Wainwright–Jordan 2004
  (0/1 only: Sherali–Adams exact at level `t+1`). Korda, Magron,
  Ríos-Zertuche (Math. Prog. 2025, arXiv 2303.14824; abstract checked):
  polynomial convergence rates depending on the largest clique size.
  Nie, Qu, Tang, Zhang (arXiv 2406.06882 v3, 2025; abstract checked; helper
  full text): the sparse hierarchy is tight exactly when `f - f_min` splits
  into sparse polynomials, one per clique, each certified nonnegative on its
  own clique (Theorem 3.1). In the program's terms this is a certificate
  with one cell and polynomial transfer terms between cliques. Their
  Example 6.7 is a 3-variable path whose separator value function is not
  polynomial, and the sparse hierarchy is never tight on it. No
  comparison with B&B node counts was found.
- **Convex MIQP with indicators on structured graphs.** Liu, Fattahi, Gómez,
  Küçükyavuz (Math. Prog. 2023; local): `O(n^2)` DP on paths; Gurobi B&B node
  counts 14, 2,764, 404,475 and 17,965,177 for `n` = 10, 50, 100, 200
  (auditor checked Table 2). Bhathena, Fattahi, Gómez, Küçükyavuz: exact
  parametric DP on trees (Math. Prog. 2025) and at bounded treewidth
  (arXiv 2603.02103, Theorem 1, time linear in `n` under a margin and
  volume-growth assumption; helper); convex only. Xu et al. (arXiv 2608.01385; local) Proposition 3: on path
  graphs the number of feasible integer leaves of B&B on their formulation is
  exponential in `n` (counts feasible leaves, not a pruned-tree bound).

### 1.5 Two-stage decomposition-based global optimization

- **Dür & Horst, JOTA 95 (1997)** (abstract): the Lagrangian duality gap
  goes to zero under refined partitioning; for partly convex problems,
  partitioning only the nonconvex variables suffices. This is the classical
  convergence basis for branching only on some variables with Lagrangian
  bounds.
- **Epperly & Pistikopoulos, JOGO 11 (1997)** (via Kannan thesis Section
  6.5): reduced-space B&B on variables in nonconvex terms; can be only first
  order (Kannan Example 6.5.9).
- **Nowak 2005 habilitation (LaGO)**
  (https://edoc.hu-berlin.de/items/463830e0-3352-48b4-b538-e5e7adf6bffa/full;
  auditor, full-text grep): block-separable splitting with copy constraints
  (Section 2.3), Lagrangian decomposition bounds (Chapter 4), and one
  rectangular B&B over the full space (Algorithm 13.1, Section 13.4). The
  relaxation is decomposed; the search is not. No complexity analysis.
  DECOGO (Nowak et al., JOGO 72 (2018); abstract) replaces the tree by
  column generation and outer refinement.
- **Karuppiah & Grossmann, JOGO 41 (2008)** (secondary): Lagrangean cuts
  added to a convex relaxation, with branching on linking variables. No
  complexity result.
- **Cao & Zavala, JOGO 75 (2019)** (helper, full preprint): B&B only on
  first-stage variables; node bound = sum over scenarios of the scenario
  minimum over the box (nonanticipativity dropped); Theorem 1 convergence;
  no complexity; node count "not expected to explode" with the number of
  scenarios.
- **Kannan thesis (2018)** (local; helper and auditor): modified Lagrangian
  relaxation, branching only on continuous first-stage variables;
  Theorems 3.5.5 and 3.5.8 (convergence, finite `eps`-convergence).
  Chapter 6 (a setting where the unbranched variables enter convexly):
  reduced-space schemes can be only first order and "can face severe
  clustering even for unconstrained problems"; the Dür–Horst dual scheme is
  at least first order (Theorem 6.5.17) and second order at KKT points when
  the functions are separable in `x` and `y`, or more generally when the
  mixed Hessian of the Lagrangian vanishes there (Theorem 6.5.23).
- **Li & Grossmann, JOGO 2019** (local card): first-stage spatial B&B with
  Lagrangian and Benders cuts; convergence in the limit (Theorem 1).
- **Robertson, Cheng, Scott, JOGO 91 (2025) 701–742** (abstract; content via
  MUSE-BB and helper's reading of Cheng's 2024 thesis, Chapter 2). Projected
  B&B on first-stage variables with per-scenario relaxations of the value
  functions. Convergence order of the relaxation (Hausdorff sense):

  | Regularity of value functions | CZ (constant per scenario) | LG (Lagrangian, affine) | Ideal (sum of convex hulls) |
  |---|---|---|---|
  | C^2 | 1 | 2 | 2 |
  | locally Lipschitz | 1 | 1 | 1 |
  | lower semicontinuous | < 1 | < 1 | < 1 |

  Li–Grossmann with optimal multipliers equals the ideal relaxation. They
  expect projection-based methods to cluster and suggest looking for other
  decomposition approaches.
- **MUSE-BB: Langiu, Dahmen, Bongartz, Mitsos, JOGO 92 (2025) 837–888**
  (auditor, full preprint, Sections 1.2–1.4 and 5).
  - B&B on the deterministic equivalent "is intrinsically exponential in the
    number of (branched) variables", hence "worst-case exponential runtime in
    the number of scenarios" (informal).
  - Projection-based methods "have not been shown to scale linearly with the
    number of scenarios"; their outer node count "may well depend on the
    number of scenarios".
  - MUSE-BB branches on all variables in one tree; second-stage multisection
    creates `2^{N_s}` children whose bounds come from `2 N_s` scenario
    subproblems. "Like classical B&B algorithms, MUSE-BB searches the full
    variable space. Thus in the worst-case, its runtime is expected to be
    exponential in `N_s`."
  - Dropping nonanticipativity gives first order (Lipschitz data); Section
    5.3: dualizing it with optimal multipliers gives second order at
    unconstrained minimizers satisfying SOSC.
  - Nested B&B repeats work; "nested exponential approaches are considered
    computationally unfavorable" (citing Smith–Pantelides 1997).
- **Zhang & Jiang, arXiv 2605.14273 (2026)** (repository scouting source):
  generalized dual decomposition; Proposition 5: piecewise-constant
  regularizers on a finite partition of the first-stage set are
  `eps`-exact under complete continuous recourse. Two-stage only, no rates.
- **Cifuentes, Dey, Xu, IPCO 2025, arXiv 2411.12085** (repository scouting
  source): tree-decomposition copy formulation (19); decomposable Lagrangian
  duals with zero gap when products of binary coupling variables are
  dualized (Theorem 8). A relaxation result for MIPs, not a search result.
- **Yildiz, Boland, Savelsbergh, Oper. Res. 70 (2022)** (auditor, preprint
  Section 1): decomposition branching for block-angular MIPs; branching
  rules come from block subproblem solutions; one tree; computational only.

### 1.6 Nested decomposition, SDDP and dynamic optimization

A multistage problem with state dimension `d` and horizon `T` is a path (or
scenario tree) whose separators are the states. This is the closest
continuous setting to C2 and C3.

- **Zhang & Sun, Math. Prog. 196 (2022) 935–985, arXiv 1912.13278** (local
  `zhang2022-...`; auditor read the card and theorem text; helper read the
  full text and proofs).
  - Model: scenario tree, nodal cost `f_n(x_{a(n)}, y_n, x_n)` (a tree
    decomposition with `d`-dimensional separators); compact nodal sets;
    exact Lipschitz regularization with a local copy of the parent state
    (Assumption 2; the authors note the penalty may need to grow with `T`);
    nonconvex
    generalized-conjugacy cuts; exact global nodal oracles, whose cost is not
    counted.
  - Theorem 1 (general tree) and Theorem 2 / Corollary 1: at most
    `T (1 + 2LDT/eps)^d` iterations, "O(T^{d+1})" in `T`. Corollary 2: linear
    in `T` for a `(T eps)`-optimal solution. Corollary 3: `T K` for finite
    state sets. Remark 2: independent of the number of nodes per stage.
  - Theorem 4: a deterministic chain with stage-uncoupled `L`-Lipschitz costs
    in `(beta, 2 beta)`, `beta = eps/T`, and a valid but adversarial backward
    oracle forces at least `(DLT/(4 eps))^d` iterations. The helper notes the
    instance is separable: the hardness is inside each `d`-dimensional
    factor, and a flat cut would certify a constant cost at once. It is an
    algorithm-specific bound, not a certificate-size bound.
  - Theorem 5: convex, linear cuts, `d >= 3`, order
    `(DL(T-1)/(8 eps))^{(d-2)/2}`; the instance is stochastic with many nodes
    per stage. DR-MCO (Zhang–Sun, arXiv 2010.06759, Theorem 3; helper)
    gives `Omega(T^{d/2-1})` for a deterministic convex chain, again with
    adversarial oracles.
  - Their closing remark is a belief, not a theorem: "any algorithm that
    relies on local approximation of value functions will face the 'curse of
    dimensionality'".
- **Lan, Math. Prog. 191 (2022) 717–754, arXiv 1912.07702** (helper, full
  text). Convex problems. Theorem 1 (deterministic DDP):
  `sum_t (D_t/delta_t + 1)^{n_t} + 1` iterations; with undiscounted costs and
  absolute accuracy this again depends on `T^n`. SDDP multiplies by the
  number of scenarios. No lower-bound theorem.
- **Forcier & Leclère, J. Convex Anal. 30 (2023)** (helper): deterministic
  bound `(2DL/(eps - gamma))^n (T-1)^{n+1}` (Corollary 23). No lower bounds.
- **SDDiP, SLDP, MIDAS** (helper): Zou–Ahmed–Sun (Math. Prog. 175, 2019)
  Theorems 1–4: binary state expansion, Lagrangian cuts tight at binary
  states, finite convergence; `d(floor(log2(M sqrt(d)/eps)) + 1)` bits per
  node. Ahmed–Cabral–da Costa (Math. Prog. 191, 2022) and Philpott–Wahid–
  Bonnans (MIDAS, 2020): convergence, no rates.
- **Füllner & Rebennack, NC-NBD, Math. Prog. 196 (2022)** (local; helper):
  piecewise-linear MILP relaxations on triangulations refined by longest-edge
  bisection, Lagrangian cuts on a binary expansion of the state;
  Theorem 4.8(c) finite `eps`-termination; no iteration or node bound. Their
  SIAM Review survey (2025, local manuscript) restates Lan and Zhang–Sun and
  lists nonconvex complexity as open.
- **Global dynamic optimization** (helper unless noted).
  - Houska & Chachuat, JOTA 162 (2014), branch-and-lift: finite termination
    (Theorem 2), no node count; the claim that direct methods scale
    exponentially is not proved.
  - Houska & Chachuat, Math. Prog. 173 (2019), "Global optimization in
    Hilbert space": `exp(O(log^2(1/eps)))` iterations independent of the
    number of variables, through spectral decay rather than decomposition.
  - Diedam & Sager, OCAM (2018): branching only on controls in direct
    multiple shooting (Corollary 14).
  - Houska, Villanueva, Chachuat, SINUM (2015) (local): second-order set
    enclosures; order-one enclosures degrade over the horizon.
  - Junge & Osinga, ESAIM COCV 10 (2004) (auditor: abstract): shortest paths
    on a cell graph whose edge weights are minima over cells give a lower
    bound on the value function that is monotone under refinement and
    converges (Propositions 3.1–3.2, Theorem 3.3 per helper); no rates. This
    is the closest control analogue of cell-based value-function minorants.
  - Lincoln & Rantzer (2006), Rantzer (2006) (local): relaxed DP with
    `alpha V* <= V <= beta V*`; no dimension or horizon bounds.
- **Chow & Tsitsiklis, J. Complexity 5 (1989); IEEE TAC 36 (1991)** (helper):
  for discounted stochastic DP on `[0,1]^n` with Lipschitz data and a density
  oracle, any algorithm needs `Omega((1/((1-alpha) eps))^{2n+m})` queries
  under mixing assumptions; multigrid matches this.
- **Borrelli, Baotić, Bemporad, Morari, Automatica 41 (2005)** (auditor:
  abstract): DP combined with multiparametric programming; piecewise affine
  value functions and laws on polyhedral partitions of the state space for
  linear hybrid systems.

### 1.7 B&B tree-size lower bounds, component branching, solvers

**Lower bounds for LP-based MILP B&B with product or path structure.**

- **Basu, Conforti, Di Summa, Jiang, Math. Prog. 198 (2023) 787–810**
  (local `basu2023-complexity-of-branch-and-bound`; auditor checked the
  statements). Theorem 2.2: for maximum stable set on `m` disjoint triangles,
  "any branch-and-bound proof certifying an upper bound of `m` on the
  optimal value has size at least `2^{m+1} - 2`" (variable disjunctions, LP
  bounds). Section 3: "the disconnected components lead to a cartesian
  product of congruent polytopes, which is well-known to be a bad case for
  branch-and-bound". Theorem 3.11: the same bound after adding a center
  vertex adjacent to at most one vertex per triangle.
  **[derived, helper; auditor agrees]** That graph has treewidth 2 and the
  center is a separator of size 1. Branching on the center and then solving
  the `m` triangle components separately needs `O(m)` nodes. This is an
  exponential separation between single-tree B&B and separator branching
  plus component decomposition, on a treewidth-2 MIP. It relies on ties:
  each triangle has three optimal choices, so no child can be pruned.
- **Cheng & Basu, arXiv 2601.23249 (2026)** (auditor: abstract; helper:
  Lemma 3.2 and proof). A product lemma: for `m` copies of a 0/1 block with
  a positive root LP gap and, for every coordinate, two optimal points that
  differ in it, every variable-disjunction tree has at least `2^{m+1} - 1`
  nodes. The tie condition is essential; it does not cover a unique
  nondegenerate minimizer.
- **Gläser & Pfetsch, SODA 2024, arXiv 2308.04320** (local; auditor
  checked). Corollary 9: `T(P x Q) = min(T(P), T(Q))` for B&B proofs that a
  product of polytopes has no integer point. For infeasibility the product
  gives the minimum, not the product; the blow-up is specific to
  optimization with an additive objective.
- **Dey & Shah, Oper. Res. Lett. 50(5) (2022) 430–433, arXiv 2112.03965**
  (local `dey2022-lower-bound-on-size-of`; auditor read the full text).
  Theorem 1: for lot-sizing with `f_j = 1`, `p_j = n - j + 1`, `d_j = 1`, "any
  general branch-and-bound tree that solves this instance has at least
  `2^{(n/2)-1}` leaf nodes" (LP bounds, general split disjunctions on the
  integer variables). The paper notes the Wagner–Whitin DP solves
  lot-sizing in `O(n^2)` (and `O(n log n)`). It does not mention treewidth;
  its formulation uses cumulative-demand constraints.
  **[derived; two helpers made the same observation]** Introducing
  inventory variables `s_i = sum_{k<=i} x_k - d_{1,i}` gives the standard
  formulation with constraints on `(s_{i-1}, x_i, s_i)` and `(x_i, y_i)`, of
  treewidth at most 2. The projection of its LP relaxation onto `(x, y)`
  equals (1b)–(1e), and branching acts on `y` only, so the lower bound
  transfers unchanged. This is an exponential gap between LP-based B&B and
  DP on a bounded-treewidth MILP. The instance also has many optimal
  solutions: by the paper's Claim 1 argument, meeting demand `j` from period
  `j - 1` costs `p_{j-1} = n - j + 2`, the same as opening period `j`.
- **Dey, Dubey, Molinaro** and **Basu et al. Part II** (local; helper): no
  product or treewidth constructions.
- **Liu et al., Math. Prog. 200 (2023)** (Section 1.4): Gurobi node counts
  grow from 14 to 17,965,177 as `n` goes from 10 to 200 (time limit, 2.5%
  gap at `n = 200`) on a tridiagonal problem that their DP solves in
  `O(n^2)`; empirical, binary branching.

**Component detection and decomposition in solvers.**

- **Gamrath, Koch, Martin, Miltenberger, Weninger, MPC 7 (2015)** (helper,
  Section 5 full text): components presolver; the only justification is
  informal ("we would expect a better performance by solving all
  subproblems to optimality one after another"); "Subproblems containing
  only continuous variables are always solved, despite their dimensions."
- **SCIP 4.0 report** (Maher et al., ZIB-Report 17-12; helper, Section
  2.1.3): component detection during B&B; "(locally) fixed variables are
  disregarded when checking the connectivity"; a node is pruned when the sum
  of the sub-SCIP dual bounds exceeds the cutoff. Justified informally by
  "the exponential nature of a branch-and-bound search". No tree-size theorem.
- **SCIP source `cons_components.c`** (auditor checked GitHub master; helper
  checked tags v4.0.0 to v10.1.0). A variable stays in the connectivity
  graph while its local lower bound is below its local upper bound, so a
  continuous variable leaves only when its domain is a point, which spatial
  branching never produces. Component detection during the tree search is
  off by default: `CONSHDLR_PROPFREQ = -1` on master and in 10.x (the SCIP 10
  changelog, per the helper, gives the reason "to avoid unnecessary calls");
  older versions ship `DEFAULT_MAXDEPTH = -1`. The program's SCIP 10 probe
  therefore ran with component detection at presolve only.
- **Gurobi presolve** (Achterberg, Bixby, Gu, Rothberg, Weninger, INFORMS J.
  Comput. 2020; local `achterberg2020-...`, auditor checked Sections
  7.3–7.4). Disconnected components are solved at presolve. "Almost
  disconnected components": a single binary articulation variable is set
  to 0 and to 1, the smaller side is solved, and variables are fixed or
  substituted; such cases "do not appear very often" and give small
  benefit. This is the only solver feature found that resembles branching
  on a separator; it is binary, of size one, and at presolve.
- **SCIP 10 report** (local `hojny2025-...`): the only "component" hit is GCG's
  component bound branching, a Dantzig–Wolfe master branching rule.
- **BARON, Octeract, Couenne:** no documented search-time component
  detection was found (helper; not verified). BARON's multilinear graph
  decomposition (Bao et al., MPC 2015) is for cut separation.
- **Yildiz, Boland, Savelsbergh** decomposition branching: Section 1.5.
- **LaGO** (Nowak 2005): Section 1.5; the relaxation is decomposed, the
  search is not.

**Continuous-domain partial precedents.**

- **Berenguel, Casado, García, Hendrix, Messine, JOGO 56(3) (2013)
  1101–1121**, "On interval branch-and-bound for additively separable
  functions with common variables" (auditor: metadata; helper: abstract).
  The abstract says the effort of interval B&B "increases exponentially
  with the problem dimension in the worst case. For separable functions this
  effort is less", and asks how to design methods when common variables
  occur in the subproblems; it proposes new B&B rules. **This is the closest
  continuous analogue found. Its full text was not read and must be checked
  before any priority claim.**
- **Deussen & Naumann, JOGO 86 (2023), arXiv 2010.09591** (auditor:
  abstract; helper: Sections 1–2). "Structural separators": monotonicity of
  the objective in a scalar function of a subset of variables, verified by
  interval adjoints. Informal count: with `k`-section in every direction a
  node has `k^n` children, reduced to `O(k^{max(|X1|,|X2|)})`. Not a
  node-count theorem, and not a graph separator.
- **Chabert & Jaulin, AIJ 2009** (local; helper): block-by-block bisection
  inside one tree; branching not analyzed.
- **Hübner, Gupte, Rebennack, IJOC 2025** (helper): spatial B&B for separable
  piecewise-linear functions; convergence only.
- **Li & Han, Optimization Online (September 2026)**, "Nonlinear
  optimization over trees with binary coupling decisions" (helper, Sections
  1–1.2; not checked by the auditor): exact parametric DP on trees with
  continuous node variables and binary couplings, polynomial oracle
  complexity; DP, not B&B.

**Decision diagrams and compiled representations.**

- Cooper et al. 2026 (local `cooper2026-...`; helper): Corollary 1,
  valid-antichain DD width `= 2^{pw(G)}`; incomparable with incidence
  treewidth. Davarnia et al. 2026 (local): DDs as relaxations inside a
  single spatial B&B tree; no treewidth statement. No formal separation
  between DD-based and ordinary B&B was found.
- Razgon, arXiv 1411.0264 (helper, abstract): nondeterministic read-once
  branching programs need `n^{Omega(k)}` on CNFs of treewidth `k`.
  Amarilli, Capelli, Monet, Senellart, ToCS 2019 (abstract): DNNF size
  exponential in treewidth for bounded-degree monotone CNFs. Itsykson et
  al., ECCC TR19-178 (abstract): regular resolution of Tseitin formulas
  needs `2^{Omega(tw/log n)}`.

## 2. Verdicts

### C1. Single-tree spatial B&B is exponential in n at bounded treewidth

**Partially known.**

- Known in estimate form: near a nondegenerate minimizer, relaxations with
  a large second-order prefactor give box counts exponential in `n`
  (Neumaier 2004, Section 15; Wechsung–Schaber–Barton 2014, Theorems 1–2
  and Section 3, threshold `K <= 9 lambda_1/4`; alphaBB has `K <= alpha n/4`).
  These estimates are upper estimates that assume sharp convergence-order
  bounds and ignore structure; they are not lower bounds for every tree.
- Stated informally for two-stage structure (a star): Kannan (2018, Section
  2.3.2.3), Cao–Zavala (2019), MUSE-BB (2025, Section 1.2). No proof.
- Proved for LP-based MILP B&B at treewidth 2: Basu et al. (Math. Prog.
  2023) Theorems 2.2 and 3.11, at least `2^{m+1} - 2` nodes on `m` triangles
  (with or without a center vertex); Dey–Shah (Oper. Res. Lett. 2022)
  Theorem 1, `2^{n/2-1}` leaves for every general-split tree on a
  lot-sizing family that DP solves, which transfers to a treewidth-2
  inventory formulation (**[derived]**, Section 1.7); Cheng–Basu (2026)
  Lemma 3.2, a general product lemma. These are the closest rigorous
  precedents. All use instances with many optimal solutions (ties), which
  keep both children of every branching alive; the product lemma needs
  them explicitly. For infeasibility proofs, products give the minimum
  tree size (Gläser–Pfetsch Corollary 9), so the blow-up comes from the
  additive objective.
- Proved in the repository for relaxations whose gap is at least
  `alpha q_B` (Theorem 3.1 of the constrained note). That result already
  covers separable problems, so C1's content is not specific to paths.
- Not found: a rigorous lower bound, for every adaptive spatial B&B tree,
  with factorable relaxations that are exact on faces (McCormick, per-factor
  convex envelopes) on a bounded-treewidth continuous problem with a unique
  nondegenerate minimizer.

### C2. Decomposition-aware B&B needs poly(n) * g(w, eps) work

**Partially known.**

- Worst case, by other algorithms: Bienstock–Muñoz, Theorems 4 and 15
  (LP size `O((2 pi/eps)^{omega+1} n log(pi/eps))`, tolerance scaled by
  coefficient norms); grid DPOP for continuous DCOPs (Hoang et al. 2020,
  error `|F| m delta`, messages `O(d^w)`); Zhang–Sun Corollary 1
  (`T (1 + 2LDT/eps)^d` iterations of nested decomposition with nonconvex
  cuts on a stage or scenario tree); Lan Theorem 1 (convex, deterministic,
  `sum_t (D_t/delta_t + 1)^{n_t} + 1`).
- Algorithm template, discrete: AND/OR branch-and-bound with context
  caching, `O(n k^w)` (Marinescu–Dechter 2009, Theorem 6); BTD+ with
  inherited upper bounds and recorded lower bounds per separator
  assignment, `O(k d^{w+1})` nodes (de Givry–Schiex–Verfaillie 2006);
  mini-bucket and cost-shifting heuristics as separator lower-bound
  functions.
- Algorithm template, continuous, depth one (star): branch only on
  first-stage variables with Lagrangian or relaxation bounds (Dür–Horst 1997;
  Cao–Zavala 2019; Kannan 2018; Li–Grossmann 2019). Convergence theorems
  only; MUSE-BB says these methods "have not been shown to scale linearly
  with the number of scenarios".
- Convergence order of child bounds: constant child bounds are at most
  first order; Lagrangian (affine) child bounds are second order only when
  value functions are C^2 and multipliers are optimal (Robertson–Cheng–Scott
  2025; MUSE-BB Section 5.3; Kannan Theorem 6.5.23).
- Not found: (i) a recursive spatial B&B over a general tree decomposition,
  with minorants on separator cells, that has a complexity theorem; (ii) any
  instance-dependent bound like `O(n log(1/eps))` at a nondegenerate
  minimizer. Nearest: exact parametric DP linear in `n` for convex MIQP with
  indicators (Bhathena et al.); exponential decay of sensitivity in
  graph-structured NLPs (Shin–Anitescu–Zavala 2022, local result).
- **Caution on the statement.** With absolute accuracy `eps` on `F` and
  factors normalized one by one, `poly(n) * g(w, eps)` with a polynomial
  independent of `w` is false under ETH (**[derived]**: encode a domain-`d`
  binary CSP on a fixed graph by 1-Lipschitz bilinear-interpolated penalty
  tables of height `1/d`; rounding shows `F < 1/(4d)` implies satisfiable;
  `d` disjoint copies give a constant gap at `n = |V(G)| d`; then apply
  Marx 2010 or Cohen-Addad et al. Theorem 2.7). Zhang–Sun's bound is also of
  the form `T^{d+1} eps^{-d}`. The worst-case claim must use accuracy
  relative to the total scale (as Bienstock–Muñoz do) or be stated as
  `(C n/eps)^{O(w)}`. If `C` in the program's `poly(n) (C/eps)^{O(w)}` is
  allowed to grow with `n` (for example, the sum of the factors' Lipschitz
  constants), the statement already has this form and is consistent. The
  instance-dependent claim is not affected.

### C3. Matching lower bounds in the treewidth

**Partially known.**

- Any algorithm, discrete: under ETH, no `f(G) n^{o(k/log k)}` algorithm for
  binary CSP (Marx 2010); for every fixed graph, no `|D|^{o(tw/log tw)}`
  (Cohen-Addad et al., Theorem 2.7, helper-verified). The continuous transfer
  above gives `(1/eps)^{Omega(w/log w)}` running-time bounds under ETH; we
  did not find it published.
- Approximation and formulation size: Faenza–Muñoz–Pokutta Theorem 3.6
  (fixed-`eps` QCQP approximation superpolynomial in treewidth unless
  `NP ⊆ BPP`), Theorem 4.24 (SDP extension complexity nearly exponential in
  treewidth); Bienstock–Muñoz Appendix A (at treewidth 2, `1/eps` cannot be
  replaced by `log(1/eps)` unless `P = NP`) and the stated `2^omega m`
  oracle-query bound for binary problems.
- Algorithm-specific: Zhang–Sun Theorem 4, `(DLT/(4 eps))^d` iterations,
  and Theorem 5, `(T/eps)^{d/2-1}` for convex problems with linear cuts;
  both use separable instances and adversarial but valid oracles, so the
  hardness sits inside one `d`-dimensional factor, not in the coupling.
  Chow–Tsitsiklis (1989, 1991) give `Omega((1/((1-alpha) eps))^{2n+m})` for
  any algorithm, for discounted stochastic DP with a density oracle.
- Proof complexity (secondary): tree-like resolution of Tseitin formulas
  needs `2^{Omega(tw)}` (Galesi–Talebanfard–Torán; helper, not verified).
- Not found: a lower bound `(C/eps)^{Omega(w)}` on the size of decomposition
  certificates, or of any B&B certificate, for factors of small arity. A
  helper argument (anchored ANOVA decomposition) indicates that with known
  factor scopes, value-oracle query counts are polynomial, so such a bound
  cannot come from an information argument; it must come from the
  certificate structure or from complexity assumptions.

### C4. Exponential separation between single-tree and decomposition-aware B&B

**Partially known in discrete and MILP settings; not found for spatial
B&B.**

- Unpruned search spaces: OR tree `O(k^n)`, tight for fully consistent
  models, versus AND/OR `O(n k^m)` and `O(n k^w)` (Dechter–Mateescu,
  Theorems 30, 67, 82).
- Model counting: #DPLL is exponential on branch-width-0 formulas, while
  component caching is `n^{O(1)} 2^{O(w)}` (Bacchus–Dalmao–Pitassi, ECCC
  Theorem 4; JAIR Theorems 1–3).
- Compiled representations: OBDD versus SDD at bounded treewidth (Razgon
  2014; helper).
- Pruned MILP optimization: Basu et al. Theorem 3.11 (single-tree lower
  bound `2^{m+1} - 2`) with the `O(m)` upper bound for branching on the
  size-1 center separator and then solving components (**[derived]**) is an
  exponential separation between two LP-based B&B schemes at treewidth 2.
  Dey–Shah plus the inventory reformulation gives an exponential gap
  between LP-based B&B and DP at treewidth 2. Both instances have many
  optimal solutions. In Basu et al. the separator is binary, so fixing it
  creates components that existing component detection can exploit; in
  Dey–Shah the fast side is a specialized DP (Wagner–Whitin), not a B&B.
- Counter-evidence a referee may raise: search tied to a fixed decomposition
  can lose super-polynomially to dynamic ordering (Bacchus–Dalmao–Pitassi,
  JAIR Theorems 6–7), and decomposition can weaken bounds (Kitching–Bacchus;
  de Givry et al.).
- Not found: a separation theorem between single-tree spatial B&B and a
  decomposition-aware B&B that use the same relaxation family, for
  continuous or mixed-integer nonconvex problems with continuous
  separators, or any separation at a unique nondegenerate minimizer. All
  statements that full-space B&B is exponential in the number of blocks or
  scenarios in the global-optimization literature are informal or
  empirical (Kannan 2018; Cao–Zavala 2019; MUSE-BB 2025; Berenguel et al.
  2013 abstract; Deussen–Naumann 2023).

## 3. Strongest competitors and how the program must differ

1. **AND/OR branch-and-bound and BTD+ (AI/CP).** A referee will say that
   C2 and C4 are the continuous analogue of Dechter–Mateescu Theorem 30 and
   AOBB-C/BTD+. To be original the program must:
   - handle continuous separators, where exact values never repeat, so
     caching per assignment is replaced by cell partitions of separator
     boxes with minorants valid on each cell (bucket elimination's
     Section 2.3 warning shows exact continuous messages are not
     width-bounded);
   - prove lower bounds for *pruned* trees with a fixed relaxation family
     and adaptive branching, not sizes of unpruned search spaces;
   - control error accumulation across bags (the `eps/n` split that appears
     in grid DPOP and in Zhang–Sun);
   - give instance-dependent rates, which have no discrete counterpart.
2. **Zhang–Sun (nested decomposition with nonconvex cuts).** This already
   gives a recursive global method on stage or scenario trees with
   `T (1 + 2LDT/eps)^d` iterations and algorithm-specific lower bounds in
   `d`. The program must not present the worst-case `(C/eps)^{O(w)}` bound
   as new. It can differ by: general tree decompositions of a factor
   hypergraph (bags, not stage states); spatial branching on separator
   cells with relaxation-based bounds instead of cuts from global nodal
   oracles; counting all local work; instance-dependent `log(1/eps)`
   bounds; and lower bounds for all certificates in a model, not for one
   algorithm with adversarial oracles.
3. **Two-stage decomposition B&B with convergence-order theory
   (Cao–Zavala; Kannan; Li–Grossmann; MUSE-BB; Robertson–Cheng–Scott).**
   The program's scheme is a recursive version of a projection-based method.
   Robertson–Cheng–Scott's order table then applies at every level:
   constant child bounds are first order and will cluster in the separator
   cells; affine Lagrangian bounds are second order only with C^2 value
   functions and optimal multipliers. To obtain `O(n log(1/eps))` the
   program must prove that (near) second-order child minorants are
   computable at a nondegenerate minimizer, with inexact multipliers, and
   that cells far from the optimum are pruned despite nonsmooth value
   functions there. It should also cover single trees of MUSE-BB type in
   the lower bound: MUSE-BB represents `2^{N_s}` children implicitly through
   separable bounds, so the cost measure (leaves, nodes, or bounding work)
   must be fixed before claiming a separation.
4. **Bienstock–Muñoz (theory).** Worst-case polynomial-size LPs for
   bounded treewidth already exist, with scaled accuracy. The program's
   worst-case statement is only a B&B-certificate version of a known
   complexity bound.
5. **MILP tree-size lower bounds (Basu et al. 2023; Dey–Shah 2022;
   Cheng–Basu 2026).** Exponential lower bounds for LP-based B&B on
   treewidth-2 instances exist, and Basu et al. Theorem 3.11 already yields
   an exponential separation from separator branching plus components. A
   referee can say C1 and C4 are "the product argument again". The program
   must show what is new: separators are continuous and never fixed, so
   components never appear and existing component detection cannot help;
   the minimizer is unique and nondegenerate, so the tie mechanism used by
   Basu et al. and Cheng–Basu is unavailable and the lower bound must come
   from the relaxation gap instead; and the decomposition-aware side is a
   B&B using the same relaxations.
6. **Interval B&B for additively separable functions with common variables
   (Berenguel et al. 2013).** Per its abstract, it asks how to design
   interval B&B when an additively separable objective has subfunctions that
   share variables (the helper's reading suggests two subfunctions). Its
   full text was not read. It must be read before claiming that no
   continuous precedent exists.

## 4. Positioning suggestions

- Cite the discrete antecedents up front (Dechter–Mateescu; Marinescu–
  Dechter; de Givry et al.; Bacchus–Dalmao–Pitassi) and say plainly that
  the discrete separation for unpruned search is known and easy. Present
  the contribution as the continuous, relaxation-based, pruned version.
- Make the instance-dependent pair the headline: at a unique nondegenerate
  minimizer, decomposition-aware B&B with second-order child minorants needs
  `O(n log(1/eps))` (or `O(n log(n/eps))`) local work, while every single
  tree with the same per-factor relaxations needs `exp(Omega(n))` leaves.
  No antecedent was found for either half in the continuous setting.
- Present worst-case bounds as consistent with Bienstock–Muñoz, grid DP and
  Zhang–Sun, and fix the accuracy model explicitly (relative accuracy, or
  `(Cn/eps)^{O(w)}`), because of the ETH obstruction in Section 2.
- Fix the relaxation family for both sides of the separation. A referee
  will note that non-factorable relaxations (convexity detection on the
  aggregated objective, SDP) remove the effect on the probe instance, whose
  convex variant is solved at the root. The separation is about search
  structure only if both algorithms use the same bounds.
- Frame the star case as an answer to the question MUSE-BB raises (linear
  scaling in the number of scenarios) under explicit nondegeneracy, and
  cite Robertson–Cheng–Scott for why constant child bounds fail.
- For C3, aim at certificate-size lower bounds; give the ETH transfer as a
  remark, and cite Marx, Faenza–Muñoz–Pokutta and Zhang–Sun for the known
  parts.
- Cite Basu et al. (Theorems 2.2, 3.11), Dey–Shah (with the treewidth-2
  reformulation) and Cheng–Basu as the MILP precedents for C1/C4, and state
  the two differences: no ties (a unique nondegenerate minimizer), and
  continuous separators that are never fixed.
- Read Berenguel et al. (JOGO 2013) in full before submission; it is the
  closest continuous precedent found and was checked only at abstract level.
- In computations, note that SCIP's in-tree component detection is off by
  default (`CONSHDLR_PROPFREQ = -1`). It cannot help on paths, where
  components never appear, but separable or star-like baselines should be
  run with it enabled, and the text should say so.
- Do not claim the first decomposition-aware B&B. Claim, if proved, the
  first complexity analysis and separation for spatial B&B along tree
  decompositions.

## 5. Source log

Depth codes: **F** full text or the named sections read; **T** theorem
statements and surrounding text only; **A** abstract or metadata only;
**C** local summary card only; **S** secondary (described in another
source). "Auditor" means read by the author of this note; "helper" means
read by a delegated agent, with the auditor's spot-check noted.

### Read by the auditor

| Source | Location | Depth | What was checked |
|---|---|---|---|
| Dechter & Mateescu, AIJ 171 (2007) | https://www.ics.uci.edu/~dechter/publications/r126.pdf | T (Secs. 4–6; helper read in full) | Thms 30, 38, 67, 69, 81, 82; Prop. 37; Cor. 68; Rem. 70; no pruning analysis |
| Bacchus, Dalmao, Pitassi, ECCC TR03-003 | https://eccc.weizmann.ac.il/report/2003/003/download | T | Thm 4 (branch width 0, #DPLL exponential); Thms 5–7 exist (formulas lost in extraction) |
| de Givry, Schiex, Verfaillie, AAAI 2006 | https://miat.inrae.fr/degivry/Schiex06a.pdf | T | `O(d^h)`, `O(d^{w+1})`, BTD+ `O(k d^{w+1})` |
| Dey & Shah, arXiv 2112.03965 | https://arxiv.org/abs/2112.03965 | F | Thm 1, formulation (1), DP remark; no treewidth discussion. Venue Oper. Res. Lett. 50(5) (2022), from the local card |
| Langiu, Dahmen, Bongartz, Mitsos (MUSE-BB), JOGO 92 (2025) | https://optimization-online.org/wp-content/uploads/2024/06/MUSE_BB_preprint.pdf; IDEAS abstract | F (Secs. 1.2–1.4, 5 intro) | scaling statements, PBDA critique, multisection, convergence orders |
| Robertson, Cheng, Scott, JOGO 91 (2025) | https://ideas.repec.org/a/spr/jglopt/v91y2025i4d10.1007_s10898-024-01458-1.html | A (+ S via MUSE-BB) | orders for CZ and LG |
| Nowak, habilitation 2005 (LaGO) | https://edoc.hu-berlin.de/items/463830e0-3352-48b4-b538-e5e7adf6bffa/full | T (grep) | Sec. 2.3 splitting, Alg. 13.1, Sec. 13.4 branching |
| Yildiz, Boland, Savelsbergh, Oper. Res. 70 (2022) | https://optimization-online.org/wp-content/uploads/2018/08/6788.pdf | F (Sec. 1) | decomposition branching setting |
| Dür & Horst, JOTA 95 (1997) | https://ideas.repec.org/a/spr/joptap/v95y1997i2d10.1023_a1022687222060.html | A | duality gap vanishes under partitioning |
| Marx, Theory of Computing 6 (2010) | https://theoryofcomputing.org/articles/v006a005/abstract.txt | A | ETH lower bound for binary CSP |
| Borrelli et al., Automatica 41 (2005) | search snippet | A | multiparametric DP |
| Junge & Osinga, ESAIM COCV 10 (2004) | https://www.numdam.org/item/COCV_2004__10_2_259_0 | A | cell-graph value-function bounds |
| Hoang et al., AAMAS 2020 | https://arxiv.org/abs/1905.13275 | A | exact and approximate continuous DCOP algorithms |
| Korda, Magron, Ríos-Zertuche | https://arxiv.org/abs/2303.14824 | A | clique-size-dependent rates |
| Nie, Qu, Tang, Zhang | https://arxiv.org/abs/2406.06882 | A | tightness characterization |
| Cohen-Addad et al., JACM 2021 | https://arxiv.org/abs/1903.08603 | A | paper exists; Thm 2.7 read by helper only |
| Shin, Anitescu, Zavala, SIOPT 32 (2022) | arXiv 2101.03067 (search snippet) | A | EDS under SSOSC and LICQ. (arXiv 2101.06350 is the related Shin–Zavala IFAC 2021 paper) |
| Wechsung, Schaber, Barton, JOGO 58 (2014) | local `wechsung2014-the-cluster-problem-revisited` | F | Assumption 1, Thms 1–2, Sec. 3 threshold |
| Du & Kearfott, JOGO 5 (1994) | local `du1994-the-cluster-problem-in-multivariate` | T | Thms 1–2 are upper bounds; Remarks 1–6 |
| Kannan & Barton, JOGO 69 (2017) | local `kannan2017-the-cluster-problem-in-constrained` | T (intro) | literature summary, interior-box assumption |
| Kannan, MIT thesis 2018 | local `kannan2018-algorithms-analysis-and-software-for` | T (Secs. 1, 2.3.2.3, 6 headers) | reduced-space motivation and clustering remark |
| Neumaier, Acta Numerica 13 (2004) | local `neumaier2004-complete-search-in-continuous-global` | T (grep) | separability remarks, LaGO entry |
| Bienstock & Muñoz, SIOPT 28 (2018) | local `bienstock2018-lp-formulations-for-polynomial-optimization` | T | Thms 4, 7, 9, 15; Sec. 1 remarks; Appendix A statement |
| Faenza, Muñoz, Pokutta (2022) | local `faenza2022-new-limits-of-treewidth-based` | C | Thms 3.3, 3.6, extension complexity |
| Zhang & Sun (2022) | local `zhang2022-stochastic-dual-dynamic-programming-for` | C + T | Cor. 1, Thms 4–5 text |
| Li & Grossmann, JOGO (2019) | local `li2019-a-generalized-benders-decomposition-based` | C | setting, Thm 1 |
| Liu, Fattahi, Gómez, Küçükyavuz, Math. Prog. 200 (2023) | local `liu2022-a-graph-based-decomposition-method` | T | Table 2 node counts |
| Xu et al., arXiv 2608.01385 | local `xu2026-coordinate-optimality-reformulation-for-mixed` | T | Props. 2–3, related-work paragraph |
| Udell & Boyd (2016) | local `udell2016-bounding-duality-gap-for-separable` | C | duality-gap bound for separable problems (background) |
| Lehmann, Grastien, Van Hentenryck (2016) | local `lehmann2016-ac-feasibility-on-tree-networks` | C | NP-hardness on a star (the hub constraint has unbounded arity) |
| Cifuentes, Dey, Xu, arXiv 2411.12085 | repo `research-20260928b/scouting/decomposition-duality-gaps/sources/` | T (Sec. 3) | formulation (19), Thm 8 |
| Zhang & Jiang, arXiv 2605.14273 | same folder | T | Assumptions 1–2, Prop. 5, Thm 3 |
| SCIP Optimization Suite 10 report | local `hojny2025-the-scip-optimization-suite-10` | T (grep "component") | no component-detection text; GCG component bound branching is a Dantzig–Wolfe rule |
| Basu, Conforti, Di Summa, Jiang, Math. Prog. 198 (2023) | local `basu2023-complexity-of-branch-and-bound` | T | Thms 2.2, 3.11 and proof sketch; Sec. 3 product remark |
| Gläser & Pfetsch, SODA 2024 | local `glaser2024-sub-exponential-lower-bounds-for` | T | Lemma 8, Cor. 9 |
| Achterberg, Bixby, Gu, Rothberg, Weninger, INFORMS J. Comput. (2020) | local `achterberg2020-presolve-reductions-in-mixed-integer` | T | Secs. 7.3–7.4 components and almost disconnected components |
| SCIP `cons_components.c` | https://raw.githubusercontent.com/scipopt/scip/master/src/scip/cons_components.c | T | `CONSHDLR_PROPFREQ -1`, `DEFAULT_MAXDEPTH INT_MAX`, local-bound connectivity test |
| Berenguel, Casado, García, Hendrix, Messine, JOGO 56(3) (2013) | https://ideas.repec.org/a/spr/jglopt/v56y2013i3p1101-1121.html | A (search summary) | topic and bibliographic data; full text not read |
| Deussen & Naumann, JOGO (2023) | https://arxiv.org/abs/2010.09591 | A | structural separators |
| Cheng & Basu | https://arxiv.org/abs/2601.23249 | A | paper exists; Lemma 3.2 read by helper only |
| Lan, Math. Prog. (2022) | https://arxiv.org/abs/1912.07702 | A | deterministic variants mildly increase with `T` |
| Kannan thesis, Ch. 1 and Sec. 2.3.2.3 | local | T | "worst-case exponential increase in solution times with a linear increase in the number of scenarios" |

### Read by helpers (auditor spot-checks in brackets)

- Helper 1 (discrete and CP): Marinescu & Dechter AIJ 173 (2009, two papers)
  and Constraints 15 (2010) [F by helper]; Kask & Dechter AIJ 129 (2001)
  [F]; Ihler et al. UAI 2012 [A]; Gogate & Dechter hybrid networks [A];
  Jégou & Terrioux AIJ 146 (2003) [F]; Jégou & Terrioux ECAI 2004 [F];
  Allouche et al. CP 2015 [F Sec. 4]; Sanchez et al. IJCAI 2009 [A];
  Kitching & Bacchus CP 2008 / IJCAI 2009 [skim]; Bacchus, Dalmao, Pitassi
  JAIR 34 (2009), arXiv 1401.3458 [T; auditor checked ECCC Thm 4]; Darwiche
  AIJ 2001 [A]; Beame et al. TOCT 2010 [A]; Razgon KR 2014 [T]; Amarilli et
  al. ToCS 2020 [A]; Huang & Darwiche JAIR 2007 [A]; Dechter AIJ 113 (1999)
  [T]; Morin & Marsten 1976, Ibaraki 1977, Kumar & Kanal 1983, Puchinger &
  Stuckey 2008, Freuder 1982, Dechter & Pearl 1989 [A or metadata];
  Bayardo & Miranker AAAI 1996 [partial]; Faltings 1994 and Vu et al. 2009
  [local]; Sam-Haroud & Faltings 1996 [A]; Bliek et al. 1998, Neveu et al.
  2010 [T]; Hoang et al. 2020 [T; auditor checked abstract]; Ye, Say,
  Sanner 2018 [A]; Capelli et al. [local]. Not accessed: Bertelè–Brioschi
  (1972).
- Helper 2 (treewidth and polynomial optimization): Bienstock & Muñoz
  [F incl. Appendix A]; Bienstock & Özbay 2004 [A]; Kolman & Koutecký 2015
  [T]; Wainwright & Jordan TR 671 [F Secs. 4–5]; Laurent 2009 [Secs. 8.1–8.2];
  Waki et al. 2006, Lasserre 2006 [local F]; Korda et al. [Sec. 1.2; auditor
  checked abstract]; Magron 2026 [local A]; CS-TSSOS [A]; Nie 2014 [A]; Nie,
  Qu, Tang, Zhang [Secs. 3–4, Ex. 6.7; auditor checked abstract]; Faenza et
  al. [F]; Aboulker et al. 2019 [T]; Del Pia & Di Gregorio [local T];
  Capelli, Boros, Clausen, Choudhary–Dey–Sahinidis, Herrmann [A or T];
  Bhathena et al. arXiv 2603.02103 [T]; Xu et al. [T; auditor checked];
  Khajavirad 2026 [T]; Cohen-Addad et al. Thm 2.7 [F by helper];
  Lokshtanov–Marx–Saurabh [recalled, not checked]; Kandasamy 2015,
  Rolland 2018, Ziomek 2023 [A].
- Helper 3 (decomposition-based global optimization): Cao & Zavala preprint
  (Optimization Online 2017/08/6164) [F]; Kannan thesis [Secs. 2.3.2.3, 3,
  6.1–6.6, App. A]; Cheng PhD thesis (Georgia Tech 2024), Ch. 2, as a
  stand-in for Robertson et al. [F; theorem numbers are the thesis's];
  MUSE-BB [F; auditor also F]; Karuppiah & Grossmann 2008 [S], 2006 [local];
  Kesavan et al. 2004 [C]; Nowak et al. 2018 [A]; Muts et al. 2020 [local];
  Epperly & Pistikopoulos 1997 [S via Kannan]; Li, Tomasgard, Barton [S];
  Ogbe & Li 2019, Belyak 2025, Liu et al. 2022, Murray et al. 2021 [local];
  Plasmo.jl [A]; Shin–Anitescu–Zavala [A]; Bynum et al. graph-partitioned
  OBBT (Optimization Online 2021/02/8248) [A]; Alpine [A]; Dey & Shah [A;
  auditor F]; Davarnia et al. arXiv 2409.19794 [A]; Mitrai & Daoutidis [A].
  No graph-partitioned OBBT paper by Sundar et al. was found.
- Helper 4 (nested decomposition and dynamic optimization): Zhang & Sun
  [F incl. App. A.3–A.4]; DR-MCO arXiv 2010.06759 Thm 3 [T]; Lan [F];
  Ju & Lan arXiv 2303.02024 [A]; Zou, Ahmed, Sun [F preprint]; Ahmed,
  Cabral, da Costa arXiv 1905.02290 [F]; MIDAS HAL report [F]; Füllner &
  Rebennack 2021, 2022, 2024, 2025 [local]; Houska & Chachuat 2014 [F
  preprint], 2019 [T]; Diedam & Sager 2018 [T]; Houska, Villanueva,
  Chachuat 2015 [local]; Villanueva et al. 2015 [T]; Chachuat et al. 2005
  [local]; Scott & Barton [A]; Lincoln & Rantzer, Rantzer [local]; Junge &
  Osinga [T; auditor A]; Chow & Tsitsiklis 1989, 1991 [T]; Forcier &
  Leclère 2023 [T]; Barros et al. arXiv 2606.10203 [title only].
- Helper 5 (components, interval methods, B&B lower bounds, recent work):
  SCIP 4.0 report Sec. 2.1.3 [F]; SCIP `cons_components.c` tags v4.0.0 to
  v10.1.0 and CHANGELOG [T; auditor checked master]; Gamrath et al. MPC 2015
  Sec. 5 [F]; Gamrath PhD thesis 2020 [grep]; Achterberg et al. 2020 [T;
  auditor checked]; Bao et al. MPC 2015 [A]; Neumaier 2004, Schichl &
  Neumaier 2005, Vu et al. 2009, Chabert & Jaulin 2009 [local]; Neveu,
  Trombettoni, Chabert 2010 [grep]; Berenguel et al. 2013 [A]; Deussen &
  Naumann 2023 [Secs. 1–2]; Hübner, Gupte, Rebennack IJOC 2025 [grep];
  Basu et al. 2023 [T; auditor checked]; Cheng & Basu 2026 [Lemma 3.2 and
  proof]; Gläser & Pfetsch 2024 [T; auditor checked]; Dey & Shah [T];
  Dey, Dubey, Molinaro and Basu et al. Part II [local]; de Givry et al.
  JFPC 2006 [Sec. 3]; Razgon arXiv 1411.0264, Amarilli et al. 2019,
  Itsykson et al. TR19-178 [A]; local `ghaddar2023-...`, `kronqvist2026-...`,
  `davarnia2026-...`, `cooper2026-...`, `lyu2023-...`, `faenza2022-...`
  [grep]; Bergman, Cire, van Hoeve, Hooker MIP 2012 poster [A]; Li & Han,
  Optimization Online 2026 [Secs. 1–1.2]; Subramanian et al. arXiv
  2605.30617, Xu et al. arXiv 2603.01267, Hespanhol et al. arXiv 1903.09117
  [A]. Not accessed: Berenguel et al. full text, Gläser's dissertation,
  Bergman et al. CPAIOR 2012.

URLs used by the helpers (local sources are named by slug above):
https://ics.uci.edu/~dechter/publications/ (r94, r76A, r126, r151, r153a,
r154); https://cdn.aaai.org/AAAI/1996/AAAI96-045.pdf;
https://pageperso.lis-lab.fr/cyril.terrioux/en/publis/aij2003.pdf;
https://miat.inrae.fr/degivry/Schiex06a.pdf;
https://miat.inrae.fr/degivry/Givry06a.pdf;
https://miat.inrae.fr/schiex/Doc/Export/hbfs.pdf;
https://arxiv.org/pdf/1401.3458; https://arxiv.org/abs/1308.3829;
https://arxiv.org/abs/1411.0264; https://arxiv.org/abs/1811.02944;
https://arxiv.org/abs/1905.13275; https://arxiv.org/abs/1501.00288;
https://arxiv.org/abs/1502.05361;
https://statistics.berkeley.edu/sites/default/files/tech-reports/671.pdf;
https://homepages.cwi.nl/~monique/files/moment-ima-update-new.pdf;
https://arxiv.org/abs/2303.14824; https://arxiv.org/abs/2005.02828;
https://arxiv.org/abs/1206.0319; https://arxiv.org/abs/2406.06882;
https://arxiv.org/abs/1807.02551; https://arxiv.org/abs/1806.00541;
https://arxiv.org/abs/2410.23045; https://arxiv.org/abs/2603.02103;
https://arxiv.org/abs/1903.08603; https://arxiv.org/abs/2102.01977;
https://optimization-online.org/2017/08/6164/;
https://repository.gatech.edu/server/api/core/bitstreams/cffb2fae-7cba-4f0e-8bd9-473948eba737/content
(Cheng thesis); https://optimization-online.org/wp-content/uploads/2024/06/MUSE_BB_preprint.pdf;
https://skoge.folk.ntnu.no/prost/proceedings/aiche-2006/data/papers/P55302.HTM;
https://research.wur.nl/en/publications/decomposition-based-inner-and-outer-refinement-algorithms-for-glo/;
https://arxiv.org/abs/2006.05378 (Plasmo.jl); https://arxiv.org/abs/2101.03067;
https://optimization-online.org/2021/02/8248/ (Bynum et al.);
https://arxiv.org/abs/1707.02514 (Alpine); https://arxiv.org/abs/2409.19794;
https://arxiv.org/pdf/2310.07068; https://arxiv.org/abs/1912.13278;
https://arxiv.org/abs/2010.06759; https://ar5iv.labs.arxiv.org/html/1912.07702;
https://arxiv.org/abs/2303.02024; https://optimization-online.org/2016/05/5436/
(SDDiP); https://arxiv.org/abs/1905.02290; HAL hal-01401950 (MIDAS);
https://optimization-online.org/wp-content/uploads/2017/03/5895.pdf (SCIP
4.0); https://opus4.kobv.de/opus4-zib/files/4253/ZR-13-48.pdf (Gamrath et
al.); https://www.lirmm.fr/~trombetton/publis/ibb_constraints_2010.pdf;
https://arxiv.org/abs/2010.09591; https://arxiv.org/abs/2601.23249;
https://arxiv.org/abs/2308.04320; https://arxiv.org/abs/2112.03965.

## 6. Searches that returned nothing relevant

These searches found no source bearing on C1–C4 beyond those listed above.
An unsuccessful search does not establish novelty.

- Auditor: `"tree decomposition" "spatial branch-and-bound" nonconvex`;
  `arXiv 2025 treewidth global optimization nonconvex branch-and-bound
  exponential separation dynamic programming separator`; `global
  optimization continuous Markov random field MAP branch-and-bound
  tree-structured dynamic programming interval bounds certified optimal`
  (discrete MAP only).
- Helper 5: `"treewidth" "spatial branch-and-bound"` (only algorithms that
  compute treewidth); `"tree decomposition" MINLP OR nonconvex
  "branch-and-bound" separator variables branching` (2024–2026); spatial B&B
  node counts exponential in dimension with sparse structure; factor-graph
  global optimization by B&B (SLAM, junction tree); globally optimal MAP in
  continuous graphical models with interval bounds; `"nonserial dynamic
  programming" continuous interval global optimization`; BARON, Octeract,
  Couenne "independent components" or "disconnected components"; decision
  diagram versus MIP B&B separation theorems.
- Helpers 1–4: no continuous or hybrid AND/OR branch-and-bound; no
  graph-partitioned OBBT paper by Sundar et al. (the related work is by
  Bynum et al.); no lower-bound theorem in Lan (2022); no proof that spatial
  B&B grows exponentially with the horizon in dynamic optimization; no
  comparison of sparse moment–SOS hierarchies with B&B node counts.

Commands run for this note (targeted only): `grep`, `sed`, `awk` on local
full texts under `literature/papers/` and on the repository's 2026-09-28
scouting sources; `curl` and `pdftotext` on the PDFs named in Section 5
into `/tmp/auditor_lit/`. No project-wide verification and no CI
inspection.
