# Stage 2 review — reviewer 03

Primary lens: shared residual formulations, exact graph containment, domain identities, and rational encoding/size.

Major findings: 0
Minor findings: 0

I found no concrete major or minor defect in the reviewed stage. The shared residual construction preserves exact graph points and the actual input domain; its rational implementation does not require irrational coordinate equations or additional integer coordinates. The other stage-2 proofs withstand the checks below. This assessment is a bounded independent review, not a guarantee of correctness or publication priority.

## Snapshot verification

All six file hashes were recomputed and matched `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

## Coverage and verification limits

I read all 1,546 lines of `sections/02-quadratic-finite.tex`, the process/protocol/task instructions, bibliography, and coverage mapping. I checked the stage-1 parity, covariance, principal-compression, symmetric-shrinking, shared-prefix, binary-product, finite-capacity, and rational-rate dependencies. The thirteen canonical stage-2 developments and six substantive supporting developments in the coverage mapping have corresponding statements/proofs in this stage.

I compared selected original proof sections in the weighted covariance, rational weighted construction, grouped ellipsoidal error, nonlinear input quotient, and integer-feature result files. I read the earlier rational-algorithm audit and root source audit after reconstructing the manuscript arguments; their pass labels were not treated as proof. Primary-source checks used the cached IQS, GGOW, Zhang–Sra, Criscitiello–Boumal, GLS1981, and Dadush–Peikert–Vempala texts. I also visually inspected the primary GLS p.172 image to resolve the weak-separation normal convention.

This was not a complete re-audit of every original research file, every supporting note, all bibliography metadata, or novelty. I did not compile the manuscript or inspect its rendered pages. I checked the imported algorithm interfaces and their applicability, rather than reproving the classical algorithms. The executable check below verifies a finite family of exact formulations; it does not implement the full geodesic or classical oracle algorithms.

## Findings

No numbered defect findings. No unsupported omission is being assigned to the unwritten stages 3–4. In particular, the stage-1 rational nc-rank preview now has its required proof in `thm:rational-ncrank`.

## Mathematical checks

1. **Finite covariance law and actual shared grid (lines 22–106).** The contact scaling uses both `Sigma <= (n/4) I` and energy scaling by the square of the covariance scale, so `c_n=max(4,n/4)` is sufficient. Rotated widths are exact rational sums when the rotation is rational. The original cube constraints and coordinate equations remain in the lift. For a square, the same prefix identity and square triangle apply; for an off-diagonal monomial one shared value is used symmetrically. The output coefficient is one half of the full symmetric Hessian sum, giving the stated `1/8` error factor. Each bit participates in only `O(n)` exact binary products. Empty prefixes and interval endpoints do not require a special binary or an excluded endpoint.

2. **Finite certificates, commuting reduction, and dimension gap (lines 108–234).** I checked the geodesic exponential energy expansion, the residual-certificate signs and determinant-to-eigenvalue bound, and the geometric-mean sign symmetrization. Successive sign symmetries are preserved because the flips commute. The water-filling formula handles zero coefficients and saturated caps. The covariance-gap example gives the claimed order; its nonsharp volume bound is sufficient.

3. **Uniform rational nc-rank construction (lines 245–343).** Nonorthonormal rational bases preserve the required zero blocks because the subspaces themselves are orthogonal. Exact interval normalization retains the original box. Nonzero monomials have the stated residual precision, and the binary count is bounded by `r k/2 + r b/2 + n/2`. IQS Theorem 1.5 explicitly supplies polynomial rational intermediate/final data and a maximal-deficiency base-field shrunk subspace; Lemma 5.3 supplies field-extension invariance. GGOW Theorem 2.18 gives the integral lower bound `r^(-2r)`. Rescaling by the Hessian denominator contributes `D_H^(-2r)`, yielding the manuscript's finite lower bound and polynomial input-height loss.

4. **Rational spectral and geodesic implementation (lines 353–608).** The maximum-pivot Jacobi contraction and additive common-denominator growth are valid. Exact rational orthogonality prevents coordinate-reconstruction drift. The logarithm, square-root, inverse-square-root, and exponential perturbation bounds used here have the stated matrix arguments; no general scalar-to-operator Lipschitz inference is needed. I checked the exact penalty, normalized trace-one gradients, polynomial metric radius, stored-iterate recurrence, near-active Rayleigh branch, numerical-error constants, exact rational scaling repair, and final `P_hat/8 <= P_tilde <= P_hat/2` sandwich. PSD-order monotonicity of the indefinite quadratic energies follows from `H P H >= 0`. The exact diagonal scales and squared rational depth comparisons then give rational formulation coefficients.

5. **Grouped, total-absolute, and oracle errors (lines 614–883).** Sharing the monomials gives one symmetric residual matrix `Z`, so the correlated output estimate follows jointly, rather than by independent output bounds that might lose a factor in the output dimension. Singular measured combinations that have zero Hessian are represented exactly by the output equations. The correlation SDP normalization, exactly feasible rational repair, and upper/lower objective interval have the advertised errors. GLS's primary Definition (5) gives approximation against the original body, which is the guarantee used here. The effective nonlinear output image equality is valid in both directions, including original relaxations with off-image errors. DPV Theorem B.5 supplies the stated rounding factor and rational ellipsoid matrix; symmetry removes the possibly real center from both inclusions. The final formulation uses the shared grid, not an attempted finite exact description of the oracle body.

6. **Input quotients and positive structure (lines 894–1415).** The common-kernel quotient preserves both minima even when the affine output varies along a fiber. The zonotope separator and exact continuous domain lift are valid. Rational LDL normalization gives the stated inner ball and volume lower bound. The logdet allocation lemma has an explicit interior ball, valid tangent separators, and an exact central-ball repair. The block lower proof uses positivity and unconditional domination correctly. Blockwise quotienting preserves a product domain because the original input blocks are disjoint. The diagonal overhead, integer-feature minor bound, and forest face-tiling volume formula check out, including zero-rank/absent-feature cases.

7. **Domain obstruction and hardness (lines 1419–1546).** The thin-domain upper construction contains the exact second output by an appropriate continuous correction; its error budget is below the tolerance. The full product-domain lower packing demonstrates the claimed gap. The Max-Cut zero-count equivalence, independent replicated parity packing, one-bit positive-optimum appendage, unit-tolerance normalization, and polynomial amplification establish the stated fixed power-sublinear exclusions. The final caveat correctly avoids claiming that every sublinear additive guarantee is excluded.

## Executed independent check

Created and ran `verification/reviewer03-stage2-shared-grid.py` with exact SymPy rationals. It uses a nontrivial rational orthogonal rotation, unequal depths `[3,4,5]`, indefinite Hessians, nonzero affine terms, and a linearly dependent nonlinear output. At 20 original-domain points, including all eight cube corners, it enumerates all 64 residual-envelope extreme choices. All 1,280 cases passed:

- exact original/rotated coordinate reconstruction;
- prefix reconstruction, residual bounds, and exact binary-product inequalities;
- every individual monomial error bound;
- all scalar energy-based error bounds;
- a coupled positive semidefinite output budget;
- exact cancellation in the dependent measured output;
- exact graph witnesses obtained by exact monomial values.

The script also verifies the stated grid count bound. These checks supplement the universal algebraic proofs. No manuscript, bibliography, or original research file was edited.
