# Reviewer 11 — stage2-round1

Primary lens: forest and integer-feature domain geometry, exact volume and minor bounds, thin domains, and benchmark counterexamples.

Major findings: 0

Minor findings: 0

I found no concrete mathematical defect requiring correction in this stage. In particular, the forest and integer-feature bounds retain the actual projected domain, use volume in the correct independent coordinates, and preserve both formulation minima despite affine variation along the fibers. The two domain/benchmark examples establish the limitations claimed for them. This assessment is bounded by the coverage below and is not a guarantee of correctness or publication priority.

## Snapshot and coverage

All six reviewed-file SHA-256 values matched `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I read the complete 1,546-line stage-2 section, the task and lens instructions, process/protocol, bibliography, and coverage inventory, including its thirteen canonical stage-2 rows and six explicit supporting developments. I rechecked the stage-1 dependencies for the representation model, parity closure, shared prefix products, covariance identity and volume inequality, principal compression, symmetric shrinking, finite capacity bound, and rational-rate preview. I had reviewed the complete original stage 1 in the preceding round; I did not repeat a full review of its unrelated smooth-map subsections in this round.

Source comparison was deepest for `results/forest-laplacian-quadratic-precision.md`, `results/independent-integer-feature-quadratic-precision.md`, `results/quadratic-nonlinear-input-rank-precision.md`, `notes/block-psd-domain-correlation-obstruction.md`, `notes/covariance-benchmark-dimension-gap.md`, and `notes/rational-block-logdet-convex-body-oracle.md`. I also inspected the existing second forest and integer-feature audits and independently reconstructed their arguments rather than adopting their verdicts.

For imported interfaces I inspected the cached primary passages in IQS, Theorem 1.5 and Lemma 5.3; GGOW, Theorem 2.18; Dadush–Peikert–Vempala, Theorem B.5 and its ellipsoid convention; Zhang–Sra, Corollary 8 and its proof; and Criscitiello–Boumal, Appendix I and Proposition I.1. These passages support the rational rank witness, field-extension invariance, capacity scaling, ellipsoid rounding, and comparison geometry used here. I did not conduct a comprehensive external novelty search, audit every bibliographic datum, reprove the imported general weak-optimization theorem, implement the complete geodesic construction, compile LaTeX, or inspect the PDF.

## Findings

No numbered major, minor, or question finding is submitted. The checks below explain the principal potential failure points that I examined and found resolved by the draft.

## Primary-lens verification

**Integer features, lines 1305–1378.** For mixed-sign integer rows, the exact coordinate range is `[l_i,l_i+w_i]`. Full row rank ensures positive widths and a full-dimensional image. Fixing the complement of a nonsingular column minor at zero leaves a translated parallelotope within the normalized image; its volume is exactly `abs(det T_I)/product(w_i)`. The translation introduced by `l` has no effect on this calculation. The minor need not maximize volume: any nonzero integer determinant is at least one in absolute value, sufficient for the displayed guarantee. The algorithm need not compute the full zonotope volume.

Expanding `(w_i u_i+l_i)^2` gives exactly the diagonal Hessian entries `a_ji w_i^2`, with the remaining terms affine. Subtracting the original affine output before projecting makes the reduced output depend only on the feature coordinates. Restoring that affine output with the original continuous input variables proves the reverse transfer even when the affine output varies on a fiber. Positive activity implies that the sum of all Hessians is `T^T diag(sum_j a_ji) T`, with positive diagonal weights; its kernel, and the common Hessian kernel, are exactly `ker T`.

The parity-contact lower bound covers the actual volume `V`. The containing-cube grid is used only for the upper construction and is restricted with the original continuous variables. Rational row normalization preserves the represented quadratic after reciprocal-square adjustment of its coefficient. Large primitive row widths are correctly retained in the overhead. Thus the result does not assert a dimension-only linear overhead for arbitrary rational transformations or an algorithm to discover a favorable decomposition.

**Forest volume, lines 1380–1415.** In a connected tree, equal incidence images differ by a constant vector. Subtracting the minimum therefore gives one canonical cube representative for each image. The images of the faces `x_v=0` cover the incidence domain, and each face has volume one because its deleted-column incidence minor has absolute determinant one. If two face images meet, the canonical representative has both corresponding coordinates zero; the intersection has dimension at most `s-2`, so it does not create an overcount of `(s-1)`-volume. Different components form a Cartesian product in the edge coordinates. Isolated vertices have zero image dimension and contribute the factor one. Rescaling all `r` independent edge coordinates gives exactly `2^{-r} product(n_c)`; there is no missing factor involving the Euclidean volume of a subspace of vertex coordinates.

Removing edges absent from all outputs before computing component sizes handles inactivity. The zero-edge case is explicitly affine. The normalized Hessian coefficient is `4a_je`, and the combination of the trace constant, rational allocation loss, and `-log2(V_F)<=r` gives `6r+1`. The statements about paths/stars and the limitation for cyclic systems are accurate.

**Thin domain, lines 1419–1447.** The coordinate map has determinant `delta/(1+delta)`, so the reported area is correct. The second exact output differs from `x_1^2` by a nonnegative amount in `[0,2delta+delta^2]`. Allowing a free continuous correction in that interval therefore retains all exact graph points and gives worst-case error at most `epsilon/4+2delta+delta^2`, which is strictly below `epsilon`. On the full product square the two separate midpoint restrictions force the stated coordinate widths, yielding `p_conv>2L-2`. These are varying instances indexed by `L`; there is no improper assertion about a fixed instance's asymptotic coefficient. The primitive rows `(1,0)` and `(M,1)` explain the growing row-width penalty.

**Benchmark example, lines 217–234 and 1297–1303.** The Frobenius determinant is `n^{-n/2}`, while the trace determinant is `n^{-n}`. The contact-diameter argument uses a ball of radius equal to the diameter, a valid conservative volume estimate; the displayed Gaussian constant follows. The grid depth includes the small-dimensional zero-depth case. Thus the true count is `(n/2) log2(n)+O(n)` at unit tolerance, and its gap from the Frobenius benchmark has order `n log n`. The draft correctly separates this benchmark limitation from an impossibility theorem for every algorithm.

## Whole-stage checks

I reconstructed the finite covariance lower/upper chain, including the factors four in covariance scaling, one eighth in shared-grid output error, and the contact-volume correction for a subdomain. The determinant certificate's distance bound follows because both capped covariances have minimum eigenvalue at least `det P`. Geometric averaging preserves previously imposed commuting sign symmetries, so the indefinite commuting reduction does not rely on unjustified ordinary diagonal truncation.

The rational rank proof now supplies the stage-1 preview's missing construction: polynomial-height rational bases and exact domain equations preserve the zero blocks, and the integral capacity rescales by `D_H^{-2r}`. The endpoint-denominator estimate gives the claimed volume lower bound and polynomial additive loss.

For the numerical argument I checked the Jacobi off-norm contraction, polynomial common-denominator growth, matrix-function perturbation bounds, normalized gradients, positive lower bounds on nonzero energies, and the telescoping recurrence with local rounding. The objective-gap and final determinant-loss constants have adequate slack. The rational final covariance sandwich permits monotonicity of the quadratic energies even for indefinite Hessians, since `H P H` is positive semidefinite for positive semidefinite `P`.

Grouped budgets preserve one common monomial error matrix. The singular-budget convention is explicit, and affine measured combinations have zero error through the shared representation. The correlation-matrix repair is exactly positive semidefinite with unit diagonal and has the stated objective-loss bounds. The effective-output-image restriction keeps every exact graph point. Symmetry removes the possibly real center in the imported rounding theorem, leaving rational ellipsoid data.

The input quotient's LP separator, explicit radii, rational LDL normalization, and interior-cube volume bound are consistent. For block trace allocation, the interior ball and central-ball repair work without positivity of the linear allocation map; positivity and unconditionality enter separately where the formulation proof needs coordinatewise domination. Blockwise input quotients retain a product because the original input blocks are disjoint. The diagonal constants and rational product loss give the stated `5r+1` count.

Finally, zero recognition uses a complement pair of maximum-cut vertices. Replication produces pairwise incompatible midpoint witnesses across independent outputs, and the appended square has exact minimum one. The power-sublinear amplification distinguishes its low case from every valid high-case formulation by the number of declared integer coordinates. It does not assume that the formulation can be efficiently optimized.

## Executed independent checks

I wrote and ran `verification/reviewer11-stage2-geometry.py`. It passed:

- 334 nonempty forests on two through five vertices;
- 2,423 exact incidence-minor calculations, including rank and the sum of absolute maximal minors;
- 61 independently computed forest convex-hull volumes;
- 48 full-rank integer-feature cases with mixed signs, normalized ranges, determinant/volume bounds, and convex-hull volume comparisons where applicable;
- 24 exact rational thin-domain error-budget checks.

The determinant and budget checks use exact arithmetic; convex-hull comparisons use floating point at tolerance `1e-8`. These finite checks supplement the universal proofs. All six snapshot hashes matched. No manuscript, bibliography, original research file, or other review was edited.
