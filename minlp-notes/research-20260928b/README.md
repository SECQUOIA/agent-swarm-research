# September 28 second continuation

The user renewed the broad research instruction after the
[first September 28 continuation](../research-20260928/README.md) closed.
This continuation treats earlier repository work as a resource, not a
constraint on direction. Nothing here is committed to git. The
[closing record](closing-research-results.md) is the final summary.

Reviews are research-agent reviews by agents that did not write the
material, not journal peer review. An unsuccessful literature search does
not establish novelty. Every note links its reviews and lists the targeted
commands actually run; no project-wide checks were run and CI was not
inspected.

## Main results

The [program synthesis](bb-complexity/SYNTHESIS.md) is the entry point. In
brief:

- **Branch-and-bound complexity with nonlinear relaxations.** For spatial
  B&B with second-order relaxation gaps, the minimum certificate size is,
  up to `C log(1/eps)`, a multi-scale covering number of the near-optimal
  set, and the `eps`-exponent is half the box-counting dimension of the
  optimal set, for every adaptive tree and branching rule. McCormick-type
  relaxations and objective-cutoff propagation change this in precisely
  characterized ways. SCIP 10 node counts follow the predicted exponents
  once its search matches the model.
- **Branching points.** In 1D, splitting at the relaxation minimizer is
  4-competitive (formalized in Lean); every node-local rule loses a factor
  exponential in the dimension on separable instances; SCIP's default clamp
  provably loses `log(1/eps)` on an explicit instance, and a recentring
  clamp is exactly split-optimal among safe rules. Two MINLPLib studies show
  that none of this changes practical performance beyond seed noise, and
  that the clamp is protective because LP values sit on variable bounds,
  which the models exclude.
- **Random sparse regression.** Sharp thresholds for root exactness of the
  perspective relaxation (`n ≈ 2k log p`) and for linear-size B&B trees
  (`n ≈ 2k log(p/sqrt n)`), strictly below root exactness; conflict cliques
  of size `C(p,k)^{c'}` in pure noise. Rank-one, 2×2-hull and
  optimal-perspective SDP relaxations have the same sharp constants. Along
  the way, Theorem 2 of Pilanci–Wainwright–El Ghaoui (Math. Program. 2015)
  was found to be false as stated, and the finding was independently
  verified.
- **Binary least squares (MIMO).** The box relaxation is exact with
  probability exactly `2^{-N}` at every SNR; at logarithmic SNR, where
  search is polynomial, box-relaxation B&B certificates need
  superpolynomially many leaves; the SDP relaxation removes the gap for
  tall systems.
- **Integer branching.** The class number `kappa` bounds every convex-piece
  tree and is exact for arbitrary convex pieces; random CVP needs
  `2^{Ω(n)}` leaves for any branching scheme with the continuous
  relaxation.
- **Secondary results.** First a priori integrality-gap bounds for
  [graphs of convex sets](gcs/a-priori-gap-bounds.md) (robot motion
  planning); [split-inequality separation](side-results/split-separation-np-complete.md)
  for integer QP is strongly NP-complete, settling a question posed by
  Burer–Letchford; [best intersection cuts](sfree/optimal-intersection-cuts.md)
  from maximal quadratic-free sets equal a computable corner bound, and the
  transformation family is not exact for bilinear constraints (exact
  certified counterexample).

## Status

The continuation is closed at the user's request to finish current ideas
without starting new ones. The [closing record](closing-research-results.md)
collects the results, verification and limits.

| Note | Review status |
| --- | --- |
| [Constrained spatial B&B](bb-complexity/spatial-constrained/instance-dependent-node-complexity.md) | [Review](reviews/spatial-constrained-review.md), [recheck](reviews/spatial-constrained-recheck.md); earlier [unconstrained review](reviews/spatial-bb-review.md) |
| [Face-exact (McCormick) relaxations](bb-complexity/spatial-face-exact/face-exact-node-complexity.md) | [Review](reviews/face-exact-review.md), [recheck](reviews/face-exact-recheck.md), [closing audit B](reviews/closing-audit-b.md); two conjectures refuted and withdrawn |
| [Objective-cutoff propagation](bb-complexity/cutoff-propagation/cutoff-propagation.md) | [Review](reviews/cutoff-review.md), [recheck](reviews/cutoff-recheck.md), [closing audit A](reviews/closing-audit-a.md) |
| [Competitive branching, 1D](bb-complexity/branching-competitiveness/competitive-branching.md) and [n-dimensional](bb-complexity/branching-competitiveness/n-dimensional.md) | [Review](reviews/competitive-review.md), [recheck](reviews/competitive-recheck.md); Theorem 1 [formalized in Lean](../formal/topics/33-competitive-branching/README.md) with a [statement review](../formal/topics/33-competitive-branching/reviews/statement-review.md) |
| [Separable competitiveness](bb-complexity/branching-competitiveness/separable-omega.md) | [Review](reviews/separable-omega-review.md), [closing audit A](reviews/closing-audit-a.md) |
| [Safe branching points](bb-complexity/robust-branching-points/robust-branching.md) | [Review](reviews/robust-branching-review.md), [closing audit A](reviews/closing-audit-a.md) |
| [Integer branching](bb-complexity/integer-core/relaxation-intrinsic-bounds.md) | [Review](reviews/integer-core-review.md), [recheck](reviews/integer-core-recheck.md); earlier [scout review](reviews/bb-conflict-review.md) |
| [Sparse regression](bb-complexity/sparse-regression/phase-transition.md) | [Easy side](reviews/sparse-easy-review.md), [hard side](reviews/sparse-hard-review.md), [PWE verification](reviews/pwe-verification.md), [recheck](reviews/sparse-recheck.md), [closing audit B](reviews/closing-audit-b.md) |
| [Stronger relaxations](bb-complexity/sparse-regression/stronger-relaxations/thresholds.md) | [Review](reviews/stronger-relaxations-review.md), [recheck](reviews/stronger-relaxations-recheck.md) |
| [Binary least squares (MIMO)](bb-complexity/binary-least-squares/certification-thresholds.md) | [Easy side](reviews/mimo-easy-review.md), [hard side](reviews/mimo-hard-review.md), [recheck](reviews/mimo-recheck.md), [closing audit B](reviews/closing-audit-b.md) |
| [SCIP node exponents](bb-complexity/solver-validation/scip-node-exponents.md) | Empirical; not independently reproduced |
| [MINLPLib branching-point study](bb-complexity/minlplib-branching/branching-point-study.md) | Empirical; default and LP-point node counts reproduced exactly by the [safe-branching study](bb-complexity/robust-branching-points/robust-branching.md) |
| [GCS gap bounds](gcs/a-priori-gap-bounds.md) | [Review](reviews/gcs-review.md), [recheck](reviews/gcs-recheck.md) |
| [Split separation](side-results/split-separation-np-complete.md) | [Review](reviews/split-separation-review.md), [final review](reviews/split-final-review.md), [recheck](reviews/split-cor5-recheck.md) |
| [Optimal intersection cuts](sfree/optimal-intersection-cuts.md) | [Review](reviews/sfree-review.md), [recheck](reviews/sfree-recheck.md) |

## Direction selection

Thirteen scouts surveyed areas the repository had not developed, checked
2024–2026 literature, and proposed open questions. Their reports are in
[scouting](scouting/); the [brief](scouting/SCOUT-BRIEF.md) lists the
required content. Scores (significance × feasibility × originality, 1–10):

| Area | Score | Main finding |
| --- | --- | --- |
| [B&B tree size, convex MINLP](scouting/bb-tree-size-convex.md) | 7 | Midpoint-conflict lower bounds; random CVP; sparse-regression transition |
| [Spatial B&B theory](scouting/spatial-bb-theory.md) | 6 | Certificate-integral lower bound for adaptive trees |
| [Intersection cuts](scouting/s-free-intersection-cuts.md) | 6 | Choosing the best maximal quadratic-free set |
| [ML surrogates](scouting/ml-surrogate-minlp.md) | 5 | Layer-hull extension complexity and B&B barriers |
| [Graphs of convex sets](scouting/graphs-of-convex-sets.md) | 5 | A priori gap bounds with the vertex-local hull |
| [Open-problem sweep](scouting/open-problem-sweep.md) | 5 | Split-inequality separation appears NP-hard |
| [Proximity](scouting/proximity-convex-minlp.md), [MICP representability](scouting/micp-representability.md), [decomposition gaps](scouting/decomposition-duality-gaps.md), [discrete convexity](scouting/discrete-convexity-minlp.md), [fixed dimension](scouting/fixed-dimension-frontier.md) | 4 | Clean but narrow or indirect |
| [MI centerpoints](scouting/mi-centerpoints.md), [data-driven configuration](scouting/data-driven-minlp-config.md) | 3 | Low solver impact |

Recent sources closed two classical targets: the characterization of
maximal quadratic-free sets ([arXiv:2605.30602](https://arxiv.org/abs/2605.30602))
and exact MIQP in fixed dimension (Ari–Hildebrand,
[arXiv:2609.18266](https://arxiv.org/abs/2609.18266); W[1]-hardness by
Herrmann, [arXiv:2608.17818](https://arxiv.org/abs/2608.17818)).

The scout reports contain further first-pass results that were not
developed (for example a one-integer-variable centerpoint theorem, a
Hessian criterion for discrete midpoint convexity, and a negative answer to
a "local Shapley–Folkman" question). They are unreviewed and should not be
cited as results.
