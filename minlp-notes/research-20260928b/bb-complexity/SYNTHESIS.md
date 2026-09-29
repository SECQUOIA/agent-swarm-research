# Relaxation-intrinsic complexity of branch-and-bound: synthesis

Program: [PROGRAM.md](PROGRAM.md). Date: 2026-09-29. This page collects the
results of the program, their verification status and what they mean for
solvers. "Reviewed" means checked by an independent research agent that did
not write the material, not journal peer review. An unsuccessful literature
search does not establish novelty.

## The question

Branch-and-bound (B&B) is the core of every global MINLP solver, yet its
theory is mostly linear: tree-size bounds exist for MILP with LP
relaxations, while spatial and nonlinear B&B had upper estimates (the
cluster problem literature) and worst-case lower bounds, but no
instance-dependent characterization. The program asks what determines the
size of a B&B tree when the node relaxations are nonlinear, and when
branching choices can or cannot help.

## The answer in one paragraph

For spatial B&B with relaxations whose gap vanishes only at box vertices
(alphaBB-type and secant relaxations), the minimum certificate size is,
up to `C log(1/eps)`, a multi-scale covering number of the near-optimal
set; the `eps`-exponent is half the box-counting dimension of the optimal
set, and this lower bound holds for every adaptive tree, branching rule,
node order and same-relaxation bound tightening. For face-exact
relaxations (McCormick, multilinear envelopes) the exponent depends on
how the near-optimal set meets the faces where the gap vanishes, and
where branching points are placed matters by polynomial factors.
Objective-cutoff propagation escapes these bounds only through
"one-sided" expression graphs; with dependency cancellation the bounds
survive. For integer branching with convex relaxations, the class number
`kappa` bounds every convex-piece tree and is exact for arbitrary convex
pieces; curvature, not constraints, makes it large. In random sparse
regression the perspective relaxation makes every variable-branching tree
linear-size above an explicit sample threshold that lies strictly below
the root-exactness threshold, while pure-noise and low-SNR regimes force
exponential trees. SCIP 10 node counts follow the predicted exponents once
its search matches the model.

## Results

### Spatial branching, second-order gaps

[Constrained note](spatial-constrained/instance-dependent-node-complexity.md).
[Review](../reviews/spatial-constrained-review.md),
[recheck](../reviews/spatial-constrained-recheck.md); earlier
[unconstrained review](../reviews/spatial-bb-review.md).

- **Stratified lower bound (Theorems 4.5, 4.6).** For every adaptive tree,
  node order, valid incumbent and same-relaxation tightening,
  `N_opt(eps) >= c alpha^{d/2} ∫_S (f - f* + eps)^{-d/2} dσ` for every
  feasible `d`-dimensional stratum `S` of positive reach, and a covering
  form without regularity. The new ingredient is a per-box arcsine bound
  with a coordinate multiplicity; bounded curvature alone is insufficient.
- **Characterization (Theorem 6.3).** `N_opt` and uniform bisection lie
  within `C log(1/eps)` of `Phi_alpha(eps) = sup_{eta>=0}
  N_inf(E(eta), 2 sqrt((eps+eta)/alpha))`. The supremum over coarser
  levels is necessary (Remark 6.3a).
- **Regular instances.** Nondegenerate KKT minima on `d >= 1` strata:
  `Theta(log(1/eps))`; unique vertex minimizer: `O(1)`; Morse–Bott optimal
  manifold of dimension `p`: `Theta(eps^{-p/2})`. First-order gaps give
  exponent `(n+p)/2`, including an `eps^{-n/2}` lower bound for the
  cluster effect valid for every adaptive tree.
- **Constraint-gap schemes (Section 5).** Slightly infeasible points below
  `f* - eps` must lie near box vertices; a constraint gap yields the same
  covering lower bounds as an objective gap under an outward-descent
  condition.
- **Novelty.** The unconstrained core transfers Lipschitz and bandit
  arguments (Hansen–Jaumard–Lu 1991; Perevozchikov; Munos; Bachoc–Cesari–
  Gerchinovitz 2021); Neumaier (2004) gives the heuristic MINLP precedent
  and Kannan–Barton (2017) the infeasible-side clustering mechanism. The
  defended claim is rigorous lower bounds for relaxation-based spatial B&B
  with adaptive trees, the stratified and constraint-gap forms, and the
  characterization.

### Spatial branching, face-exact (McCormick) relaxations

[Note](spatial-face-exact/face-exact-node-complexity.md).
[Review](../reviews/face-exact-review.md),
[recheck](../reviews/face-exact-recheck.md).

- The termwise McCormick gap vanishes exactly on box faces whose fixed
  coordinates form a vertex cover of the bilinear interaction graph.
- Transversal `p`-dimensional near-optimal strata force `Ω(eps^{-p/2})`
  leaves; on a tilted stratum `N_opt = (1/2) sqrt(theta/eps) + O(1)`.
- Convergence order alone does not determine node counts: McCormick and
  alphaBB can share order and prefactor while `N_opt` is 2 versus
  `Theta(eps^{-1/2})`.
- **Branching points.** Unclamped splitting at the relaxation point uses 3
  nodes on aligned kinks; a clamp fails on an uncountable null Cantor set of
  kink positions (for `a = 1/6`, clamp 1/5: at least `0.0745 eps^{-1/2}`
  nodes against `N_opt = 2`). Incumbent-point branching
  (Shectman–Sahinidis, used by BARON) realizes the `O(1)` certificates on
  the kink family, with the tie rule stated.
- Two conjectured characterizations (7.1 and 7.1') were refuted by
  reviewers; the remaining open question is whether row-slice bounds restore
  a characterization.

### Branching-point competitiveness

[1D note](branching-competitiveness/competitive-branching.md),
[n-dimensional note](branching-competitiveness/n-dimensional.md).
[Review](../reviews/competitive-review.md),
[recheck](../reviews/competitive-recheck.md).
[Lean formalization](../../formal/topics/33-competitive-branching/README.md)
with an independent [statement review](../../formal/topics/33-competitive-branching/reviews/statement-review.md).

- **Theorem 1 (1D, exact-gap relaxation).** Splitting every invalid node
  exactly at its relaxation minimizer uses at most `8 N_opt - 9` nodes, a
  ratio below 4 against every finished tree. Formalized in Lean 4 without
  `sorry`; 167 declarations audited, standard axioms only.
- Every rule that sees the relaxation solution (as a germ) has ratio at
  least 5/3 on piecewise-quadratic instances (Theorem 3); the minimizer
  rule attains 5/3 when `N_opt = 2`, and its worst ratio lies in
  `[11/5, 4)`.
- **SCIP's default rule** (midpull 0.75 scaled by global relative width,
  clamp 0.2 against local bounds; confirmed in the SCIP 10.0.2 source)
  loses `log(1/eps)` on an explicit instance, proved in exact arithmetic;
  the clamp alone forces the loss. Box-only rules lose `c_n log(1/eps)`.
- In `n >= 2`, splitting every coordinate at the minimizer is provably not
  competitive. For separable objectives
  ([note](branching-competitiveness/separable-omega.md),
  [review](../reviews/separable-omega-review.md)): every deterministic
  node-local rule has competitive ratio at least `(2G(n)+1)/3`, which is
  7/3, 11/3, 19/3, 31/3 for `n = 2..5` and grows like `2^{n+2}/(3n)`
  (Theorem C′, derived by the reviewer and proved by the author); the
  most-central-coordinate rule itself uses `2^{n+1} - 1` nodes against an
  optimum of 3 on a tie-free family. With one sharp coordinate it is
  constant-competitive (`<= 112 N_opt`, Theorem B). Whether it is
  `C_n`-competitive in general remains open; any such constant must be
  exponential in `n`.
- **Safe branching points** ([note](robust-branching-points/robust-branching.md),
  [review](../reviews/robust-branching-review.md)). Every clip schedule
  (a clamp whose fallback is the clamp zone's inner end, whatever the
  schedule) fails on an uncountable null set of kink positions; a
  deterministic recentring clamp, which places the relaxation point at the
  child's centre when it falls in the clamp zone, is exactly split-optimal
  among all rules that keep every child at least a `theta` fraction of its
  parent (it meets the lower bound `J(theta) + 1` with equality in 1D);
  randomized clamps are robust in 1D but not under widest-side selection.
  On MINLPLib all safe variants are neutral beyond seed noise (recentring
  0.92, CI 0.71–1.14, against SCIP's default), and removing the clamp is
  harmful (2.00, CI 1.43–2.96).
- **Novelty.** Modest: Hansen–Jaumard–Lu (1991) is the 1D Lipschitz
  precedent; Daskalakis–Diakonikolas–Yannakakis (chord algorithm) is the
  closest instance-optimality precedent.

### Objective-cutoff propagation

[Note](cutoff-propagation/cutoff-propagation.md).
[Review](../reviews/cutoff-review.md), [recheck](../reviews/cutoff-recheck.md), [closing audit A](../reviews/closing-audit-a.md).

- Fixed-point interval propagation of `f <= UBD - eps` is itself a node
  bound that depends on the expression graph, not only on `f`.
- One-sided representations can certify optimality with `O(1)` nodes (the
  cost moves to propagation rounds); representations with gradient
  cancellation and no dominant term keep every relaxation-gap lower bound
  with `alpha_eff = min(alpha, alpha_F)`.
- The same function and relaxation can need 1 node or `Theta(eps^{-1/2})`
  nodes depending only on the DAG. This refines Schichl–Markót–Neumaier's
  order-1 overestimation claim and contradicts it for one-sided
  representations.

### Integer branching with convex relaxations

[Note](integer-core/relaxation-intrinsic-bounds.md).
[Review](../reviews/integer-core-review.md),
[recheck](../reviews/integer-core-recheck.md); earlier
[scout review](../reviews/bb-conflict-review.md).

- **Class number.** `kappa_tau`, the fewest classes of integer points whose
  convex hulls have relaxation value at least `OPT - eps`, bounds every
  convex-piece tree (variable, split, multiway, SOS branching) and equals
  the minimum leaf count with arbitrary convex pieces, realized by a binary
  hemispace tree. Integer-variable cuts valid for the node's feasible points
  do not change it; incumbent-based tightening keeps a node form.
- `kappa` is weak for linear objectives (at most `m + 1` for pure ILPs) and
  split trees can be `2^{L^{Ω(1)}}` while `kappa <= L`; a quadratic
  Jeroslow instance has `kappa = 2` but needs `C(n+1,(n+1)/2)` leaves under
  variable branching.
- **Random CVP.** For a Haar-random lattice and uniform target, with high
  probability `kappa >= 2^{(0.2925-o(1))n}` for every basis, so no
  branching scheme with the continuous relaxation (including lattice
  reduction, sphere decoding, general disjunctions) is subexponential.
- **Perspective versus pairwise hull.** Explicit gadgets (including an
  asymmetric one) force `2^k` leaves under the perspective relaxation while
  the 2x2 block hull is exact at the root.
- **Novelty.** The counting mechanism is Dey–Dubey–Molinaro's; random CVP
  is the most novel part.

### Random sparse regression

[Note](sparse-regression/phase-transition.md).
[Easy-side review](../reviews/sparse-easy-review.md),
[hard-side review](../reviews/sparse-hard-review.md),
[PWE verification](../reviews/pwe-verification.md); revisions under
[recheck](../reviews/sparse-recheck.md).

- Root exactness of the perspective relaxation: sharp threshold
  `tau_lam^2 = 2 log p`, hence `n ≈ 2k log p` over all ridge choices, with
  converse (asymptotic, regime `log^6 p <= n <= p`).
- Condition C1 (every single wrong fixing prunable at the root), which makes
  every variable-branching tree linear-size when the incumbent `OPT` is
  available or best-bound search is used: threshold
  `tau_lam^2 = 2 log(p lam/n)`, hence `n ≈ 2k log(p/sqrt n)`. For
  `k = p^gamma` this is `alpha = 2 - gamma` against `alpha = 2` for the
  root, so linear trees hold strictly below root exactness.
- Pure noise and low total SNR force midpoint-conflict cliques of size
  `C(p,k)^{c'}` (asymptotic only; the explicit conditions are vacuous at
  practical sizes).
- **A published theorem is false as stated.** Theorem 2 of
  Pilanci–Wainwright–El Ghaoui (Math. Program. 151:63–87, 2015), a
  sufficient condition for exactness of the Boolean (perspective)
  relaxation under per-entry Gaussian noise, fails: by the paper's own
  Corollary 2 the exactness probability tends to a limit below 1 (0.123 in
  an explicit example) while the theorem claims probability tending to 1.
  The proof hides a normalization mismatch between its two appendix lemmas.
  Pilanci's 2016 thesis repeats the statement; later papers cite it as
  valid; no erratum was found. With total-energy noise the argument goes
  through, and the note's Theorem 3.1 gives the sharp asymptotic constant 2
  in the `n ≍ k log p` scaling. Two independent agents confirmed the
  counterexample with separate code.
- Observed C1 transitions at practical sizes sit at about half the
  first-order threshold; a second-order heuristic explains this.
- **Stronger convexifications in the `(z, beta, beta beta')` lift do not
  move the constants** ([note](sparse-regression/stronger-relaxations/thresholds.md),
  [review](../reviews/stronger-relaxations-review.md),
  [recheck](../reviews/stronger-relaxations-recheck.md)). Every relaxation
  between the perspective relaxation and the `r`-wise lifted hull in that
  lift with a global PSD lift (including the optimal-perspective SDP,
  rank-one relaxations and free-sign 2×2 hull decompositions) has the same
  sharp root and C1 thresholds when `r n log p = o(p)`: the lifted matrix
  can hide a fractional point's variance in the null space of `X`, so the
  fractional part costs only `lam(1 + o(1))`. Their large gains at small
  `p/n` fade as `p` grows. Lifting the cross products `z_j beta_m` inside
  the full PSD moment matrix escapes the obstruction (pairwise product
  cones in that matrix already do in experiments; pairwise hulls alone do
  not); the asymptotic constant of that stronger relaxation is open. Prior work cited
  by Bandeira et al. suggests hardness of approximate recovery below about
  `2(1-gamma) k log p`, with low-degree support only as `gamma -> 0`, so the
  windows between that and the proved thresholds remain open.
- **Novelty.** Theorem 3.2, Corollary 3.3 (linear trees below root
  exactness), the saturated witness and the node-count reading appear new;
  Theorem 3.1 is new as a sharp statement but uses the standard Lasso-style
  technique; the clique argument transfers Dey–Dubey–Molinaro.

### Random binary least squares (MIMO detection)

[Note](binary-least-squares/certification-thresholds.md).
[Easy-side review](../reviews/mimo-easy-review.md),
[hard-side review](../reviews/mimo-hard-review.md),
[recheck](../reviews/mimo-recheck.md),
[closing audit B](../reviews/closing-audit-b.md).

The same method gives a very different picture from sparse regression:

- The box relaxation is exact at the planted point with probability
  exactly `2^{-N}` at every SNR, because the relevant KKT signs do not
  depend on the SNR. The logarithmic "box relaxation threshold" in the
  literature concerns rounding, not exactness.
- Linear-size variable-branching trees (condition C1) need SNR linear in
  `N`: sharp at `rho = N/(4(2beta-1))` for `M = beta N` with `beta > 1`, and
  at `N/4` for square systems given a cited input.
- Between these regimes, every convex-piece certificate for the box
  relaxation of `f` has `exp(Θ((N/rho) log rho))` leaves (the lower-bound
  constant is tiny, about `1.4e-4`, and vacuous below `N ≈ 1.7e7`). At
  `rho = c log N`, where the maximum-likelihood point is found in
  polynomial time (Papailiopoulos 2026, square systems), certifying it with
  box-relaxation B&B needs `exp(Θ(N log log N / log N))` leaves.
- The gap is specific to the plain box relaxation: the SDP relaxation, and
  even a diagonal eigenvalue shift of the objective, are exact at
  `rho = Θ(log N)` for tall systems.
- The Gaussian-cone face law used for the root is known in substance
  (Hug–Schneider; McCoy–Tropp); ML achievability at `2 log N` is due to
  Hansen–Hassibi–Dimakis–Xu; the SDP tightness condition is
  Jaldén–Martin–Ottersten's.

### Solver validation and its limits

- [SCIP node exponents](solver-validation/scip-node-exponents.md)
  (empirical, SCIP 10.0.2, not independently reproduced). On 20 synthetic
  instances with best-first search and the incumbent fixed at `f*`, every
  applicable predicted exponent holds (slopes 0.50–0.52 for 1-dimensional
  optimal sets, about 1 for 2-dimensional, 0.25 for a quartic direction,
  logarithmic at isolated minima). Each departure of default SCIP traces to
  a named component: plunging, cutoff propagation, shared subexpressions,
  expansion of squares, variable-lock presolve.
- [MINLPLib branching-point study](minlplib-branching/branching-point-study.md)
  (empirical, 57 nonconvex instances, 3 seeds, 1,927 runs). The theory's
  branching-point recommendation does **not** transfer as a general rule.
  Moving SCIP's split to the LP point changes node counts by a factor 1.03
  (95% CI 0.83–1.26); removing the clamp as well multiplies them by 2.19
  (CI 1.43–3.39). Pure midpoint splitting is worse than the default (1.15,
  p = 0.009). The clamp protects against LP values that sit exactly on a
  variable bound, which produces chains of nearly identical nodes (a single
  path of 378,210 nodes on `ex4_1_5`). The exact-gap model cannot produce
  this, because a node whose relaxation minimizer lies on the boundary is
  pruned there. The theory's direction appears only on very small smooth
  instances. SCIP's default is already close to the LP point deep in the
  tree, because its midpoint pull vanishes below half the global width.

## What this establishes for solvers

Proved consequences:

- When the near-optimal set has positive dimension, no branching rule, node
  order or same-relaxation tightening avoids `eps^{-p/2}` nodes; only a
  different relaxation, a different representation (for propagation) or
  removing the degeneracy (for example symmetry breaking) can.
- Branching-point safeguards have a provable worst-case cost within the
  models: SCIP's default clamp loses a `log(1/eps)` factor on an explicit
  instance where splitting at the relaxation minimizer needs 3 nodes; for
  McCormick, a clamp fails on a Cantor set of kink positions, and
  incumbent-point branching recovers the optimal certificate on the kink
  family. The MINLPLib study shows this is not a practical recommendation
  to remove clamps: relaxation points on variable bounds, absent from the
  models, make the clamp protective on real instances. A model that
  includes boundary relaxation points is needed before any rule change
  can be justified.
- For integer problems, the class number measures when cuts, not branching,
  are needed; random integer least squares is exponential for every
  continuous-relaxation B&B.

Plausible applications, not established: online estimation of the
optimal-set dimension from the slope of `log(nodes)` against
`log(1/eps)`; adaptive selection between branching-point rules; choosing
the ridge parameter in sparse regression to reach the C1 regime.

## Open questions

- Whether the most-central-coordinate rule is `C_n`-competitive in `n`
  dimensions; any such constant must be exponential in `n`.
- A characterization of face-exact node complexity (whether row-slice
  bounds restore one).
- Whether split-tree size is polynomial in `kappa` for convex quadratic
  objectives.
- Finite-size versions of the sparse-regression thresholds, and the
  asymptotic constant of relaxations that lift the products `z_j beta_m`.
- A branching-point model that includes relaxation points on variable
  bounds, which the MINLPLib studies show is what matters in practice.
