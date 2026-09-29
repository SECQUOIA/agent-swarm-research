# Scout report: tree-size theory of branch-and-bound for convex MINLP

Area: `bb-tree-size-convex`. Date: 2026-09-28. Status: scouting report with
first-pass proofs and small floating-point computations. Nothing here has been
independently reviewed. Scratch code and result files are in
[`bb-tree-size-convex/`](bb-tree-size-convex/).

## Summary

The theory of branch-and-bound (B&B) tree sizes is almost entirely linear. For
mixed-integer linear programs there are random-instance polynomial bounds
(Dey–Dubey–Molinaro; Borst–Dadush–Huiberts–Tiwari; Borst–Dadush–Mikulincer),
exponential lower bounds for general split disjunctions (Dadush–Tiwari;
Dey–Dubey–Molinaro; Gläser–Pfetsch), and branch-versus-cut separations (Basu,
Conforti, Di Summa and Jiang). For convex MINLP with nonlinear node relaxations
(NLP, conic, perspective), the bounded search found only two tree-size
statements. The first is Basu et al.'s extension of Dash's "cutting planes are
at least as good as variable branching" to convex 0/1 sets, with an `eps`
slack. The second is a remark by Hijazi–Bonami–Ouorou that their
outer-approximation example also needs `2^n` nodes in an OA branch-and-cut.
No node-count theory was found for random convex MIQPs or for
perspective relaxations in sparse regression. The communications literature on
sphere decoding is the nearest analogue, but it covers only fixed-order
enumeration.

First-pass mathematics gives a small package built on one tool, the
**midpoint-conflict lemma**. The lemma generalizes the cross-polytope argument
of Dey–Dubey–Molinaro to convex objectives. In any B&B tree whose children are
convex sets covering the parent's integer points (this includes variable,
general split, multiway hyperplane, and SOS branching) and whose nodes are
bounded by a convex relaxation `phi`, no leaf can contain two feasible integer
points `a != b` with `phi((a+b)/2) < OPT - eps`. So the number of leaves is at
least the chromatic number of the "midpoint-conflict graph". The bound depends
only on the relaxation, not on the branching rule. Curvature is what makes it
useful for nonlinear objectives: for a quadratic,
`phi((a+b)/2) = (phi(a)+phi(b))/2 - ||A(a-b)||^2/4`. Proved consequences:

- **Theorem 2 (random CVP).** For a Haar-random unimodular lattice and a
  uniformly random target, with high probability every such tree for the
  closest vector problem (CVP) with the continuous relaxation has at least
  `2^{(0.161-o(1))n}` leaves. This holds for any basis, including LLL- or
  BKZ-reduced ones. So lattice reduction and general disjunctions cannot make
  continuous-relaxation B&B subexponential on random instances.
- **Theorem 3 (correlated pairs).** On `k` orthogonal blocks of two correlated
  features, every such tree using the perspective relaxation has at least
  `2^k` leaves. The per-block 2x2 convex-hull relaxation is exact at the root,
  so strengthening the relaxation gives an exponential gain that no branching
  rule can match.
- **Lemma 4 (path lemma).** If every single "wrong" variable fixing is
  prunable at the root (condition C1), then every variable-branching tree, for
  any rule, is a path with pruned siblings and has at most `2p+1` nodes.
- **Hijazi–Bonami–Ouorou ball.** The known outer-approximation (OA) example
  forces `2^n` leaves on NLP-based B&B with any convex-piece branching, and on
  LP-based B&B over its extended-formulation OA master. `n` one-variable
  disjunctive cuts in the extended space close it at the root. The authors
  already note `2^n` nodes for OA branch-and-cut; the extension to arbitrary
  convex pieces and to the extended master is new here but minor.

Computations (random instances; certified dual bounds; 8 seeds unless noted)
show a sharp transition for perspective-relaxation B&B in random sparse
regression:

- At `n = 0.9 k ln p`, the geometric-mean node count stays between 31 and 52
  for `k = 8..20`, that is, `O(k)`.
- At `n = 0.5 k ln p`, it grows from 131 to about 10^4 (fits `e^{0.36k}` or
  `p^{4.7}` equally well).
- Condition C1 holds in 7–8 of 8 runs for `n >= 1.4 k ln p` and in all runs
  for `n >= 1.8 k ln p`, at every tested `k`. At `k = 20` it holds in all
  runs already at `1.1 k ln p`.

Both thresholds lie below the Lasso threshold `2 k ln p`. Conflict cliques
match the transition qualitatively. In square binary MIMO detection, trees
grow quickly at fixed SNR and much more slowly at SNR `4 log N`. Random-CVP
conflict cliques grow as about `1.17^n` for `n <= 28`.

Recommended direction: **Q1**, a relaxation-intrinsic phase transition for
perspective B&B in random sparse regression. The plan pairs the path lemma
(easy side) with random midpoint-conflict cliques (hard side), and uses
Theorem 2 and Theorem 3 as proved anchors. **Score 7/10.** The main risks are
novelty of the midpoint technique in nonlinear form (it is the
Dey–Dubey–Molinaro argument), and the difficulty of the random landscape
analysis needed for an `exp(Omega(k))` lower bound.

## 1. Frontier map

### 1.1 Linear baseline (what is proved for MILP)

| Result | Exact assumptions | Conclusion | Source (checked) |
|---|---|---|---|
| Dey–Dubey–Molinaro, random binary IPs | `max c'x, Ax <= b, x in {0,1}^n`; `A in [0,1]^{m x n}`, `c in [0,1]^n` iid uniform; `b_j = beta_j n`, `beta_j in (0,1/2)`; best-bound node selection; **any** fractional variable for branching; `n >= m+1` | tree has at most `n^{a1 (m + alpha log m)}` nodes with probability `>= 1 - 1/n - 2^{-alpha a2}` (`a1, a2` depend on `m, beta`). The proof uses only pruning by bound, a Dyer–Frieze integrality gap `O(log^2 n / n)`, and reduced-cost counting. Corollary 3 extends it to any "well-behaved" 0/1 IP with small gap and spread columns | arXiv 2007.15192 (Theorem 1 and Corollary 3 read from the PDF) |
| Borst–Dadush–Huiberts–Tiwari | Gaussian `A, c`; mild RHS condition | integrality gap `poly(m)(log n)^2/n` w.h.p.; meta-theorem linking gap to B&B size | Springer MP 2023; arXiv 2012.08346 (abstract) |
| Borst–Dadush–Mikulincer | `A` uniform on integer intervals or isotropic logconcave | gap `O_m(log^2 n / n)` w.p. `1 - 1/poly(n)`; B&B trees of size `n^{poly(m)}` w.h.p. | arXiv 2203.11863 (abstract) |
| Dadush–Tiwari | general branching proofs of integer infeasibility | coefficients recompilable to `(nR)^{O(n^2)}`; a polytope family in `[0,1]^n` needing `2^n/n` leaves | arXiv 2006.04124 (abstract) |
| Dey–Dubey–Molinaro, lower bounds | general split disjunctions | exponential lower bounds for packing, set cover and TSP instances. The cross-polytope needs `2^{n+1}-1` nodes (Prop. 3, midpoint argument), and this persists under Gaussian perturbation (no smoothed polynomial bound). Monotonicity (Lemma 4) and integral affine maps (Lemma 5) transfer bounds | local `dey2023-lower-bounds-on-the-size` (Sections 2, 3, 5 read) |
| Gläser–Pfetsch | compact (polynomially many constraints) IPs, general disjunctions | `2^{Omega(L^{1/12 - eps})}` via interpolation | local `glaser2024-sub-exponential-lower-bounds-for` |
| Dey–Shah | lot-sizing | exponential for general split disjunctions | local `dey2022-lower-bound-on-size-of` |
| Dey–Dubey–Molinaro–Shah | full strong branching (FSB) | FSB provably good on some vertex-cover instances, exponentially worse than another tree on others; empirically within 2x of optimal | arXiv 2110.10754 (abstract); follow-up Shah–Dey arXiv 2507.09455 (listing only) |
| Basu–Conforti–Di Summa–Jiang I | convex sets `C`, disjunction families | Theorem 2.1: for closed convex `C` in `[0,1]^n` and variable disjunctions, a B&C proof of size `N` yields a CP proof of size `<= N` for `c'x <= gamma + eps`, with `eps = 0` for polytopes. Stable set: CP polynomial vs B&B `2^{m+1}-2`. Fixed dimension: B&B `<= poly(CP)`. **Open:** Table 1 cells for split disjunctions; `eps = 0` for nonpolyhedral `C` | local `basu2023-complexity-of-branch-and-bound` (Sections 2, 4 read) |
| Basu–Conforti–Di Summa–Jiang II | branching and cutting families | "complementary" pairs give B&C exponentially better than both. **Open:** whether complementarity exactly characterizes when B&C is superior | local `basu2022-complexity-of-branch-and-bound` (p. 141 text) |
| Cornuéjols–Dubey | B&B trees viewed as extended formulations | skewed `k`-trees versus Sherali–Adams; examples both ways; `2^{(n-1)/6}` lower bound where lift-and-project needs 2 rounds | local `cornuejols2025-branch-and-bound-versus-lift` |
| Cheng–Basu | learning for B&C | local expert signals (strong branching, LP bound improvement) can be exponentially suboptimal; tie-breaking instability; linear MILP only | arXiv 2601.23249 (HTML) |
| Encz–Mastrolilli–Vercesi | knapsack and scheduling B&B | PTAS-like behaviour of standard B&B | arXiv 2504.15885 (abstract) |

### 1.2 Nonlinear relaxations: what exists

- **Convex 0/1 sets.** Basu et al. I, Theorem 2.1, above, is the only general
  tree-size theorem found that is stated for nonpolyhedral relaxations. It
  compares B&B with lift-and-project cuts and does not bound node counts. See
  also the Hijazi–Bonami–Ouorou remark below.
- **Oracle complexity.** Basu–Jiang–Kerger–Molinaro give information-complexity
  bounds for mixed-integer convex optimization. Basu–Kerger–Molinaro give tight
  lower bounds for binary first-order oracles. Both concern oracle queries, not
  B&B trees over an explicit relaxation (local
  `basu2025-information-complexity-of-mixed-integer`,
  `basu2025-tight-lower-bounds-for-binary`).
- **Integrality gaps.** Kocuk–Morán Ramírez classify when the continuous
  relaxation of a convex MIP has a finite gap and estimate it, and they warn
  that polyhedral approximations can give arbitrarily worse gap estimates
  (local `ramirez2026-on-the-integrality-gap-of`, arXiv 2501.00638). This is
  the natural input to a DDM-style "gap to tree size" theorem, but no such
  theorem is given there.
- **Outer approximation.** Hijazi–Bonami–Ouorou, Example 1 (PDF read): the
  ball `B(1/2 * 1, sqrt(n-1)/2)` has no 0/1 points, and classical OA needs
  `2^n` iterations. The univariate extended formulation
  `z_i >= (x_i - 1/2)^2`, `sum z_i <= (n-1)/4` fixes OA. Their Lemma 2.1 is a
  midpoint argument: no valid linear inequality cuts two vertices, because
  every edge meets the ball. They remark that an OA branch-and-cut also needs
  at least `2^n` nodes. Lubin et al. (local
  `lubin2018-polyhedral-approximation-in-mixed-integer`,
  `lubin2016-extended-formulations-in-mixed-integer`) develop the
  extended-formulation view. None of these sources counts nodes for general
  disjunctions or for the extended master.
- **Convex quadratic integer programs.** Buchheim–Caprara–Lodi (Math. Prog.
  2012) and Buchheim–Hübner–Schöbel (ellipsoid bounds) are fast depth-first
  B&B with continuous or ellipsoid bounds; their exponential growth on random
  instances is empirical. This is from memory; the papers were not re-read.
- **Sphere decoding.** Sphere decoding is B&B for integer least squares with
  the unboxed continuous relaxation and a fixed branching order. Hassibi–Vikalo
  (2005) report polynomial expected complexity at practical sizes.
  Jaldén–Ottersten (2005) prove the expected complexity is exponential at every
  fixed SNR. Seethaler–Jaldén–Studer–Bölcskei (ISIT 2009, arXiv 0905.1215)
  show a Pareto-type complexity tail with exponent `N-M+1` that lattice
  reduction does not improve. Checked via search summaries only.
- **MIMO detection at the ML threshold.** Papailiopoulos (arXiv 2609.19405,
  16 Sep 2026): square Gaussian binary MIMO
  `y = sqrt(rho/N) H x* + w`; rounded linear MMSE plus steepest single-bit
  descent recovers `x*` in `O(N^3)` operations for `rho >= 2 log N`. This is
  tight to first order, since ML fails for
  `rho <= 2 log N - log log N - s_N`. The box relaxation needed `4 log N`.
  This is a **search** result. It does not certify optimality, so the B&B
  certification threshold is a separate question.

### 1.3 Sparse regression, perspective relaxations, and hardness

- **Root exactness.** Pilanci–Wainwright–El Ghaoui (MP 2015): the Boolean
  relaxation equals the perspective relaxation after minimizing out `beta`.
  They give necessary and sufficient exactness conditions, satisfied w.h.p.
  for Gaussian designs. As restated in arXiv 1603.04572 (Theorem 3): exact
  w.p. `1 - 2e^{-c1 n}` when
  `n > c0 (gamma^2 + ||beta*_S||^2)/beta_min^2 * log p` with ridge
  `rho = sqrt(n)`. With equal magnitudes `b` this reads
  `n >= c0 (k + sigma^2/b^2) log p`, a one-node tree. The constants are
  unspecified. The original paper was checked via its abstract only.
- **Empirical phase transition, no node theory.** Bertsimas–Van Parys
  (Ann. Stat. 2020, arXiv 1709.10029) observe an empirical transition: large
  `n` is easy and fast, small `n` is slow. Hazimeh–Mazumder–Saab (L0BnB,
  arXiv 2004.06152) observe larger trees at small `n` (loose relaxation). The
  abstracts of Guyard et al. (ICML 2024, arXiv 2406.03504), El0ps (arXiv
  2506.06373), Lucas–Meng–Mazumder GPU B&B (arXiv 2602.04551), and the GPU
  certification papers (arXiv 2603.01306, 2605.22188) contain no node-count
  theory. The SC-SDP variable-fixing paper (arXiv 2606.22894) shows no
  tree-size theorem in its abstract.
- **Overlap gap property (OGP).** Gamarnik–Zadik (arXiv 1711.04952;
  Ann. Stat. 2022): Gaussian design, `k`-sparse `beta*`, noise `sigma^2`.
  There is a gap between `n*` (information-theoretic) and `n_alg` (Lasso-type,
  about `(2k + sigma^2) log p`). OGP holds in `[n*, c n_alg]` for a small `c`,
  local search succeeds above `C n_alg`, and Lasso fails in the conjectured
  hard window. Li–Schramm (arXiv 2411.01836) give shortest path as an easy
  problem with OGP, so OGP alone does not predict hardness.
- **Structural tractability.** Del Pia–Dey–Weismantel give polynomial-time
  subset selection under sparsity of the data matrix (local
  `pia2020-subset-selection-in-sparse-matrices`). This is not about B&B.

### 1.4 Repository baseline and overlap

- `results/spatial-bb-exponential-lower-bound.md` and the sibling scout
  `research-20260928b/scouting/spatial-bb-theory.md` concern **spatial**
  branching with separable underestimators. This report concerns **integer**
  branching with exact convex relaxations. The two share one idea: lower
  bounds come from near-optimal sets and curvature. The sibling's Theorem D is
  the continuous analogue of the conflict bound below.
- The indicator quadratic star/tree results study structured Hessians and
  dynamic programming, not B&B trees on random designs. There is no overlap
  with the questions below.

### 1.5 Search log and caution

Searches ran on 2026-09-28: web search (until the session limit of 200 was
reached) and arXiv listing queries through WebFetch ("branch-and-bound tree
size lower bound"; "branch-and-bound" + "sparse regression"; "sphere decoding
complexity lower bound"; "branch-and-bound convex integer quadratic
complexity"). None returned a node-count theorem for NLP, conic, or
perspective B&B, or a branching-independent lower bound for integer least
squares or CVP. An unsuccessful bounded search does not establish novelty.
Dadush–Tiwari (CCC 2020) and Fleming et al. (CCC 2021) were checked only by
abstract or secondary description; lattice-enumeration lower-bound papers
(Hanrot–Stehlé and successors) were not checked.

## 2. Open questions

Notation: *convex-piece B&B* means every node carries a closed convex set,
children cover the parent's integer points, and each node is bounded by
`inf{phi(x) : x in K ∩ Q_v}` for a fixed convex relaxation `(phi, K)` that is
exact on feasible integer points. An *`eps`-certificate* is such a tree whose
leaves all have bound `>= OPT - eps`.

**Q1 (recommended). Relaxation-intrinsic phase transition for perspective B&B
in random sparse regression.**

- Model: `X in R^{n x p}` with iid `N(0,1)` entries; `beta*` with `k`
  entries `+-b` at random positions; `y = X beta* + sigma w`.
  `P: min ||y - X beta||^2 + lam ||beta||^2` subject to `||beta||_0 <= k`,
  with `lam = sqrt(n)`.
- Relaxation: the perspective (Boolean) relaxation,
  `g(z) = y'(I + X diag(z) X'/lam)^{-1} y` over
  `{z in [0,1]^p : sum z <= k}` with fixings. Equivalently, least squares
  regularized by the squared `k`-support norm.
- Question: with `k = p^gamma` for some `0 < gamma < 1` and SNR `b/sigma`
  fixed, find `alpha_- <= alpha_+` such that:
  - (a) for `n >= (alpha_+ + delta) k ln p`, w.h.p. every single wrong fixing
    is prunable (condition C1), so every variable-branching tree has at most
    `2p+1` nodes;
  - (b) for `n <= (alpha_- - delta) k ln p`, w.h.p. the midpoint-conflict
    graph of `g` has clique number `exp(Omega(k))`, or at least
    superpolynomial, so every convex-piece `eps`-certificate is that large.
- Decide whether `alpha_- = alpha_+`, and where the transition lies relative
  to exact-recovery `n` and to the Lasso threshold `2 k ln p`.
- Evidence that it is open: part (a) is known only in the stronger form "root
  exact" (Pilanci–Wainwright–El Ghaoui) with unspecified `c0`. Part (b) has no
  result in any source above. The empirical transition (Bertsimas–Van Parys;
  Hazimeh et al.) has no node-count theory.
- Our data (Section 3.6) suggest `alpha_+ <= 1.4` and a tree-size transition
  near `alpha ≈ 0.7–0.9` for `b/sigma = 2`. Both are below the Lasso constant
  2, in part of the Gamarnik–Zadik window.

**Q2. Certification threshold for random binary least squares (MIMO) with the
box relaxation.**

- Model: `y = sqrt(rho/N) H x* + w`, with `H in R^{N x N}` and `w` iid
  Gaussian and `x* in {+-1}^N`.
- Relaxation: `min ||y - A x||^2` over `x in [-1,1]^N` with fixings, where
  `A = sqrt(rho/N) H`.
- Questions:
  - (i) For fixed `rho`, is every convex-piece certificate of size
    `exp(N^{Omega(1)})` w.h.p.?
  - (ii) Is there `c*` such that for `rho >= (c* + delta) log N`, a
    `poly(N)`-node variable-branching certificate exists w.h.p.? Is `c* = 2`
    (the ML/search threshold of Papailiopoulos 2026), smaller, or between 2
    and 4?
- Evidence that it is open:
  - Known complexity results are for fixed-order sphere decoders, in
    expectation or tail (Jaldén–Ottersten; Seethaler et al.), not for adaptive
    or general-split B&B with the box relaxation.
  - The 2026 polynomial-time result is for search, not certification.
  - Our Theorem 2 settles the unbounded, Haar-random, random-target case only.
    It does not cover Gaussian-basis lattices: there `lambda_1` stays bounded
    while the covering radius grows, so the shell argument is empty.

**Q3. Is the conflict chromatic number a polynomially tight measure of
convex-MIQP B&B complexity, and does it characterize when B&C beats B&B?**

- Setting: convex MIQP with the natural relaxation `(phi, K)`.
  `chi_eps(phi, K)` is the chromatic number of the midpoint-conflict graph,
  and `H_eps` is its hypergraph refinement (classes `I` with
  `min_{conv I} phi >= OPT - eps`).
- (i) Over arbitrary convex pieces that cover the feasible integer points,
  the minimum number of leaves equals the minimum number of
  `H_eps`-admissible classes (Section 3.1). Is the minimum general-split tree
  size at most `poly(n, encoding size) * (that number)^{O(1)}`?
- (ii) If yes, B&C beats B&B exactly when cuts shrink the class number. This
  would answer, for convex MIQP, the question left open in Basu et al. II
  (whether complementarity characterizes B&C superiority) and some of the
  split-disjunction cells of Basu et al. I, Table 1.
- Evidence that it is open: no source defines this parameter. The
  cross-polytope bound (DDM Prop. 3) is its linear special case. Gläser–Pfetsch
  use interpolation rather than midpoints, which hints that (i) may fail for
  polytopes; nothing is known for strictly convex objectives.

**Q4 (lower priority). The `eps = 0` case of Basu et al. I, Theorem 2.1.**

- Question: for a closed convex, nonpolyhedral `C` in `[0,1]^n` and variable
  disjunctions, does a B&C proof of size `N` always give a CP proof of the
  same inequality with no slack?
- Status: stated as open in Basu et al. I, Section 4. The obstacle is
  rotating face-valid inequalities on curved faces (their Lemma 3.3).
- Solver significance is modest. It is listed because it is the one
  explicitly posed open problem that is specific to nonlinear relaxations.

## 3. First-pass mathematics and computations (for Q1, with Q2 and Q3 anchors)

### 3.1 The midpoint-conflict lemma

Setting:

- Integer program: `OPT = min{f(x) : x in C, x in Z^n}`. Continuous
  variables are projected out, which keeps convexity in `x`.
- Convex relaxation `(phi, K)`: `K` is closed convex and contains all feasible
  points; `phi` is convex on `K` with `phi = f` on feasible integer points.
  This covers the natural relaxation and the perspective relaxation in `z`
  (after minimizing out `beta`).
- Convex-piece tree: the root carries `R^n`; each node carries a closed convex
  `Q_v`; its children's sets cover `Q_v ∩ Z^n`; node bound
  `r(v) = inf{phi(x) : x in K ∩ Q_v}`.

**Lemma 1.** If the set of a leaf `v` contains feasible integer points
`a_1, ..., a_r`, then `r(v) <= min{phi(x) : x in conv{a_i}}`.

*Proof.* `conv{a_i}` lies in `K` (convex, contains the `a_i`) and in `Q_v`
(convex, contains the `a_i`). ∎

A B&B run that ends with incumbent `UB <= OPT + eps'` and prunes by
infeasibility, by bound (`r >= UB - eps`), or by integrality (the relaxation
optimum is feasible and integral, so `r = f(x̂) >= OPT`) yields an
`eps`-certificate in this sense.

**Theorem 1 (conflict-graph bound).** Let `G_eps` be the graph on feasible
integer points with `a ~ b` iff `phi((a+b)/2) < OPT - eps`. Every
`eps`-certificate has at least `chi(G_eps) >= omega(G_eps)` leaves. More
generally, it has at least the minimum number of classes in a partition of the
feasible integer points into sets `I` with `min_{conv I} phi >= OPT - eps`.
If the pieces only need to cover the *feasible* integer points (as in a
disjunctive reformulation), this number is attained by the pieces `conv I`.
With the usual requirement that pieces cover all of `Z^n`, it is only a lower
bound.

*Proof.* By induction, the leaves' sets cover `Z^n`. Assign each feasible
point to a leaf containing it. By Lemma 1, each leaf's points form an
independent set (respectively an admissible class). ∎

Remarks:

- **Robustness.** The bound also holds with presolve-style domain reductions
  that use the incumbent: OBBT on `K ∩ {phi <= UB}` and reduced-cost fixing.
  The offending midpoint satisfies `phi < OPT <= UB`, so it survives every
  such reduction.
- **What is not covered.** Node-local cutting planes (B&C) and stronger
  relaxations change `(phi, K)`, so the graph must be recomputed for them.
  This is the intended use: cuts help exactly when they remove conflicts.
- **The linear case is weak.** For linear `phi`, the midpoint of two feasible
  points has value equal to their average. Conflicts then arise only from
  infeasibility structure; the DDM cross-polytope is the case `phi ≡ 0`, where
  conflict means "midpoint in `K`". For strictly convex `phi`, curvature
  creates conflicts among near-optimal points.

**Corollary 1.**

- (a) If `phi` is `mu`-strongly convex, all feasible integer points with
  `phi < OPT + mu/8 - eps` are pairwise adjacent, so a certificate has at
  least as many leaves as there are such points.
- (b) If `phi(x) = ||Ax - y||^2`, then `a ~ b` iff `||y - A(a+b)/2||^2 < OPT - eps`,
  equivalently `||A(a-b)||^2/4 > (phi(a)+phi(b))/2 - OPT + eps`.

**Corollary 2 (Hijazi–Bonami–Ouorou ball).**

- For `K = B(1/2 * 1, sqrt(n-1)/2) ∩ [0,1]^n`, the midpoint of two distinct
  0/1 points at Hamming distance `d` satisfies
  `||m - 1/2 * 1||^2 = (n-d)/4 <= (n-1)/4`. So all `2^n` points conflict, and
  every convex-piece NLP-B&B proof of infeasibility has at least `2^n`
  leaves.
- The same holds for LP-based B&B on the extended OA master
  `z_i >= max(1/4 - x_i, x_i - 3/4)`, `sum z_i <= (n-1)/4`. Its projection is
  `{sum |x_i - 1/2| <= n/2 - 1/4}`, which contains all half-integral
  midpoints.
- On the other hand, the `n` one-variable disjunctive (lift-and-project) cuts
  `z_i >= 1/4` make the root infeasible.
- This is a nonlinear instance of the CP-versus-B&B phenomenon of Basu et
  al. Its novelty is low: Hijazi–Bonami–Ouorou's Lemma 2.1 uses the same
  edge-midpoint idea and already gives `2^n` nodes for OA branch-and-cut.

### 3.2 Theorem 2: random CVP is exponentially hard for continuous-relaxation B&B

**Theorem 2.** Let `L` be a Haar-random lattice of determinant 1 in `R^n`,
`B` any basis, and `t` uniform on `R^n / L`. Let `phi(x) = ||Bx - t||^2`
over `x in Z^n`, let `GH` be the radius of the unit-volume ball, and fix
`delta in (0, 0.1)` and `eps <= delta GH^2`. Set
`V = ((1-delta)^2 * 5/4 - delta)^{n/2}`.

With probability at least `1 - 2(1-delta)^n - 4/V`, every convex-piece
`eps`-certificate with the continuous relaxation has at least `V/2`
(that is, `2^{(0.161 - O(delta))n}`) leaves. This includes Lenstra- or
Kannan-style hyperplane branching, any sphere decoder with any lattice
reduction and any ordering, and all split trees.

*Proof.*

1. For uniform `t` and any fixed unimodular `L`,
   `E|L ∩ B(t,r)| = vol B_r = (r/GH)^n`. So
   `P(OPT < (1-delta)^2 GH^2) <= (1-delta)^n`.
2. By Siegel's mean value theorem, `E #{v in L\0 : ||v|| <= r} = vol B_r`, so
   `P(lambda_1 < (1-delta) GH) <= (1-delta)^n`.
3. On the complement of both events, let
   `r0^2 = (1-delta)^2 (5/4) GH^2 - eps <= OPT + lambda_1^2/4 - eps`. For
   distinct lattice points in `B(t, r0)`,
   `phi(mid) = (phi(a)+phi(b))/2 - ||B(a-b)||^2/4 < OPT + lambda_1^2/4 - eps - lambda_1^2/4`,
   so all such points are pairwise adjacent (Corollary 1(b)).
4. Let `N = |L ∩ B(t,r0)|`. Then `E N = vol B_{r0} =: V' >= V`. For fixed
   `L`,
   `E_t N^2 = sum_{v in L} vol(B_{r0} ∩ (B_{r0}+v)) = V' + sum_{v≠0} h(v)`,
   and Siegel gives `E_L sum_{v≠0} h(v) = ∫ h = V'^2`. So `Var N = V'`, and
   Chebyshev gives `P(N < V'/2) <= 4/V'`. ∎

Remarks:

- The constant 0.161 comes only from the "shell" `OPT + lambda_1^2/4`. A
  larger clique should come from lattice points that are nearly orthogonal as
  seen from `t`. The heuristic target is `(3/2)^{n/2}` or more; it is not
  proved.
- Numerics (`cvp_clique.py`, `cvp_count.py`; 20–30 random instances per `n`)
  are summarized in the table below. The shell counts match the
  Gaussian-heuristic prediction `vol B_r` on average. The greedy clique grows
  by a factor of about 1.17 per dimension (about `2^{0.22n}`) for both
  Gaussian-basis and Goldstein–Mayer random lattices.
- Caution: for Gaussian-basis lattices (the MIMO model), `lambda_1` stays
  `O(1)` in absolute units while `GH` grows like `sqrt(n)`. The shell count
  therefore saturates at `exp(O(1))`, and Theorem 2's proof does not apply.
  Only the unproved near-orthogonality mechanism remains, which the growing
  cliques support.

| `n` | shell count, median | greedy clique, Gaussian basis (median) | greedy clique, Goldstein–Mayer (median) |
|---:|---:|---:|---:|
| 8 | 2 | 5.5 | 6 |
| 12 | 3 | 13 | 13 |
| 16 | 4.5 | 23 | 25 |
| 20 | 5 | 44 | 36.5 |
| 24 | 6.5 | 52 | 87 |
| 28 | 9 | 122.5 | not finished |

The shell counts are from `cvp_count.py` (30 runs per `n`, Gaussian bases).
At `n = 24–28` the candidate list was truncated at 2500 points, so the cliques
there are lower bounds on the greedy value. The shell count is itself a
rigorous clique.

### 3.3 Theorem 3: perspective versus pairwise hulls on correlated pairs

Gadget:

- `k` orthogonal blocks. Block `j` has two unit features `u = e_1` and
  `v = (cos th, sin th)` in its own `R^2`, and response
  `y_j = s (u+v)/||u+v||`.
- Ridge `lam > 0`; budget `sum z <= k`.
- Block values: `g00 = s^2` (no feature), `g10` (one feature), `g11` (both).
- Assumptions: (i) diminishing returns, `g00 - g10 > g10 - g11`; (ii)
  `delta := g10 - ĝ(1/2,1/2) > 0`, where `ĝ` is the block's perspective
  relaxation value. Condition (ii) holds by strict convexity and symmetry, and
  was verified numerically. At `th = 0.3`, `s = 3`, `lam = 1`: `delta = 0.0497`,
  `g00 - g10 = 4.40`, `g10 - g11 = 1.55`.

**Theorem 3.** With `eps < delta`, the following hold.

- (a) `OPT = k g10`, attained by the `2^k` one-per-block supports.
- (b) Every convex-piece `eps`-certificate with the perspective relaxation has
  at least `2^k` leaves. This covers any variable, split, or SOS branching.
- (c) Replace each block's perspective terms by the convex hull of the block's
  mixed-integer epigraph (a 4-term disjunctive formulation). The resulting
  relaxation equals `OPT` at the root, so one node suffices.

*Proof.*

- (a) Let `b_j` be the number of features used in block `j`. The value is
  `sum_j h(b_j)`, where `h` is convex decreasing on `{0,1,2}`, so the minimum
  under `sum b_j <= k` is at `b_j = 1` for all `j`.
- (b) Two one-per-block supports that differ on a block set `D` have a
  midpoint that is `(1/2,1/2)` on `D` and one-per-block elsewhere, with
  `sum z = k`. The relaxation is separable over orthogonal blocks, so
  `g(mid) = OPT - |D| delta < OPT - eps`. Apply Theorem 1.
- (c) The block hull's value, as a function of the block budget, is the convex
  piecewise-linear interpolation of `(0, g00), (1, g10), (2, g11)`, so the
  coupled relaxation attains `k g10`. ∎

Check (`block_pair.py`): the root perspective gap equals `k delta`, and
most-fractional best-first B&B uses 6, 14, 36, 82, 196, 436, 1000, 2186, 4884
leaves for `k = 2..10`. That is always `>= 2^k`, growing like about `2.3^k`.
The weakness of the perspective relaxation on correlated features is folklore
(it motivates rank-one and 2x2 convexifications). The branching-independent
tree-size statement appears new in the bounded search.

### 3.4 Lemma 4: single-wrong-fixing certificates give linear trees

**Lemma 4.** Consider variable branching on binaries with a relaxation that
is monotone under added fixings. Let `z°` be optimal. Suppose that for every
`i`, the node with the single fixing `z_i = 1 - z°_i` has bound
`>= OPT - eps` (condition C1). Then every variable-branching tree, for any
branching rule and any node order, with incumbent `OPT`, has at most `2D+1`
nodes, where `D <= p` is the number of branchings on the nodes that contain
`z°`.

*Proof.* A node not containing `z°` contains a wrong fixing, so its bound is
at least the single-fixing bound, and it is pruned when created. The nodes
containing `z°` form a path. ∎

C1 is exactly "root probing fixes every variable". It is weaker than root
exactness, since Pilanci–Wainwright's condition implies C1.

Computation (`sparse_single.py`; 8 runs per cell; `p = 6k`, `b = 1`,
`sigma = 0.5`, `lam = sqrt(n)`):

| `k` | runs with C1, by `alpha = n/(k ln p)` (0.5 / 0.7 / 0.9 / 1.1 / 1.4 / 1.8 / 2.5) | node count over all C1 runs |
|---:|---|---|
| 6 | 0 / 1 / 1 / 0 / 7 / 8 / 8 | 7–19 |
| 10 | 0 / 1 / 3 / 3 / 7 / 8 / 8 | 11–29 |
| 14 | 0 / 1 (7 runs) / 2 / 6 / 8 / 8 / 8 | 5–35 |
| 20 | 0 (1 of 8 finished) / 1 / 3 / 8 / 8 / 8 / 8 | 23–55 |

Across all 124 runs where C1 holds, nodes are at most `1.46 (2k+1)`, well
within `2p+1`. Exact support recovery by the L0 optimum sets in at about
`alpha ≈ 0.7–0.9`.

### 3.5 Upper-bound mechanism: why the DDM proof does not transfer

DDM bound the tree by counting fixing sets whose total reduced cost is below
the integrality gap. The count stays small because an LP vertex has at most
`m` fractional variables, and the remaining variables carry reduced costs.

Nonlinear relaxations lose this vertex sparsity. In square binary least
squares and in weak perspective relaxations, the root optimum has many
fractional coordinates with zero first-order reduced cost. Only curvature
separates them, and curvature is exactly what creates midpoint conflicts.

So a nonlinear analogue of the DDM theorem needs a second-order "reduced
cost". The natural candidate is the single-fixing margin used in C1, combined
with a bound on the number of fractional coordinates at the root. This is
the core of the easy side of Q1 and Q2.

### 3.6 Computations for Q1 and Q2

Implementation:

- `sparse_bb.py`: best-first B&B with the perspective relaxation, solved by
  Clarabel (SOCP) or accelerated projected gradient, and pruned on a
  certified Frank–Wolfe / Lagrangian dual bound. Checked against CVXPY on
  random nodes to `1e-8` (`check_relax.py`).
- `bls.py`: the box relaxation by BVLS, with the same dual bound.
- `dp_min_tree.py`: exact minimum variable-branching trees by dynamic
  programming over partial assignments. The B&B optimum was checked against
  brute-force enumeration (`quick_bb.py`).

**Sparse regression**, `p = 6k`, `b/sigma = 2`, `lam = sqrt(n)`, 8 seeds
(`scaling_big_s0.5.jsonl`). Entries are the geometric mean of processed nodes;
the range is in brackets.

| `k` (`p`) | `alpha ≈ 0.5`: `n`, nodes | `alpha = 0.9`: `n`, nodes |
|---:|---|---|
| 8 (48) | 15: 131 [55, 467] | 28: 47 [15, 377] |
| 10 (60) | 20: 339 [75, 1287] | 37: 38 [25, 111] |
| 12 (72) | 26: 494 [247, 2201] | 46: 31 [25, 43] |
| 14 (84) | 31: 2319 [297, 7815] | 56: 32 [27, 39] |
| 16 (96) | 37: 2713 [155, 12983] | 66: 40 [33, 67] |
| 18 (108) | 42: 4487 [169, 34933] (7 runs) | 76: 41 [29, 95] |
| 20 (120) | 48: 10606 [4279, 39811] (4 runs) | 86: 52 [43, 85] |

- At `alpha ≈ 0.5`, least squares gives `ln(nodes) = 2.13 + 0.361 k` or
  `-13.3 + 4.66 ln p`, with equal residuals. Exponential growth in `k` and
  polynomial growth in `p` cannot be distinguished at this scale.
- A finer `alpha` grid (6 seeds, `scaling_s0.5.jsonl`) places the
  easy-to-hard change at `alpha ≈ 0.7–0.85`. The hardest point for fixed `k`
  is at `alpha ≈ 0.4–0.55`, below exact recovery.
- Conflict cliques are small in the easy regime and grow in the hard
  regime. By full enumeration (`sconf_p24_k4`, `sconf_p30_k5`; 180 instances),
  the medians are 1–2.5 in the easy regime and 3–5.5 in the hard regime, and
  the clique is at most the leaf count in every instance. From B&B candidate
  pools (`sconf_pool`), the geometric means are 18–26 at `k = 12–14`. The
  pooled cliques are only 3–30% of the leaf count, so the greedy clique on
  pooled candidates is a weak certificate at `k >= 10`.
- Minimum trees (`dp_vs_clique.jsonl`; `p = 12`, `k = 4`, 36 instances): in
  every instance, `clique <= minimum leaves <= most-fractional leaves`.
  Most-fractional branching is within a factor of 1.67 of optimal, and the
  optimal tree is within a factor of 5 of the greedy clique.

**Binary MIMO, box relaxation** (`bls_big*.jsonl`; `M = N`; 8 seeds, fewer
where marked). Entries are the geometric mean of nodes.

| SNR | `N = 20` | 40 | 60 | 70 | 80 | 100 | 120 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `rho = 1` | 31 | 368 | 3310 | 3489 | – | – | – |
| `rho = 2` | 39 | 532 | 4864 | 9360 | – | – | – |
| `rho = 2 log N` | 26 | 97 | 761 | 477 | 2233 | 1933 (7 runs) | 1606 (3 runs) |
| `rho = 3 log N` | – | – | – | – | 467 | 457 | 2174 |
| `rho = 4 log N` | 21 | 52 | 133 | 100 | 208 | 219 | 626 |
| `rho = 6 log N` | – | – | – | – | 113 | 126 | 225 |

- At fixed `rho`, growth is about `1.1^N` over `N <= 70`. This is not
  conclusive.
- At `2 log N` and `3 log N`, growth is irregular with heavy tails (the
  maximum at `3 log N`, `N = 120` is 13663). The data are compatible with a
  polynomial of degree about 2–3 or a slow exponential.
- At `4 log N`, trees grow roughly like `N^2` (21 to 626 from `N = 20` to
  120); at `6 log N` they are smaller still.
- Enumeration-based conflict cliques for `N <= 20` (`bls_sweep.jsonl`) have
  medians 3–7 at `rho <= 4` and about 1 at `rho = 16`, with maxima up to 29.
- Everything here is small-`N` evidence only.

Caveats: all computations use floating point. Pruning uses certified dual
bounds but no exact arithmetic. Cliques are greedy, so they are valid lower
bounds but can be far from `omega`. Instance sizes are far from asymptotic.

### 3.7 Attack plan for Q1, and risk

1. **Easy side, `alpha_+`.** Prove C1 w.h.p. for
   `n >= (alpha_+ + delta) k ln p` using node-specific dual certificates.
   - For "null feature `j` forced in", use the dual of the node problem built
     from a primal-dual witness on `S* ∪ {j}`, with leave-one-out conditioning
     on `x_j`.
   - For "true feature `i` removed", use a rank-one downdate.
   - To get sharp constants, CGMT for squared-`k`-support-norm regression
     gives fixed-point equations for the node values. A single fixing is a
     rank-one perturbation of the root problem.
   - The union bound is over `2p` events.
   - Expected output: an explicit `alpha_+(b/sigma)`, to compare with the
     empirical 1.1–1.4 and with the root-exactness constant.
   - Risk: moderate. The techniques exist; the new ingredient is the node
     dual.
2. **Hard side, `alpha_-`.** Build explicit random cliques that imitate
   Theorem 3.
   - Find `m` disjoint swap pairs `(i_l in S°, j_l not in S°)`. Each swap
     should have a small integer cost `Delta_l`, a midpoint gain
     `delta_l > sum Delta`, and weak cross-interaction. The `2^m` supports
     `S° ⊕ (any subset of swaps)` then form a clique.
   - Estimate `m` with a first- and second-moment count of cheap swaps,
     plus uniform restricted-isometry control of cross terms on `2m`-sparse
     sets. This mirrors a first-pass heuristic for binary MIMO that gives
     `m ≈ N^{1/3}` and hence `2^{Omega(N^{1/3})}`, not yet proved.
   - Main risk: the swap costs are measured from the random optimum `S°`.
     This needs landscape control near the optimum, which is OGP-type
     analysis. Reaching `exp(Omega(k))` rather than `exp(k^{Omega(1)})` is
     the hard part.
   - Risk: high for `exp(Omega(k))`; moderate for a superpolynomial bound.
3. **Tightness (Q3 link).** Compute minimum trees and exact `chi` or `H_eps`
   class numbers on small instances to test whether split trees are within
   polynomial factors of the class number. The DP data so far show a factor
   of at most 5 between the minimum tree and the greedy clique.
4. **Scale-up.** Replace Clarabel with a first-order GPU relaxation (as in
   Lucas–Meng–Mazumder) to reach `k ≈ 50`. Measure `alpha` thresholds and
   whether `ln(nodes)` scales with `k` or with `ln p`.

Overall difficulty: the easy side is a solid paper-sized result. The hard
side is a research problem; its lower-risk fallback is Theorem 2 plus
Theorem 3 plus explicit superpolynomial random cliques.

## 4. Significance

**Proved (first pass, unreviewed).**

- Theorem 1 gives relaxation-intrinsic lower bounds that hold for every
  branching rule, every node order, and every convex-piece disjunction
  family, and survive incumbent-based bound tightening.
- Theorem 2: continuous-relaxation B&B, including all lattice-reduced sphere
  decoders and general split trees, needs `2^{Omega(n)}` leaves on random CVP.
  Branching innovation alone cannot fix random convex integer least squares;
  only stronger bounds can.
- Theorem 3: an exponential separation, immune to any branching choice,
  between perspective and pairwise-hull relaxations. It is a clean nonlinear
  instance of "cuts beat branching".
- Lemma 4: root probing (C1) certifies linear-size trees for all branching
  rules.

**Plausible (supported by data, not proved).**

- Perspective B&B in random sparse regression has a sharp transition in
  `alpha = n/(k ln p)`. Above it, trees have `O(k)` nodes; below it, growth is
  superpolynomial. The transition lies below the Lasso threshold, so exact
  MIO certification is easy in part of the conjectured statistically hard
  window at moderate sizes.
- For binary MIMO, box-relaxation certificates grow roughly like `N^2` at
  `rho = 4 log N`. At `rho = 2–3 log N` they may be polynomial, but the tails
  are heavy and the data are inconclusive. At fixed `rho` they look
  superpolynomial.
- The conflict clique is a usable, branching-free diagnostic of
  relaxation-limited instances.

**Speculative (possible solver impact).**

- A cheap online test: sample near-optimal incumbents, compute a few midpoint
  relaxation values, and detect a large clique. On detection, a solver would
  switch effort from branching to relaxation strengthening (rank-one, 2x2, or
  SDP cuts for indicators; ellipsoidal or SDP bounds for integer QPs). This
  is the Q3 mechanism.
- Root probing (C1) as a predictor of "easy" instances.
- A benchmark for learned branching rules: the gap to the conflict bound
  measures how much any branching rule could still gain.
- For practical value, one would still need fast clique heuristics, evidence
  on real instances (not only random ones), and cut families that provably
  remove conflicts.

## 5. Recommendation

Pursue Q1, organized around the midpoint-conflict framework, and write up
Theorems 1–3 and Lemma 4 first. Theorem 2 (random CVP) and Theorem 3
(perspective versus pairwise hull) look nearly complete, but they need an
independent proof check and a targeted novelty check against Dadush–Tiwari,
Fleming et al., and lattice-enumeration lower bounds before any claim of
originality.

Then attack the easy side of Q1 (an explicit `alpha_+` through C1 and a node
dual certificate), which is feasible and would give the first node-count
theorem for perspective B&B at a threshold below root exactness. Keep the
hard side (random cliques) as the ambitious part, with Q2 (MIMO certification
threshold) as a parallel test bed that uses the same tools.

**Score: 7/10.** Significance is high for MINLP and statistics, because it
explains a widely reported empirical transition and says when branching
cannot help. Feasibility is moderate: the easy side and the anchors are
within reach, while the exponential hard side is risky. Originality is
moderate to high: the tool is the DDM midpoint argument, but its use for
nonlinear objectives, random CVP, and perspective relaxations appears new in
the bounded search.

## Appendix: commands run (targeted local checks only)

All commands ran from `research-20260928b/scouting/bb-tree-size-convex/`
with Python 3.13, NumPy 2.5, SciPy 1.18, CVXPY 1.9, and Clarabel 0.11. No
project-wide checks were run and CI was not inspected.

- `python3 check_relax.py`: perspective relaxation versus CVXPY/Clarabel on
  8 random nodes (agree to `1e-8`).
- `python3 quick_bb.py`: B&B optimum equals brute force on 5 instances.
- `python3 sweep.py 40 6 0.5 20000 4 ...` and `python3 sweep.py 60 10 0.5 30000 4 ...`:
  exploratory sweeps.
- `python3 sweep_scaling.py scaling_s0.5.jsonl 0.5 100000 6 4,...,14 0.4,...,1.8`
  and `python3 sweep_scaling.py scaling_big_s0.5.jsonl 0.5 300000 8 16,18,20,8,10,12,14 0.5,0.9`:
  sparse scaling. The unfinished runs (4 at `k = 20, alpha = 0.5`; 1 at
  `k = 18`) were stopped to free shared CPUs.
- `python3 sparse_single.py sparse_single.jsonl 50000 8 6,10,14,20 0.5,...,2.5 12`:
  C1 certificate. The 7 unfinished `k = 20, alpha = 0.5` runs were stopped.
- `python3 sparse_conflict.py 24 4 ...` and `python3 sparse_conflict.py 30 5 ...`:
  enumeration cliques. Also `python3 sconf_pool.py ...` (pooled cliques) and
  `python3 dp_vs_clique.py 12 4 6 5,6,7,8,10,14 ...` (exact minimum trees).
- `python3 block_pair.py`: Theorem 3 gadget, `k = 2..10`.
- `python3 bls_test.py`, `python3 bls_sweep.py bls_sweep.jsonl`,
  `python3 bls_big.py bls_big.jsonl 300000 20,...,70 1,2,4,8,L1,L2,L4 1 8 12`,
  and `python3 bls_big.py bls_big2.jsonl 300000 80,100,120,160 L2,L3,L4,L6 1 8 16`:
  binary MIMO. The run was stopped with `N = 120` complete except at
  `2 log N`, and `N = 160` barely started.
- `python3 cvp_count.py 8,...,32 30 ...` and
  `python3 cvp_clique.py 8,...,28 20 ...`: CVP shell counts and cliques. The
  Goldstein–Mayer `n = 28` runs were stopped unfinished.
