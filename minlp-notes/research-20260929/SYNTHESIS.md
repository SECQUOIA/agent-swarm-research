# Structure, relaxations and branching: synthesis of the September 29 program

Date: 2026-09-30. Program: [PROGRAM.md](PROGRAM.md); log:
[root-research-log.md](root-research-log.md). "Reviewed" means checked by an
independent research agent that did not write the material, not journal peer
review. An unsuccessful literature search does not establish novelty.

## The question

Global MINLP solvers search one branch-and-bound (B&B) tree of boxes in the
full variable space and bound each box by a relaxation built term by term
from the model's expression graph. Many important models are sparse:
multi-period plans, networks, discretized dynamics. Their interaction graphs
have small treewidth while the dimension is large. The program asked what
this search-and-relaxation design costs on such models, what a
structure-aware alternative can achieve, and whether this explains open
benchmark instances.

## The answer in one paragraph

With termwise relaxations, single-tree spatial B&B needs a number of leaves
exponential in the dimension even on a path-structured problem with a unique
nondegenerate interior minimizer (proved: at least `0.57 (5/3)^n` leaves with
termwise McCormick). This is the case whose cost grows only like
`log(1/eps)` at fixed `n` (September 28 notes); the cluster-problem
literature estimated exponential growth in `n` here (Neumaier 2004;
Wechsung–Schaber–Barton 2014), and Theorem 1 makes this rigorous for
termwise relaxations at treewidth 1. A decomposition-aware certificate
that branches only on bags of a tree decomposition and passes affine
(Lagrangian) child bounds needs `O(|T| C^{w+1} log(|T|/eps))` work under
quadratic growth (an existence result centred at `x*`), so treewidth takes
the place of dimension (proved), and the slopes are essential: constant
child bounds provably need `Omega(eps^{-1/2})` cells. The separation is a
statement about fixed termwise relaxations, not about search alone: on a
tree decomposition, freely chosen splits of the objective make per-bag
relaxations exact, and SCIP's PSD-minor cuts escape both lower bounds.
Computationally, SCIP 10's node counts grow about fivefold per two added
variables on these chains while a chain dynamic-programming B&B solves
certified instances with 8192 variables. Instance-specific certificates
(Lagrangian and SDP duality, calibrations, comparison, tangent-plane tests,
concavity and exact identities, and for eg_* Taylor-model branch and bound),
each independently verified (eg_disc2_s partly by sampling), closed 31 MINLPLib instances listed as open (for the models as written; for 13 of
them the primal side is a point feasible only to row violations of 1e-20 to
8e-12), certified the intended relaxation of 6 KAN instances whose models
turned out to be exactly infeasible, raised the waterno2 dual bounds by
factors of 1.6–6.2 (for waterno2_06, branching on the tank-level
separators with cell-dependent slopes then cut the remaining gap to
1.67%), and brought
ann_cumene_tanh to within 0.194% of its best known point. In our reading of every closed case, the obstacle was
the relaxation (unbounded variables, long chains of nonconvex equalities,
hidden convexity or monotonicity, cancellation among many exponential terms
lost by termwise enclosures), not the amount of branching. A
systematic audit found 19 listed solver dual bounds on 15 instances
provably invalid (8 of them at tolerance scale).

## Results

### 1. Single-tree lower bounds on low-treewidth problems

[Face-exact note](theory-face-exact/face-exact-exponential.md);
[review](reviews/face-exact-review.md); [recheck](reviews/face-exact-recheck.md) (an independent exact-rational
B&B reproduces the corrected leaf counts).

- **Theorem 1 (termwise McCormick).** On the path family
  `f = sum_i g_i(x_i) + sum_i b_i x_i x_{i+1}` with `|b_i| = b`, `g_i'' <= D`
  near `x*`, every single-tree certificate (any branching rule, split
  points, node order, valid incumbent, same-relaxation bound tightening, the
  latter adding `2n` per tightening round) has at least
  `(1 + 1/S)^n exp(-lambda(1 + eps/(b r^2)))` leaves when `D/(2b) <= 1.99`,
  where `S = sqrt(1 + D/(2b))` and `r` is the radius of a cube around `x*`
  inside the root box. For the probe family this is `0.57 (5/3)^n`
  (`eps <= 1e-4`, `r >= 1/2`). It needs neither uniqueness nor
  nonconvexity: it holds for a strictly convex QP written with separate
  bilinear terms.
- **Theorem 2 (per-factor convex envelopes).** `c 1.205^n` for the natural
  factorization; the mechanism disappears near `x*` for a split
  factorization (outside that region the question is open).
- **Per-factor alphaBB on the bilinear terms** ([decomposition note](theory-decomposition/decomposition-certificates.md),
  Corollary 2.1; alphaBB on an isolated bilinear term is dominated by
  McCormick and not used by solvers, but this bound carries a `log(1/eps)`
  factor): `0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps))`, base
  `sqrt(2e/pi) ≈ 1.3154892`, exponential
  whenever the geometric mean of the per-variable alphaBB weights exceeds
  `pi/(4e)` times that of the Hessian eigenvalues.
- **Mechanism.** A center-of-box volume argument: at the center of a leaf's
  intersection with a cube around `x*`, the termwise gap grows with the sum
  over edges while the objective gap is limited by the distance to `x*`.
  This is the precise form of the heuristic "gaps add up over terms".

### 2. Decomposition certificates

[Decomposition note](theory-decomposition/decomposition-certificates.md);
[review](reviews/decomposition-review.md); [recheck](reviews/decomposition-recheck.md) (base rounding corrected: the
first revision's `1.3155` made the uniform ratio false for very large `n`;
that correction has not been rechecked);
[non-dyadic check](reviews/decomposition-nondyadic-check.md) and its
confirmations ([r1](reviews/decomposition-nondyadic-confirm-r1.md),
[r2](reviews/decomposition-nondyadic-confirm-r2.md),
[r3](reviews/decomposition-nondyadic-confirm-r3.md)).

- **Model.** Cells on each separator box, one affine minorant of the subtree
  value function per cell, a leaf cover of each bag box; the root bound is a
  Lagrangian relaxation of the separator copy constraints.
- **Theorem 3.4 (main new result).** Under quadratic growth
  `F - f* >= c_g |x - x*|^2`, factor gradients `M_a`-Lipschitz and
  vertex-vanishing relaxation error, a certificate of size
  `2|T| (4/theta)^{w+1} (log2(s0/h) + 2)` exists, i.e.
  `O(|T| (C M_a sqrt(w)/c_g)^{w+1} log(|T|/eps))` on paths. It never uses
  smoothness of value functions (kinks away from `x*` are harmless), and it
  tolerates a center error `O(sqrt(eps/|T|))` in the sup norm and multiplier
  errors `O(sqrt(eps))`. The cell-width-to-distance ratio must be small
  relative to `c_g/M_a`; computations show that this condition is real: a
  copy-drift pattern makes the gap grow linearly in `n` when it fails
  (Remark 3.6, observed numerically). The theorem is an existence result
  centred at `x*`. Its constant `c_g` is global: a second local minimizer
  within `delta` of `f*` at distance `D` makes the base
  `(C M_a D^2/delta)^{w+1}`, no better than the worst case when
  `delta ~ eps`.
- **Slopes are necessary (Proposition 2.6).** Constant child minorants need
  at least `|lambda*|/(6 sqrt(M_F eps))` cells at a separator with nonzero
  optimal multiplier (proved for a child of the root with a 1-D separator).
  This turns the first-order copy error of Robertson–Cheng–Scott (2025) into
  a certificate-size lower bound.
- **Width lower bounds for every tree decomposition.** `exp(Omega(w))`
  above the `pi/(4e)` threshold at nondegenerate minima, and
  `(n/(w+1))^{1+(w+1)/2} eps^{-(w+1)/2}` for flat blocks, which shows that
  the `n^{Theta(w)}` cost of splitting the tolerance across bags is
  unavoidable.
- **Separation (Theorem 4.1).** On the path family with the same
  relaxations on both sides, `N_single/N_dec >= 3e-10 (2e/pi)^{n/2}/sqrt(n)` for
  every `n >= 3` and `eps <= 1e-4` (alphaBB), and `c (5/3)^n/(n log(n/eps))` for termwise
  McCormick. Crossovers with computed decomposition certificates: `n = 29`
  (proven bound); actual bisection trees exceed them already at `n = 9`.
- **Adaptive algorithm and characterization** ([extension](theory-decomposition/extension-adaptive.md);
  [review](reviews/decomposition-adaptive-review.md),
  [confirmation](reviews/decomposition-adaptive-confirm-r2.md)). A
  level-synchronous algorithm that uses min-marginals from one extra DP pass
  and slopes from the previous minimizing configuration — no knowledge of
  `x*`, no problem constants, no local solver — produces, with monotone
  relaxations, a certificate of
  size `O(|T| (C sqrt|T|)^{w+1} log(|T|/eps))` (Theorem A.5), and the extra
  `sqrt|T|^{w+1}` factor is real for it: `Omega(n^2 log(1/eps))` leaves on
  the path family where `O(n log(n/eps))` certificates exist
  (Proposition A.6). The lower half of the covering characterization
  (Conjecture 3.7) holds if the power of `|T|` may depend on `w` and is false
  with a fixed-degree polynomial in `|T|` (Theorem B.2); a new pointwise
  lower bound (Theorem B.3) contains the earlier ones. The upper half was
  open beyond one separator; the follow-up below settles it in the
  exact-bag model for trees with one-dimensional separators. A later check found that the certificate code
  dropped touching (leaf, cell) pairs at non-dyadic centres; two zero-slope
  gaps in the original note's Section 5.3 table were corrected (the old
  values were still valid lower bounds).
- **Upper half of the covering characterization for one-dimensional
  separators** ([note](theory-decomposition/covering-upper-half.md);
  [review](reviews/covering-upper-half-review.md),
  [confirmation r1](reviews/covering-upper-half-confirm-r1.md),
  [r2](reviews/covering-upper-half-confirm-r2.md)). A new exact split, the
  graded split `psi_e = (1 − theta_e) U_e + theta_e L_e` with
  `theta_e = (2E_e + 1)/(2n)` (`E_e` edges below `e`, `n` edges), makes
  every edge's error free up to `w_e/(2n)`, where `w_e` is that separator's
  band width (Theorem 1, any tree and separator dimension; the factor
  `1/(2n)` cannot be improved for bounds of this form, Proposition 1.3).
  With a one-dimensional kink bound (Lemma 2: concave kinks can only
  sit where the band is wide; now sharp, though Theorem 3 uses its earlier
  constant 8), it gives, in the exact-bag model of
  Proposition B.4 and for trees with one-dimensional separators, cellwise
  affine splits with gap at most `eps` and
  `O(n log)` times the per-separator covering number of cells on each
  separator (Theorem 3; upper bound only, no band stability or copy-error
  hypothesis). Refinement driven by one-edge band brackets can stall: on an
  explicit two-edge example it never refines, and its gap stays at a fixed
  positive value (Proposition 4). For decomposition certificates
  (Definition 1.2) only a partial result holds: Proposition 5 proves a
  sufficient condition for certificates whose leaves are aligned with the
  cells, and the resulting size estimate is a sketch (at best reading
  (R2)); reading (R1) of Conjecture B.5 stays open, as do separators of
  dimension 2 or more.
- **Matching Theorem 3.4 without `x*` on paths** (round 4;
  [note](theory-decomposition/adaptive-matching.md);
  [review](reviews/adaptive-matching-review.md), confirmations
  [r1](reviews/adaptive-matching-confirm-r1.md),
  [r2](reviews/adaptive-matching-confirm-r2.md)). Algorithm GR runs one
  dynamic program per stage and refines leaves and cells only around the
  copies of the current minimizing configuration, with widths graded away
  from them; slopes come from the previous consistent point. It uses no
  pruning, no local solver and no knowledge of `x*`; unknown constants
  cost one more logarithmic factor (dovetailing). For path decompositions
  (any width `w`) with `∇F(x*) = 0`, it certifies `eps` with at most
  `2|T| j* (4R + 4/theta + 4)^{w+1}` boxes when `theta <= theta*` and
  `R >= 3K*` (explicit constants; `theta* ≈ 8.2e-8` on the path family),
  `j* = O(log(|T|/eps))` (Theorem 2, proved): the `|T| C^{w+1} log(|T|/eps)` form of Theorem 3.4,
  with a base quadratic rather than linear in `M_a/c_g` and numerically
  vacuous proved constants. The key step is a localization lemma: the
  minimizing configuration of the relaxed dynamic program lies within a
  constant multiple of the core width of `x*` in every bag, independently
  of `|T|` (Lemma 1, proved for paths; it also proves Conjecture A.7 on
  paths). In floating-point runs on the path family GR (`theta = 1/8`,
  `R = 4`) needs 12.1k–17.1k boxes per bag at `eps = 1e-4` for
  `n = 4…256`, flat in `n`, and at `n = 64`,
  `eps = 1e-4` it processes 4.7M boxes against 36.4M for the
  level-synchronous algorithm. Branching trees remain open (localization
  stated as Conjecture 7; the binary-tree computations do not separate size
  from conditioning). The bound-driven rule of the covering note provably
  needs `Omega(n^{3/2} log(1/eps))` cells on a strongly convex quadratic
  path (Proposition 6): its equal-share discount costs `sqrt(n)` per edge.
- **Worst case.** `(C n/eps)^{w+1}`; known in substance (Zhang–Sun 2022;
  Bienstock–Muñoz 2018). With absolute accuracy, `poly(n) g(w, eps)` is false
  under ETH (literature audit).

### 3. What the separation is about

- Both lower bounds are about **fixed termwise relaxations**. They hold for
  convex problems written with nonconvex terms. A chordal split of a positive
  definite path Hessian into PSD `2x2` blocks makes clique-wise PSD cuts
  exact on the convex variant, and a split factorization makes every factor
  convex near `x*` (with positive definite blocks; Griewank–Toint 1984,
  Theorem 4, and their local convexification; face-exact note, Section 9).
- **Observation 4.2 (decomposition note).** On a tree decomposition, if the
  objective may be split into arbitrary bag functions, splitting by the
  conditional margins makes per-bag convex envelopes exact at the root
  (equivalently, bag measures with equal separator marginals glue on a
  tree). So no lower bound can hold uniformly over all splits for
  relaxations that are exact at factor minima, such as convex envelopes;
  this says nothing about fixed rules such as alphaBB or about restricted
  split classes. The measure form is classical (Vorob'ev 1962; Lasserre
  2006).
- **Split-robust lower bounds** ([robust-lower-bound note](theory-robust-lb/robust-lower-bound.md);
  [review](reviews/robust-lb-review.md), [recheck](reviews/robust-lb-recheck.md),
  [confirmation](reviews/robust-lb-confirm-r1.md)). The probe family with `c = 0` is
  solved at the root by a fixed balanced split with exact envelopes
  (Proposition 2.1; the reviewers' 2.3–2.5 growth came from alphaBB). On a
  path, a split is a redistribution of one-variable functions, and the best
  split from a class chosen per box equals a relaxation whose neighbouring
  factor measures agree only on that class (Lemma 1.2; known in substance as
  dual decomposition / cost-shifting duality in graphical models and
  weighted CSP). Theorem 4.3 gives an exponential lower bound that holds
  for every split in natural classes (weighted unary splits; for each fixed
  degree `d`, a family defeating degree-`d` polynomial splits), even with
  splits chosen per node and with knowledge of `x*`, at a unique interior
  nondegenerate minimizer on a treewidth-1 chain. It is qualitative only:
  proved bases are about 1.003 (analytic) and 1.05 (computer-evaluated), the
  method cannot exceed about 1.063, and the family is built from nearly
  independent gadgets. Observed growth for weighted unary splits is about
  2.85 per variable; degree-6 splits grow 2.0 per variable and degree-10
  splits close the root gap.
- **Split-robust bounds on uniform chains** (round 4;
  [note](theory-robust-lb/robust-chains.md);
  [review](reviews/robust-chains-review.md), confirmations
  [r1](reviews/robust-lb-chains-confirm-r1.md),
  [r2](reviews/robust-lb-chains-confirm-r2.md),
  [r3](reviews/robust-lb-chains-confirm-r3.md), final
  [confirmation](reviews/robust-lb-chains-final-confirm-r1.md),
  [nits](reviews/round4-nits-confirm.md)). For uniform chains
  `sum u(x_i) + sum w(x_i, x_{i+1})` with symmetric `w` (including
  `b x_i x_{i+1}`), splitting each unary term evenly makes every interior
  factor exact in the bulk (Proposition A.1), and under a nondegeneracy
  hypothesis (H1) the balanced split has certificates whose size does not
  depend on `n` (Theorem A.2). So no split-robust lower bound that grows
  with `n` exists there for classes containing the balanced split, and the
  exponential bound of the face-exact note's Theorem 2 is, under (H1), a
  property of the unsplit factorization. Without (H1) the fixed balanced
  split can need at least `n/2` boxes (example WALL, every even `n >= 4`,
  `eps < 0.01134`), while reweighted
  classes are exact at the root. A translation-invariant chain with a
  chiral cubic coupling gives a split-robust exponential lower bound
  without gadgets or weak links, for every per-node split in class (a)
  (factorable relaxations sharing `x_i` and `x_i^2` lifts; Theorem C.3,
  proved); its bases are again tiny (1.0009–1.0087 analytic for window
  lengths 7–100, supremum 1.0093 not attained; 1.023 computer-evaluated;
  observed 1.75–2.3 per variable), a shared `t^3` lift
  closes it at the root, and order-2 sparse moment-SOS relaxations are
  exact at the root when the box constraints are placed suitably
  (Proposition C.5, proved; the gaps for other placements are floating
  point). A meaningful base was not achieved: with Lebesgue reference
  measure, volume-type counting is capped near `exp(c · gap/curvature)` per
  variable (other product measures were not optimized).
- For solvers this suggests three remedies: decomposition-aware search
  (proved on the path family, Section 2); consistency-strengthened
  relaxations (clique-wise PSD cuts are proved exact for the convex variant
  `kappa = 0` only; sparse moment hierarchies with bag-uniform error in the
  September 28 program); and tree Lagrangians with good multipliers plus
  exact treatment of the few windows where the local Lagrangian is
  nonconvex (supported by the closed instances of Section 5, not proved).

### 3b. Consistency relaxations: why affine splits plus short exact windows work

[Consistency note](theory-consistency/consistency-relaxations.md);
[review](reviews/consistency-review.md), [recheck](reviews/consistency-recheck.md),
[confirmation](reviews/consistency-confirm-r1.md).

On a tree decomposition, Lagrangian bounds (affine splits), separator
branching (piecewise splits on cells) and sparse moment relaxations
(polynomial splits) all enforce separator consistency through a class of
test functions; by cost-shifting duality (known in substance) each equals a
relaxation whose neighbouring bag measures agree only on that class.

- **Exact identity (one separator).** The relaxation gap equals exactly
  twice the sup-norm distance from the class to the "band" of exact splits
  (functions squeezed between the two conditional value functions). Errors
  matter only near optimal separator values, where the band is thin.
- **Trees.** `2 max_e dist_e ≤ gap ≤ 2 inf over joint exact splits of
  sum_e dist_e`. Both ends are attained in some instances: the upper end in
  the separable instance T1 (`K = 0`); the lower end, numerically, in 515 of
  900 random three-bag instances. In T1 with coupling `K`, the lower end is
  approached as `K` grows and, as proved, not attained at any finite `K`.
  The per-edge version is false (a three-bag counterexample with a constant
  in every band has gap 1).
- **Kinks.** A kink of the value function at an optimal separator value
  forces `Theta(1/n)` gaps for degree-`n` polynomial classes (proved lower
  bound `1/(30(3+c)n)`). For a zero-width band `n·gap → 2 beta = 0.5603`
  (Bernstein's constant `beta`); for a band that opens quadratically this
  limit is a conjecture. Semiconcavity makes affine splits second order at
  interior optimal values; piecewise-affine cells give `O(h^2)` (1-D
  separators; a 2-D counterexample shows the per-cell bound fails in
  higher dimension).
- **Consequences.** The lower-bound halves of the repository's September 28
  sparse-moment rates (`R^-2` smooth, `R^-1` at kinks) follow from
  identities already proved there; evaluating the best-approximation errors
  raises their constants about 8x and 12x (asymptotic, floating point). Piecewise polynomials aligned with kinks
  converge exponentially in the number of coefficients, but coefficient
  count is only a proxy for cost. The certificates that closed open
  instances fit the pattern "affine splits plus full consistency on short
  windows".
- **Novelty.** New as far as found, and elementary: the exact identity with
  its clipping proof, the tree lower bound and counterexample, the kink
  bound, the shell count. Known in substance: the duality; the one-sided
  bound (de Farias–Van Roy; on paths the tree upper bound is their
  approximate-LP bound); its positive-width form (Grimm–Netzer–Schweighofer
  2007, quantitative in Korda–Magron–Ríos-Zertuche); the zero-width identity
  (Han–Jiao–Weissman; the September 28 notes); the bracket form
  (robust-lower-bound note, Proposition 3.3).

### 3c. Dense linear coupling (modest, largely negative)

[Coupling note](theory-coupling/coupling.md); [review](reviews/coupling-review.md),
[recheck](reviews/coupling-recheck.md).

Extending the structure results to tree-structured nonlinearity plus `k`
dense linear rows gives: a tree version of Shapley–Folkman (at most `k`
fractional components; the per-bag gap bound fails, with gap `cn/4` for
one row); zero cost from the rows when the Lagrangian has quadratic growth;
an augmented-Lagrangian partial-sum certificate of size
`|T| C^{w+1} Γ^{kΔ} log^2(...)`; and unavoidable `exp(Omega(k))` dependence.
Shapley–Folkman bounds the gap, not the certificate: B&B with Lagrangian
node bounds needs `C(n+1,(n+1)/2)` leaves on a one-row instance (without
bound tightening; the count is Jeroslow's and the dynamic program is
Vavasis's (1992); the contribution is the transfer to continuous spatial
branching with Lagrangian bounds), while a lifted box certificate needs
`3n^2 - 3n + 2`. Practically, dualizing up to 8 linear rows raises the share
of large nonconvex MINLPLib instances with width at most 12 only from about
15% to about 17% (14.8% with the coupling note's baseline, which first
removes objective and objective-defining rows and takes the smaller of the
two width bounds; 13.6% in the census): the census gap comes from wide
linear structure, not from a few dense rows.

### 4. Computation

[Scaling study](computation/scaling-study.md); [review](reviews/computation-review.md).

- SCIP 10 on the path family (5 seeds, 300 CPU-s): geometric-mean nodes
  220–240, 1.5–1.8k, 7.1–7.8k and 29–37k at `n = 4, 6, 8, 10`; nothing
  solved from `n = 14`. The growth is the same under best-first search,
  OBBT at nodes with a solved LP, a single nonlinear objective, and
  optimality emphasis; supplying the optimum barely changes the counts, so
  the cost is in proving the bound. Local power-law exponents rise from 4.7
  to 8.1, which argues against a fixed-degree polynomial.
- A chain DP B&B prototype with valid bounds (independently bracketed on 33
  instances up to `n = 256`) solves certified instances with a unique,
  interior, nondegenerate, but globally nonconvex minimizer up to
  `n = 8192` in 13–19 s, work about `n^1.6–1.8`.
- Limits: one solver; paths only; prototype bounds use a rounding analysis
  rather than interval arithmetic; failures and heavy tails on probe3
  (amp 0.3: one of five seeds exceeds the pair cap at `n = 2048`, no
  setting solves `n = 8192`, cost across seeds up to 1800 times the
  median); prototype times are wall-clock seconds under load, SCIP times
  CPU seconds.

### 5. Open MINLPLib instances

[Report](open-instances/open-instances-report.md);
[independent verification](reviews/open-instances-verification/verification-report.md).

Rigorous dual bounds (interval or exact rational arithmetic, rechecked with
independent code) close the MINLPLib gaps of lnts50–400, dtoc5,
camshape100–800 (exact optima in closed form), lukvle10 (gap 1.4e-9) and
optcdeg2 (first 2.1e-5 relative; later closed to 9.0e-16 by one quadratic
calibration, Section 8). Measured
against the best single-solver bounds on the instance pages (not the
three-solver metadata), the improvements are marginal for camshape100 and
lnts50 and substantial for dtoc5 (listed dual 0.0024 vs optimum 5.39) and
camshape200/400/800 (listed gaps about 8%, 16%, 20%). MINLPLib's listed
primal values for camshape400/800 come from points violating rows by 3e-10
that lie below the exact optimum, because the chain amplifies tolerance
violations (Chebyshev weights up to 600). The mechanisms are classical:
discrete Sturm comparison (camshape), Mangasarian/Arrow-type sufficiency
(dtoc5), the linear-tangent law (lnts), a monotone head block (optcdeg2),
and a 2-D interval B&B on an end window (lukvle10). The generic cell-constant
separator DP failed (camshape needs cells of width `O(1/n^2)`), consistent
with Proposition 2.6, and branching on part of the separator failed on
optcdeg2; the working certificates used affine child bounds with good
multipliers.

**Second wave** (consolidated in [open-instances-summary.md](open-instances-summary.md)).
Verified: hvycrash solved exactly (the objective is constant on the
feasible set), ex6_2_7 and ex6_2_5 (Gibbs energy; an ε-global method,
McDonald–Floudas 1997, very likely solved them; not confirmed), etamac
(hidden convexity) and pricing050 closed; waterno2_06–24
duals raised by factors of 1.6–6.2 (remaining gaps 4.9–10.8%) through an exact
period decomposition. Also verified: chain50–400 closed to 1e-14 by a discrete catenary calibration
(a discrete Weierstrass field) plus an end-window B&B, and catmix100–800
closed to 1e-11–5e-10 by an exact DP on a 1-D projective separator whose
concave value functions make chord interpolation second order — the fix for
the first wave's failed cell-constant DP. Found along the way, and proved:
listed LINDO dual bounds that are invalid (methanol50 by 1.2%;
rocket100/200/400 by about 1e-7 relative, below MINLPLib's 1e-6 tolerance
and outside the audit's 19 pairs),
and SCIP 10.0.2 returning wrong optimal values on waterno2 period
subproblems because of an invalid in-tree bound reduction (not reported
upstream). A systematic audit of all MINLPLib listed bounds then
proved 19 solver bounds on 15 instances invalid (11 beyond MINLPLib's 1e-6
convention, including ANTIGONE/BARON on ghg_3veh and COUENNE/LINDO on
glider100 by a factor of about 784, though 7 of these 11 are below common
1e-4 gap tolerances; 8 at tolerance scale, including CPLEX/GUROBI and
BONMIN); all 19, and the two-sided optimum enclosures of the four emfl
instances, have been confirmed with code independent of the audit's (14
pairs by the first verification, the other 5 and three emfl instances by
the recheck; [audit](bound-audit/audit-report.md)).

Completion work then closed powerflow0030p/0039p/0039r (an exact-rational
SDP-dual certificate; for 0039 an exact identity at a leaf bus plus vertex
cuts), pindyck (the reduced objective proved concave on a polytope
containing the feasible set, after an entrywise interval-Hessian attempt in
wave 2 failed) and optcdeg2 to rounding level (Section 8);
certified the six KAN instances' intended network relaxations to about
1e-10 (their OSIL models have no exactly feasible point, proved by Sturm and
resultant certificates); gave ann_cumene_tanh its first finite dual bound
(gap 19%; verified with caveats: the full 3600 s run was not repeated);
and independently certified every period bound behind the waterno2 duals.
Follow-ups on the two unclosed families (independently verified):
waterno2_06's dual rose from 263.735099 to 272.584700 (gap 7.26% → 3.78%)
by branching on the tank-level separators — 113–162 cells per link, a
rigorous bound for each (entry cell, exit cell) pair of each period, the
horizon row replaced by an exactly derived terminal-volume row, and an exact
shortest path over the cell pairs
([note](open-instances-wave2/waterno2/separator-branching.md);
[review](reviews/waterno2-sepbranch-review.md), which re-bounded all 8,958
pair bounds with independent code). This is the decomposition certificate
of Section 2 with one fixed slope per link. KKT slopes from the best known
point were nearly tight along its trajectory but poor elsewhere (an
estimated 223 on a uniform grid); the minimizing cell path of the
certificate leaves that trajectory, and the remaining gap comes from level
regions where the slopes and cells used still allow profitable jumps.
waterno2_09–24 were not attempted with separator branching or cell
slopes. ann_cumene_tanh's dual rose
from −4024.495 to −3386.5403 (gap 19% → 0.194%) with affine arithmetic
(one noise symbol per tanh neuron), a per-box LP dual and domain reduction
([note](open-instances-wave3/ann/extension.md);
[review](reviews/ann-extension-review.md), which re-certified every closed
region and open box with its own code); the remaining boxes lie along a
nearly flat active constraint surface.
Round 4 went further on waterno2_06: giving each separator cell its own
slope vector is valid when that vector is used for both periods sharing
the link (the only coupling condition the proof needs), and old pair bounds can be re-used at new slopes through
an exact correction. With slopes chosen cell by cell and further
refinement, the certified dual rose to 278.230573 (gap 1.67%)
([note](open-instances-wave2/waterno2/cell-slopes.md);
[review](reviews/waterno2-cellslopes-review.md), which re-bounded all
49,315 pair bounds the certificate uses with independent code). Whether
cell slopes beat further splitting per unit of work was not established.
In wave 3, interval branch and bound with natural and mean-value
enclosures stayed below the listed bounds on eg_int_s and eg_disc2_s
(eg_disc_s was not run). In
round 4 all three were closed to a relative 1e-9 against exactly feasible
points: eg_int_s 6.45310315 (listed dual 6.33), eg_disc_s 5.76053961
(listed 3.37) and eg_disc2_s 5.64210057 (listed 0)
([note](open-instances-wave3/eg/retry.md);
[review](reviews/eg-retry-review.md), which re-certified every leaf of
eg_int_s, eg_disc_s and the optimum-containing part of eg_disc2_s, and a
sample of the other parts, with independent code). The method is a
reduced-space branch and bound whose second-order Taylor models keep the
signed cancellation among the 97 Gaussian-kernel terms of each row, with a
per-box LP over the minimax rows and domain reduction. eg_int_s had been
solved in floating point by SCIP 8.1 in the literature (Göß–Burlacu–Martin);
no closure of the other two was found.
In all, 31 instances listed as open were closed for the model as written,
all with independent verification. For 13 of them (lnts50–400, dtoc5,
lukvle10, chain50–400, powerflow0030p/0039p/0039r) the primal side is a
point feasible to row violations of 1e-20 to 8e-12; closure is measured
against its value, and no exactly feasible point was constructed.

### 6. Census

[Census report](treewidth-census/census-report.md). Among 582 nonconvex
MINLPLib instances with at least 100 nonlinear variables, 13.6% have
factor-incidence width at most 12 and 62.7% have nonlinear-term width at
most 12 (heuristic upper bounds; a root computation, not independently
reviewed). In MINLPLib's listing before this work, constant-width families
whose best known gaps grow with size included waterno2 (solved up to 4
periods, open from 6), camshape and lnts; camshape and lnts have since been
closed (in our reading, the obstacle was the relaxation). The census does
not show that width causes the difficulty: size, scaling and unbounded
variables grow too.

### 7. Singularity theory of node counts (secondary line)

[RLCT note](rlct/rlct-node-complexity.md); [review](reviews/rlct-review.md);
[recheck](reviews/rlct-recheck.md); [second recheck](reviews/rlct-recheck2.md).

For objectives with Lipschitz gradient on a box and relaxations whose gap
is of alphaBB type (quadratic in the box width), the optimal certificate
size and uniform bisection lie within factors that do not depend on `eps`
of `max_F integral_F (m + eps)^{-d_F/2}` over the faces `F` of the box (no
log slack, no doubling condition). The factors depend on `n` and on
instance constants (relaxation and Hessian constants, box side, values at
non-optimal vertices); the upper constants are exponential in `n`. For
analytic objectives this gives `N_opt ≍ eps^{lambda - n/2} (log 1/eps)^{theta - 1}` with `(lambda, theta)`
the real log canonical threshold and multiplicity when the minimizers are
interior, a face-wise version otherwise (the interior-only statement is
false: a 4-D counterexample grows like `eps^{-3/4}` where it predicts
`eps^{-1/4}`), and, for non-identifiable exact-data least squares, exponents
given by Watanabe's learning coefficients. The link between B&B complexity
and RLCTs appears to be new; the RLCT–volume link itself is classical.

### 8. Discrete calibrations and bang-bang transcriptions

[Calibration note](theory-calibration/scouting.md) ([review](reviews/calibration-review.md),
[recheck](reviews/calibration-recheck.md), [confirmation](reviews/recheck-calibration-confirm.md));
[bang-bang note](theory-bangbang/report.md) ([verification](reviews/bangbang-verification/verification-report.md),
[confirmation](reviews/bangbang-root-fixes-confirm-r2.md)).

Every certificate that closed a transcribed control or variational instance
here is a *discrete calibration*: verification functions `S_t` whose stage
residuals `L_t + S_{t+1}∘f_t − S_t` are bounded below (Krotov's discrete
condition; the Bellman inequality of approximate dynamic programming). The
closed instances use affine `S_t` (the discrete costate: dtoc5, lnts),
affine plus exact windows (lukvle10), field-type `S_t` (chain), concave
piecewise-linear `S_t` (catmix), comparison certificates (camshape) and a
quadratic calibration (optcdeg2).

- **Proved (elementary; the framework is classical):** an exact affine
  calibration exists iff some multipliers (the discrete costates, for smooth
  interior data) make every stage residual globally minimal on the
  trajectory ("only if" needs `f*` attained); a mesh-uniform Euler version
  holds under Mangasarian with margin or a strict pointwise sufficient form
  of the Leitmann–Stalford condition. A transfer theorem: a strict smooth
  continuous-time calibration plus an `O(h)` costate correction gives exact
  certificates for every sufficiently fine Euler transcription, provided
  the calibration is exact, strict and `C^4`, the state and control sets
  are compact, the optimal controls are interior and the Euler KKT points
  converge uniformly (with `U = R` the Euler transcription is unbounded
  below for every `h`).
- **Bang-bang switches (window law**, under the hypotheses (W1)–(W5) of the
  bang-bang note's Theorem 2.3). Non-tangential calibrations fail on a
  window of fixed duration around a regular switch (`Theta(1/h)` stages);
  tangential ones (whose switching function has zero state gradient at the
  switch) fail on `O(1 + e_h/h)` stages. Every `C²` calibration exact on the
  trajectory is tangential; in Osmolovskii–Maurer's Riccati test, tangency is
  the no-jump case. The needed `O(h)` discretization rate is established for
  linear problems but unverified for nonlinear ones.
- **optcdeg2 closed** by one quadratic calibration whose curvature vanishes
  at both switches: exact certificate value 293.876075095875092379…
  (truncated) against a rigorously feasible 293.87607509587509328
  (independently verified in exact rational arithmetic).
- **State dimension at least 2** ([extension](theory-bangbang/extension-n2.md);
  [review](reviews/bangbang-n2-review.md),
  [confirmation](reviews/ext-bangbang-n2-confirm.md)). In the local
  formulation, existence of tangential strict quadratic calibrations is
  decided by one number,
  `eta_L = b^T(Q(tau+) b − w)` with `Q` the last arc's Lyapunov solution: if
  `eta_L > 0` they exist (explicit construction); if `eta_L < 0` no exact
  calibration that is `C^3` on a uniform tube exists. The earlier conjecture
  ("tangential calibrations exist iff there is no conjugate point") is false
  in that reading: an `n = 2` example satisfies the classical second-order
  sufficient condition `F''(tau) = D + Delta^2 eta_L > 0` yet admits no such
  calibration. The maximal tangential Hessian is the Osmolovskii–Maurer
  rank-one Riccati jump with `D(H)` set to zero. This settles the
  continuous existence question in the local formulation only. The transfer
  theorem needs the global form, which can fail even when `eta_L > 0`
  (Example C, a floating-point blow-up); a transfer theorem for local
  calibrations is open.
- **Window exactness** ([note](theory-bangbang/window-exactness.md);
  [review](reviews/window-exactness-review.md), confirmations
  [r1](reviews/window-exactness-confirm-r1.md),
  [r2](reviews/window-exactness-confirm-r2.md),
  [r3](reviews/window-exactness-confirm-r3.md)). The window-exactness
  assumption of the bang-bang note's Theorem 4.1 (transfer with
  `O(1)`-stage switch windows) is decided by the sign of one
  data-determined number, the switch self-curvature
  `kappa_tau = b(x*(tau))^T w`, which every `C²` calibration exact on the
  trajectory shares. Under the hypotheses of Theorem 4.1 plus an exact
  terminal term (which the conclusion `B = f*` also needs; it was missing
  from Theorem 4.1's statement and has been added) and `b(x*(tau)) != 0`:
  `kappa_tau > 0`: every stage is exact, no window is needed, and the rate
  `e_h <= c_* sqrt(h)` with a specific small `c_*` (in particular
  `e_h = o(sqrt(h))`) suffices. `kappa_tau = 0` (with `e_h = O(h)`): at
  most one stage fails, at order `h^3`, and one window of `O(1)` stages is
  exact. `kappa_tau < 0`: on grids whose KKT point has a fractional stage
  (a positive fraction of grids by a heuristic phase model), every window
  of `o(1/h)` stages falls short by order `h^2` for the transferred
  calibration, so a repair needs a window of fixed duration; for LQ data
  this holds for all quadratic families with the discrete costate slopes
  that are exact over `R^n × U` after the window and at the terminal
  (families exact only over the state boxes are not covered). Checked in
  exact rational arithmetic on toys.
- **Singular arcs** ([note](theory-bangbang/singular-arcs.md);
  [review](reviews/singular-arcs-review.md), confirmations
  [r1](reviews/singular-arcs-confirm-r1.md),
  [r2](reviews/singular-arcs-confirm-r2.md),
  [r3](reviews/singular-arcs-confirm-r3.md)). A `C²` calibration exact on a
  singular arc is tangential along the whole arc; with several controls
  tangency implies Goh's condition, and the residual curvature equals
  Kelley's coefficient, so exact calibrations imply Kelley's condition
  (classical conditions in calibration form; that form was not found in a
  limited search). For the Euler transcription the sign of `b^T w`
  decides: if positive, transferred tangential families have no failing
  stage (given a discrete rate `o(sqrt(h))` near junctions; exact rational
  certificates on a 2-D test); if negative, no family with bounded Hessians
  and `K_t ⪯ hΛI` (the Hessian may drop by at most `O(h)` per stage going
  backward; Hessians that change by `O(h)` per stage are one example) is
  exact at fractional stages (isolated stages can be exact through `O(1)` Hessian
  drops), and a smooth KKT point with a run of fractional stages is a
  saddle; the discrete optimum chatters in the tested examples (E2 and
  catmix; observed, not proved). `b^T w` depends on the formulation and the
  scheme; the calibration-independent quantity is an accessory symbol
  `f(pi)`. For catmix, the COPS trapezoidal rule has `f(pi) < 0`, which
  explains its chattering optimum (heuristic: against a smooth reference
  with free junction stages the predicted chattering gain agrees within 3%,
  and the lowest Hessian eigenvalue there is within 0.1% of the
  finite-section estimate; the gain comparison depends on the reference by
  up to a factor 3.2, and at the oscillating KKT point the eigenvalue lies
  21% below the symbol minimum). No rigorous catmix certificate was built
  this way; catmix was closed by the DP certificate of Section 5.
- **What works when `kappa_tau < 0`, and several switches** (round 4;
  [note](theory-bangbang/kappa-negative.md);
  [review](reviews/kappa-negative-review.md), confirmations
  [r1](reviews/kappa-negative-confirm-r1.md),
  [r2](reviews/kappa-negative-confirm-r2.md),
  [r3](reviews/kappa-negative-confirm-r3.md), final
  [confirmation](reviews/kappa-negative-final-confirm-r1.md),
  [nits](reviews/round4-nits-confirm.md)). For LQ-structured data:
  branch and bound on the fractional control with node-specific
  calibrations cannot give an exact certificate with finitely many nodes
  when the families are `kappa`-limited (Corollary 4.2), and
  `epsilon`-certificates need and suffice `Theta(log(h^2/epsilon))` nodes
  (Theorem 4.3, leading order; the lower bound for a stated family class).
  *Lifted* calibrations, which treat the fractional control as a parameter,
  give exact bounds `J(zbar)` on a central node that contains an
  `h`-independent neighbourhood (Theorem 5.4, under a neighbour-margin
  condition and `e_h = o(sqrt h)`); that a bounded number of outer nodes
  suffices is heuristic. Exact rational certificates of `f* = J(zbar)` were
  obtained this way on every documented grid of the scalar toys (1–9
  nodes); on the two-state example A− the construction passed only a float
  screening. At leading order
  the discrete optimum does not chatter near a regular switch (Lemma 3.1,
  Proposition 3.2), but a local search can return a non-optimal KKT point
  (seen once). The toy's convexification is an exact identity for constant
  `b` and affine `l_1`, but convex only in special cases. For several
  switches, Theorems A and B hold switch by switch (sketch level, by
  locality); a tangential calibration across two close switches exists
  only if a new coupling condition holds (Proposition 7.1, `b` constant); with terminal rows the terminal condition is needed
  only on `ker C` (with the discrete rate for fixed endpoints assumed),
  which makes optcdeg2 an instance of the `kappa = 0` theorem up to the
  unverified rate and (H3) hypotheses.
- **Open:** the global-model versions (sketches); a transfer theorem for
  local calibrations; `kappa_tau < 0` beyond LQ data and a proof that few
  outer nodes suffice; asymptotics for close switches; state
  constraints.

## What this means for solvers

- **Proved.** Termwise relaxations in a single box tree cost `exp(Omega(n))`
  leaves on explicit treewidth-1 families, even at a unique nondegenerate
  minimizer; decomposition-aware certificates with Lagrangian slopes of size
  `O(n log(n/eps))` exist on the same families with the same relaxations.
  These certificates are built around `x*`. An algorithm that does not know
  `x*` (Theorem A.5) needs `O(n^2 log(n/eps))` leaves here, still
  polynomial, and its level-synchronous rule provably needs
  `Omega(n^2 log(1/eps))`; the graded-refinement algorithm GR, which also
  does not know `x*`, needs `O(n log(n/eps))` on path decompositions with
  `∇F(x*) = 0` (round 4; proved, with numerically vacuous constants). The proven single-tree bound overtakes computed
  certificates only from `n = 29`, so at practical sizes the separation is
  qualitative. Slopes are necessary.
- **Evidence.** SCIP 10's node counts grow about fivefold per two added
  variables on these families (`n = 4–10`; power laws of degree 5–6 fit
  equally well, so exponential growth is not established rigorously).
  Default SCIP is outside the theorems' relaxation class (its minor
  separator adds PSD cuts), so the theorems neither predict nor explain
  these counts. In MINLPLib's listing before this work, constant-width
  families became open as they grew; the census does not show that width is
  the cause, since size, scaling and unbounded variables grow too, and lnts
  and camshape have since been closed. 31 open instances were closed with
  instance-specific certificates, most within minutes; the largest
  (eg_disc2_s) took 3.4 CPU-hours (38 min on 8 processes) and catmix800
  about an hour; about half (15) use affine or state-dependent splits along
  chains plus short exact windows.
- **Plausible capability.** A solver component that (i) finds a tree
  decomposition of the expression graph, (ii) derives bounds for free
  variables from objective level sets and propagation along the tree,
  (iii) computes tree-Lagrangian bounds from a local solution's multipliers,
  and (iv) branches only inside the windows where the local Lagrangian is
  nonconvex. Waves 2 and 3 tested this. They closed 17 more instances and
  round 4 three more (eg_*), but
  waterno2 remains 1.7–10.8% open (waterno2_06 after separator branching
  with cell slopes), ann_cumene_tanh keeps a 0.194% gap, and several
  closures (hvycrash, ex6_2_*, etamac, pindyck, powerflow, and the eg_*
  closures of round 4) did not use the tree mechanism.
- **Not shown.** A general implementation; performance on instances with
  dense linear coupling (the factor-incidence width is small for only about
  one in seven large nonconvex instances); results for solvers other than
  SCIP 10.

## Novelty position

See the [literature audit](literature/decomposition-bb-prior.md). Discrete
AND/OR search separations, MILP B&B lower bounds at treewidth 2 (Basu et al.
2023; Dey–Shah 2022), two-stage decomposition B&B with convergence-order
theory (Cao–Zavala; Kannan; Li–Grossmann; MUSE-BB; Robertson–Cheng–Scott
2025), nested decomposition bounds (Zhang–Sun 2022) and Bienstock–Muñoz LPs
are prior. Berenguel et al. (JOGO 2013), read in full by the recheck, is the
precursor of the algorithm for subfunctions sharing one variable (copy
relaxation, zero-slope bounds), with bound-validity results only. Not found
elsewhere: rigorous single-tree lower bounds at a unique nondegenerate
minimizer for face-exact (termwise McCormick) relaxations (for relaxations
with gap at least `alpha q_B` such bounds are in the repository's
September 28 constrained note, Theorem 3.1, and the cluster-problem
literature, Neumaier 2004 and Wechsung–Schaber–Barton 2014, predicted the
growth as estimates); instance-dependent decomposition-certificate bounds;
the slope lower bound; the RLCT characterization; and rigorous certificates
for the 31 closed instances (ex6_2_7 and ex6_2_5 very likely already had
ε-global solutions, McDonald–Floudas 1997, by a known method; eg_int_s was
solved in floating point by SCIP 8.1; camshape100 and lnts50 were already
within 1.2e-6 and 3.8e-5 relative of closure). The
follow-ups add, within short searches only: the graded exact split and its
margin-discounted sandwich (the ingredients, mixed forward and backward
messages and convex combinations of exact splits, are standard); the
window-exactness trichotomy (the number `kappa_tau` itself is, up to a
factor, the switch cross term of the Osmolovskii–Maurer quadratic form;
what appears new is its role as the control curvature of every tangential
stage residual); and, for singular arcs, the discrete sign criterion and
the accessory-symbol explanation of catmix's chattering (the Goh and Kelley
connections are classical).

## Open questions

- A single-tree lower bound with a good base that is robust to how the
  objective is split, for problems nonconvex away from the minimizer (the
  split-robust method cannot exceed about 1.063 per variable on the gadget
  family; round 4 proved that none growing with `n` exists for symmetric
  uniform chains under (H1) for split classes that contain the balanced
  split, and found only tiny bases for chiral chains).
- The right base in Theorem 1 (termwise relaxations grow by 2.7–3.5 per
  variable in the data; minimal grid certificates, which are upper bounds,
  by 2.5–3.2; Conjecture 5.4 proposes `c 2^n`) and a `log(1/eps)` factor
  with a good base.
- An algorithm without knowledge of `x*` that matches Theorem 3.4 on
  branching tree decompositions and without `∇F(x*) = 0` (solved for path
  decompositions with `∇F(x*) = 0` by GR in round 4; open for trees, where
  it reduces to a localization property, Conjecture 7), and with practical
  constants.
- The upper half of the covering characterization (Conjecture B.5) for
  decomposition certificates in reading (R1), and for separators of
  dimension 2 or more; it is settled in the exact-bag model for trees with
  one-dimensional separators (covering note, Theorem 3), and the lower half
  holds with a `w`-dependent power of `|T|` and fails with a fixed-degree
  polynomial.
- Dense coupling: whether the depth factor of the partial-sum certificate
  (coupling note, Theorem 4.5) is necessary; an adaptive algorithm; a
  general lower bound for lifted certificates.
- Certificates when `kappa_tau < 0` beyond LQ data (lifted calibrations
  give exact certificates on the scalar toys; few outer nodes is
  heuristic), and window exactness for families exact only over the state
  boxes; a transfer theorem for local calibrations; full proofs for
  several switches (Theorems A_k, B_k are sketch level) and asymptotics
  for close switches; state
  constraints; for singular arcs, a global catmix calibration, the discrete
  rate near junctions, and a proof of the exact-flow law
  `f(pi) = K h^3/12`.
- Closing waterno2 (waterno2_06 is at 1.67%; 09–24 were not attempted
  with separator branching) and ann_cumene_tanh (the remaining boxes lie
  along a nearly flat constraint surface).
