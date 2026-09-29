# Second September 28 continuation: results and closing record

Date: 2026-09-29. On 2026-09-29 the user asked to finish the current ideas
and their extensions without starting new ones. This record collects the
results, their verification and their limits. Nothing in this continuation
is committed to git.

"Reviewed" means checked by a research agent that did not write the
material, not journal peer review. Most literature checks ran after the
shared web-search quota was exhausted, so they used arXiv pages, author
PDFs and the local library. An unsuccessful search does not establish
novelty; each note states what was and was not examined.

## Main contribution

A complexity theory of branch-and-bound (B&B) with nonlinear relaxations,
presented in the [program synthesis](bb-complexity/SYNTHESIS.md). Its
strongest parts, in order of expected significance:

1. **Random sparse regression.** For B&B with the perspective (Boolean)
   relaxation of L0-constrained ridge regression with Gaussian design:
   a sharp root-exactness threshold `n ≈ 2k log p`, and a sharp threshold
   `n ≈ 2k log(p/sqrt n)` for condition C1, above which every
   variable-branching tree is linear-size (with the incumbent available or
   best-bound search). For `k = p^gamma` the windows are `alpha = 2` and
   `alpha = 2 - gamma`, so linear trees hold strictly below root exactness.
   Pure noise and low total SNR force conflict cliques of size
   `C(p,k)^{c'}` (asymptotic only). Every relaxation between the perspective
   relaxation and `r`-wise lifted hulls in the `(z, beta, beta beta')` lift
   (optimal-perspective SDP, rank-one, free-sign 2×2 hulls) has the same
   sharp constants. [Note](bb-complexity/sparse-regression/phase-transition.md),
   [stronger relaxations](bb-complexity/sparse-regression/stronger-relaxations/thresholds.md).
2. **A published theorem is false as stated.** Theorem 2 of
   Pilanci–Wainwright–El Ghaoui (Math. Program. 151:63–87, 2015) claims
   exactness of the Boolean relaxation with probability tending to 1 under
   per-entry Gaussian noise; by the paper's own Corollary 2 the probability
   tends to a limit below 1 (0.123 in an explicit case). The proof hides a
   normalization mismatch between two appendix lemmas. Pilanci's thesis
   repeats the statement; later papers cite it as valid; no erratum was
   found. Two agents confirmed the counterexample with separate code
   ([verification](reviews/pwe-verification.md)).
3. **Spatial B&B node complexity.** For relaxations with second-order gaps,
   rigorous lower bounds valid for every adaptive tree, branching rule, node
   order and same-relaxation tightening; the `eps`-exponent is half the
   box-counting dimension of the optimal set; certificate size and bisection
   lie within `C log(1/eps)` of a multi-scale covering profile.
   Face-exact (McCormick) relaxations follow a different, transversality-based
   law; objective-cutoff propagation escapes the bounds only through one-sided
   expression graphs. SCIP 10.0.2 node counts follow the predicted exponents
   once its search matches the model.
   [Constrained](bb-complexity/spatial-constrained/instance-dependent-node-complexity.md),
   [face-exact](bb-complexity/spatial-face-exact/face-exact-node-complexity.md),
   [cutoff propagation](bb-complexity/cutoff-propagation/cutoff-propagation.md),
   [SCIP validation](bb-complexity/solver-validation/scip-node-exponents.md).
4. **Branching points.** In 1D, splitting at the relaxation minimizer is
   4-competitive (Lean-verified); every node-local rule loses at least 5/3,
   and in `n` dimensions at least `(2G(n)+1)/3`, which grows exponentially;
   SCIP's default clamp provably loses `log(1/eps)` on an explicit instance;
   a recentring clamp is exactly split-optimal among safe rules. On
   MINLPLib none of this changes performance beyond seed noise, and removing
   the clamp is harmful, because LP values on variable bounds (outside the
   models) make the clamp protective.
   [1D](bb-complexity/branching-competitiveness/competitive-branching.md),
   [n-dimensional](bb-complexity/branching-competitiveness/n-dimensional.md),
   [separable](bb-complexity/branching-competitiveness/separable-omega.md),
   [safe rules](bb-complexity/robust-branching-points/robust-branching.md),
   [MINLPLib study](bb-complexity/minlplib-branching/branching-point-study.md),
   [Lean topic 33](../formal/topics/33-competitive-branching/README.md).
5. **Binary least squares (MIMO detection).** The box relaxation is exact
   at the planted point with probability exactly `2^{-N}` at every SNR;
   linear trees need SNR linear in `N`; in between, box-relaxation
   certificates need `exp(Θ((N/rho) log rho))` leaves, so at `rho = c log N`
   certification is superpolynomial while search is polynomial (square
   systems). The SDP relaxation, and for tall systems even a diagonal shift,
   remove the gap. [Note](bb-complexity/binary-least-squares/certification-thresholds.md).
6. **Integer branching.** The class number bounds every convex-piece tree
   and is exact for arbitrary convex pieces; random CVP forces
   `2^{Ω(n)}` leaves for every branching scheme with the continuous
   relaxation. [Note](bb-complexity/integer-core/relaxation-intrinsic-bounds.md).

## Secondary results

- [Split-inequality separation](side-results/split-separation-np-complete.md)
  for integer QP is strongly NP-complete, even for 0/1 splits and at points
  satisfying every cut family used by de Meijer et al.; additive
  approximation below `1/(N+7)` is strongly NP-hard; FPT in rank. This
  settles a question posed by Burer–Letchford and called a conjecture by
  Buchheim–Traversi. The lattice core is standard.
- [A priori gap bounds for graphs of convex sets](gcs/a-priori-gap-bounds.md):
  Jensen-defect rounding bounds for the relaxation with the vertex-local
  hull on acyclic graphs; `sec theta` for norm lengths; an exact
  enclosing-ball constant for squared lengths; negative results for
  overlapping covers; `1 + theta^2/poly` hardness.
- [Best intersection cuts](sfree/optimal-intersection-cuts.md) from maximal
  quadratic-free sets equal a computable corner bound; the transformation
  family is not exact for bilinear constraints (certified counterexample);
  SCIP's set can be arbitrarily weaker than another set of its own family.

## Verification

Every note links its reviews. Each substantive correction was rechecked by
a fresh agent, and the final round of revisions was covered by two closing
audits ([A](reviews/closing-audit-a.md), [B](reviews/closing-audit-b.md))
and a final recheck of the stronger-relaxations note. Reviews found and
removed several errors: an invalid proof (replaced), several false side
claims and conjectures (withdrawn), wrong solver-default attributions, a
misreported computational result, and overstated novelty. Remaining
minor wording fixes applied after the last check are recorded in each
note's revision section.

Targeted commands run by the root (others are recorded in each note):

```
python3 -B research-20260928b/side-results/check_split_separation.py   # ALL CHECKS PASSED
cd formal && lake env lean topics/33-competitive-branching/verification/AuditCompetitiveBranching.lean
# PASS: audited declarations; axioms [propext, Classical.choice, Quot.sound]
```

No project-wide checks were run and CI was not inspected.

## Limits

- The sparse-regression and MIMO theorems are asymptotic; their regime
  assumptions exclude every experiment in the notes, and several constants
  (for example the MIMO class-number constant, about `1.4e-4`) make the
  lower bounds vacuous at practical sizes.
- The spatial theory covers specified relaxation classes. Real solvers
  combine relaxations, propagation and plunging; the SCIP study shows the
  exponents only after the search is aligned with the model.
- The branching-point theory does not transfer to practice as a rule
  change; the MINLPLib studies are the decisive evidence.
- Novelty assessments are provisional, and several classical sources
  were available only through abstracts or secondary citations.

## Open questions left by this continuation

- Whether the most-central-coordinate branching rule is `C_n`-competitive
  (any constant must be exponential in `n`).
- A characterization of face-exact node complexity (row-slice bounds).
- Whether split-tree size is polynomial in the class number for convex
  quadratic objectives.
- The asymptotic constant of sparse-regression relaxations that lift
  `z_j beta_m`, and finite-size versions of the thresholds.
- The square-system C1 threshold without the cited Hu–Lu input.

## Process notes

Thirteen scouts selected the direction ([scouting](scouting/)). Work was
interrupted once by an API session limit; interrupted agents were resumed
from their transcripts. The scout reports contain further unreviewed
first-pass results that were not developed; they should not be cited.
