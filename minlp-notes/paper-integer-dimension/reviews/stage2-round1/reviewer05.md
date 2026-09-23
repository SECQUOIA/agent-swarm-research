# Stage 2, round 1 — reviewer 05

Primary lens: exact geodesic penalty, gradients, projected inexact recurrence, and feasibility repair.

Major findings: 0

Minor findings: 1

## Assessment

I found no major mathematical defect in this stage. The central numerical argument is coherent: the penalty equals the negative log determinant of a feasible scalar repair; its branch gradients have the claimed uniform norm; approximate steps enter a local squared-distance recurrence; and the final rational repairs lose only a controlled determinant factor. The surrounding covariance, output-body, input-quotient, positive-block, feature and hardness arguments are consistent with this construction. This is a bounded review judgment, not a claim of certainty or a replacement for the other independent reviews.

## Coverage and snapshot

I read all 1,546 lines of `sections/02-quadratic-finite.tex`, its relevant stage-1 definitions and dependencies (parity, binary products, square law, covariance, principal compression, symmetric shrinking and finite nc-rank bound), the bibliography, coverage inventory, process file and review protocol. I had previously reviewed the entire stage-1 draft; for this assignment I reread the dependencies in the corrected snapshot rather than relying only on the earlier report. I checked the stage-2 coverage mappings for all thirteen canonical results and six substantive supporting developments.

All six SHA-256 hashes matched `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I compared the original weighted polynomial construction proof, rational Jacobi/matrix-function note and covariance-certificate note. I inspected the root source audit only after independently reading the important primary-source passages and reconstructing the manuscript's arguments. I did not independently implement the complete outer algorithm or the classical oracle algorithms, reread every original stage-2 result file in full, compile/render the manuscript, or perform an exhaustive bibliography/priority search. The remaining stages are outside this report's scope.

## Finding

1. **MINOR — ambiguous referent in the interior-ball estimate.** Location: `sections/02-quadratic-finite.tex:1045–1048`, proof of `lem:block-logdet-oracle`. After bounding the independent-coordinate gradient of `g` by `8N/delta`, the text says, “Its variation is at most 1/4.” The established bound is on the objective's variation, namely `|g(P)-g(P_0)| <= (8N/delta) sigma <= 1/4`; it is not a bound on variation of the gradient mentioned immediately before it. For example, in the scalar case `N=1`, `delta=1/4`, `P_0=1/8`, and `sigma=1/128`, changing `P` to `P_0-sigma` changes the gradient `1/P` by `8/15 > 1/4`, although the objective changes by only `log(16/15)`. These constants fit the lemma with the zero linear map and an inner radius one. Repair by writing “Consequently, the value of g changes by at most 1/4 from its value at P_0.” This is an expository ambiguity; the objective bound needed by the proof is valid and no theorem changes.

## Reconstruction of the primary argument

- **Penalty and gradients, lines 457–478.** Quadratic energy scales by the square of a positive scalar, while the cap scales linearly. Thus dividing by `exp(h)` simultaneously repairs every constraint, and the determinant identity has coefficient exactly `n`. Along a geodesic, the energy is a positive exponential sum. Differentiating its half-log gives `M^2/tr(M^2)` even for indefinite Hessians. This matrix is positive semidefinite, has trace one, and has Frobenius norm at most one. The Rayleigh branch has the same properties. The resulting Lipschitz and subgradient bounds follow without a Hessian definiteness or eigenvalue-gap assumption.
- **Radius and projection, lines 480–497.** A dyadic feasible multiple of the identity supplies an optimizer with all eigenvalues at most one and determinant at least `delta^n`. The sum of the negative logarithmic eigenvalues bounds its distance to the identity. The radial projection formula follows from the reverse triangle inequality and the identity-centered geodesic, and its denominator is bounded away from zero.
- **Stored-iterate recurrence, lines 499–556.** The sign in `eq:inexact-subgradient` matches descent. The curvature factor depends on the distance from the current iterate to the comparison point, bounded by `D`, and not on the full length of a hypothetical exact trajectory. Although the stored point can lie outside the projection ball, the ambient comparison inequality in the proof of Zhang–Sra Corollary 8 followed by nonexpansiveness still applies: only the comparison point must be fixed by projection. The local rounding term is bounded by `(2D xi+xi^2)/(2 eta)`. With the stated choices the mean gap is at most `7/64`, and objective selection adds at most `1/32`, comfortably below the claimed half-unit gap. The near-active branch and gradient errors satisfy `3n tau+D nu < 1/32`.
- **Precision and repairs, lines 534–607.** The radius gives spectral lower bounds of inverse-exponential-polynomial size. The nonzero rational Hessian energy lower bound prevents division by an uncontrolled denominator. Fresh symmetric dyadic rounding controls stored lengths. Rounding the scalar feasibility factor upwards adds at most `1/4` to the negative log determinant. The rational spectral residual then gives the displayed `P_hat/8 <= P_tilde <= P_hat/2` sandwich. Energy monotonicity in PSD order is valid even for indefinite `H`, since the directional derivative is `2 tr(HPH A)` and `HPH` is PSD. The final determinant and bit-count losses follow.

## Other mathematical checks

The finite covariance lower bound uses the correct factor four from quadratic midpoint error and the variance cap `nI/4`; the shared residual grid retains graph points and gives the stated factor-eight output margin. The residual optimality certificate correctly bounds relative eigenvalues using `det P`. Geometric sign symmetrization, unlike ordinary diagonal deletion for arbitrary indefinite commuting Hessians, preserves all energy constraints and the determinant.

The rational nc-rank proof now discharges the stage-1 preview: the base-field shrunk-space output has polynomial height, rational orthogonal subspaces need not have orthonormal bases, capacity scales by `D_H^(-2r)`, and the rational box volume contributes the stated endpoint-denominator bound.

Grouped errors use a single shared residual matrix and a sum of squares after PSD factorization; the algorithm itself can retain rational double sums. The correlation SDP repair has exact PSD feasibility and a certified upper value, and its normalized optimum lies between one and `m`. Both output-image and common-input-kernel reductions preserve graph containment even when original errors leave the nonlinear image or affine outputs vary along fibers. The input normalization retains a sufficient dimension-only domain volume. Positive block reductions use independent original domains, while the thin-domain counterexample correctly prevents an unrestricted transfer. The diagonal, integer-feature, and forest constants follow from trace covariances and the specified volumes. The Max-Cut replication argument establishes the stated fixed-power sublinear hardness and does not claim a sharp linear barrier.

## Primary-source checks and executed checks

I checked the cached primary texts for Zhang–Sra Corollary 8 and its proof, Criscitiello–Boumal Appendix I and Proposition I.1, IQS Theorem 1.5 and Lemma 5.3, GLS Definition (5), Definition (6) and Theorem (3.1), and DPV Theorem B.5. Their relevant hypotheses match the applications. I visually inspected the cached image of GLS printed p.172: the weak-optimization guarantee compares against the original body, and the weak-separation convention indeed requires the normal norm to be at least one. The DPV theorem permits a real center; symmetry removes that center from both inclusions, leaving the rational ellipsoid matrix. The GGOW integral capacity theorem was also checked in the earlier stage-1 review and is now applied to integral compressed matrices.

Executed existing checks:

- `code/quadratic_rank/check_covariance_algorithm.py`: passed 26 exact rational Jacobi contractions across six matrices and 40 penalty derivative/feasibility-repair checks.
- `code/quadratic_rank/check_block_logdet_repair.py`: passed 24 rational block-logdet repairs, with exact spectral/body bounds and 100-digit log-determinant evaluations.

These are finite supporting checks; they do not prove the universal convergence or oracle-complexity statements. No manuscript or research-source files were edited.
