# Repository evidence and manuscript coverage

This map records mathematical coverage and evidence. Paths below are relative
to the repository root. It is not a claim that finite checks or earlier reviews
replace the manuscript proofs. The manuscript covers the complete scoped
encoding, calibration and right-hand-side perturbation package, including
the supporting variants and qualifications below.

| Development | Repository source | Manuscript coverage |
| --- | --- | --- |
| Fixed versus optimized multiplier; value, attainment and minimizer-set distinctions | `research-20260925/penalty-geometry.md`, §§1–3 | §2, including fixed-multiplier ratio formula and strict coefficient increase |
| Balanced finite mixtures, at most m+1 points, threshold ratio, finite-threshold exactness | Same, §2; `research-20260925/penalty-geometry-review.md`, §§1–2 | Proposition 2.1 and Corollary 2.2; sharp support example included |
| Scalar two-sign formula, exact multiplier interval, one-sided nonattainment | Same, §3 and review §3 | Proposition 2.3 and following example |
| Feasible-slice multiplier versus infeasible-slice residual bounds | Same, §4 | Lemma 2.4 |
| One-binary quadratic-chain lower bound, full optimized dual, ordinary encoding, additive accuracy, strict points | `research-20260925/parametric-exploration.md`, main theorem; `research-20260925/parametric-penalty-review.md` | §3, Theorem 3.1 and Corollary 3.2 |
| Symmetric two-binary companion, full fixed-multiplier and dual formulas | Same, symmetric companion sections | §3.1 |
| Fractional-power augmentation with short exponent and constant coefficient | Same, capabilities section | End of §3.1; scope distinguished from a fixed norm |
| Source Example 13: exact supremum but no finite attaining multiplier | `research-20260925/penalty-geometry-review.md`, §4; `research-20260925/publication-penalty-priority-audit.md` | Appendix A, explicitly limited to the December 15, 2025 version |
| General exponential encoding upper bound, sparse KKT certificates, reciprocal residual graph | `research-20260925/penalty-upper-bound.md`, “Statement and encoding model” through “Combining the bounds and accounting for integer variables”; `research-20260925/penalty-upper-bound-review.md`; `research-20260925/penalty-upper-bound-source-review.md` | §4, Theorem 4.1 and its complete proof; effective radius consequence in Lemma 4.2 |
| Fixed nonlinear-quadratic count refinement; affine-face reduction, regularized KKT and quantified limit; common Slater margin and multiplier recovery | Same, fixed-count section; `research-20260925/penalty-fixed-quadratic-count-review.md`; `research-20260925/publication-penalty-fixed-k-audit.md`; `research-20260925/publication-penalty-fixed-k-prior-audit.md` | §5, Theorem 5.1 and Lemma 5.2, with degeneracy and coefficient heights handled explicitly |
| Conservative polynomial-time output for fixed continuous dimension or fixed nonlinear count | Derived here for native quadratics from the uniform upper bounds and monotonicity; the k=0 encoding/output antecedents are Gu–Ahmed–Dey Theorem 11 and Lefebvre–Schmidt Theorem 15; no active-face algorithm required | §5.3, Corollary 5.3 |
| Binary-box exact dual formula, coNP-complete exactness test, polynomial-factor sufficient-calibration hardness | `research-20260925/minimum-penalty-hardness.md`, “Binary-box construction” and “Complexity consequences”; `research-20260925/minimum-penalty-independent-review.md` | §6.1, Proposition 6.1 and Theorems 6.2–6.3; fixed-zero-multiplier threshold and hardness, symmetric estimates, scaling and weak-hardness qualifications follow |
| Unit-data strong hardness with native constraints and fixed gap | Same, “Strong hardness with unit data” | §6.2, full stable-set embedding and exact dual formula |
| Deterministic right-hand-side margin, convex-boundary tube estimate, rational-grid theorem, feasibility conditioning and local stability | `research-20260925/smoothed-penalty.md`, “Setting” through “Feasibility and local stability”; `research-20260925/smoothed-penalty-geometry.md` | §§7.1–7.4, Lemmas 7.1–7.2 and Theorem 7.3, full fiber proof and feasibility qualifications |
| Scalar sharpness, infinite expectation of numerical penalty; centered and endpoint grid variants and dimensional/union losses | Same, later sections; `research-20260925/smoothed-penalty-review.md`; `research-20260925/smoothed-penalty-review-second.md` | §§7.2–7.5: sharp dimension constant, atomic correction, endpoint grid, continuous and finite-grid tails, and expectation distinction |
| Gaussian Euclidean companion, convexity necessity, adjacent-grid almost-sure slice dependence | `research-20260925/smoothed-penalty-novelty.md`, “Statement being assessed” and “Limitations and counterexamples” | §§7.1, 7.5 and 7.6, with explicit lower-dimensional Gaussian extension |
| Infinite optimized threshold at an exceptional rational-grid atom | Developed in the manuscript: a compact convex quadratic slice and one singleton, with linear objectives | §7.5, balanced-mixture proof; no expected encoding guarantee on exceptional grid atoms |

## Primary-source comparisons

`research-20260925/parametric-penalty-literature-review.md`, `research-20260925/penalty-significance-review.md`,
`research-20260925/minimum-penalty-novelty.md`, `research-20260925/smoothed-penalty-novelty.md`, and the
`research-20260925/publication-penalty-*.md` audits establish the repository's bounded literature
comparison. Their review judgments are evidence to inspect, not mathematical
premises. The manuscript cites primary sources directly. The lower-bound
comparison acknowledges Gu–Ahmed–Dey's polyhedral encoding guarantee,
Lefebvre–Schmidt's finite exactness and stated extension question, and the
prior squaring chains of Bienstock–Del Pia–Hildebrand and Beck et al.

The original Bienstock–Del Pia–Hildebrand PDF names **Robert Hildebrand**;
some repository notes incorrectly use Roland. The manuscript bibliography
uses Robert. The inspected versions and local primary text are in
`research-20260925/parametric-sources/`. The current text does not claim that
an unsuccessful novelty search establishes priority.

The source's Example 13 also has a smaller branch-selection error at zero
multiplier: its minimum equals `-1/(4 rho)` only above the branch crossing,
not throughout `rho >= 1/2`. Appendix A retains the complete two-branch
minimum, which resolves this issue without a separate correction claim.

## Related developments with different scopes

A repository-wide text search also identifies exact penalties in
`notes/research-20260922-error-bound-transfer.md` and
`results/cluster-free-branch-and-bound-constrained-minima.md`. These apply
classical local exact-penalty quadratic growth to branch-and-bound counting;
they do not concern ordinary encoding or least augmented-dual calibration.
Similarly, `results/quadratic-l1-output-precision.md`,
`results/quadratic-ellipsoidal-output-precision.md`, and
`results/quadratic-weighted-precision-polynomial-construction.md` concern
relaxation/output precision using other penalty constructions. Pooling
upper-flow-only penalty reductions and rank-one hardness notes concern other
optimization models. They are not omitted results of the present
exact-norm-penalty package and are not asserted as contributions here.
The scouting material in
`research-20260922/scouting/scout_area678_convex_decomp_new.md` motivates the
encoding question; it supplies no additional theorem to transcribe.

## Verification scope

The repository contains prior exact finite checks
`research-20260925/check_parametric_penalty.py`, `research-20260925/parametric-penalty-review-check.py`,
`research-20260925/check_minimum_penalty_hardness.py`, `research-20260925/check_minimum_penalty_review.py`, and
`research-20260925/check_smoothed_penalty_review_second.py`. Their prior results are recorded
in the accompanying notes; they have not been rerun as checks of this new
manuscript. New targeted checks are local to `paper-exact-penalties/verification/`.

`research-20260925/formal/PenaltyEncoding.lean` proves the lower-bound dual
identities from the native constraints in its sequence representation.
`research-20260925/formal/penalty-encoding-coverage.md` and `research-20260925/formal/penalty-lean-review.md`
record its scope. The finite-model restriction/extension correspondence
was checked manually there, not as a separate Lean theorem. Convexity,
Slater margins, encoding, bit counts, literature comparisons, upper bounds,
hardness and smoothing are not thereby formalized. No claim of complete
formal verification is made for this manuscript.

## Encoding upper-bound source checks

The primary-source and scope record in
`paper-exact-penalties/evidence/stage2-sources.md` identifies the final
Basu–Roy weak-sign bounds, the coefficient-height clause of block quantifier
elimination, and the few-quadratic comparison. The local symbolic check
`paper-exact-penalties/verification/check_upper_bound.py` supports the
determinant elimination and a singular limit example.

The older repository notes distinguish the encoding bound from finding an
active affine face. The manuscript adds a consequence that those notes did
not state for native quadratic constraints: a uniform bit bound already yields a polynomial-time algorithm
printing a conservative sufficient coefficient for fixed n or fixed k.
It simply prints a power of two above the uniform bound. This does not
require discovering the face, a small sufficient coefficient, or the minimum
penalty, and applies only on the promised input class. Polynomial output in the linear-constraint case was already established; no general novelty for the printing argument is claimed.

## Calibration and perturbation source checks

`paper-exact-penalties/evidence/stage3-sources.md` records the inspected
QUBO and Ising comparisons, the newer probabilistic-solver result and the
Gaussian boundary lemma, including source versions, locators and hashes.
`paper-exact-penalties/verification/check_calibration_perturbation.py` checks
finite exact mixtures, grid coupling consequences and the sharpness examples.
The manuscript newly makes the exceptional-grid limitation concrete through
a rational convex quadratic example with an infinite optimized threshold at
a grid atom. This example lies outside the upper bounds' refined-Slater
promise and outside the perturbation theorem's good event.
