# Reviewer 15 — standalone exposition and full proof reconstruction

Round: `stage2-round1`.

Major findings: 0

Minor findings: 0

## Snapshot and coverage

I computed the following SHA-256 hashes and checked them against every file entry in `reviews/stage2-round1/snapshot.json`. All match.

| File | SHA-256 |
| --- | --- |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |

I read all 1,546 lines of stage 2, the process and review protocol, the bibliography, and the coverage inventory. I reread the stage-1 dependencies for the representation model, parity contacts, shared prefix products, covariance/volume inequalities, principal compression, real symmetric shrinking, the finite capacity bound, and the rational-rate preview. I had independently reviewed the whole earlier stage in round 1; this review uses the corrected dependency statements and proofs.

I compared central arguments with the original results for rational nc-rank construction, finite covariance and its rational algorithm, general output norms, nonlinear input rank, unconditional PSD blocks, integer features, and forest differences. Supporting comparisons included the block logdet oracle and determinant certificate notes. I inspected the corresponding claims for all thirteen stage-2 canonical coverage rows and all six substantive supporting rows. The manuscript contains their stated mathematical developments; I did not find a missing stage-2 coverage item.

Primary-source inspection used the cached IQS Theorem 1.5 and Lemma 5.3, GGOW Theorem 2.18, Zhang–Sra Corollary 8 and its triangle proof, Criscitiello–Boumal Appendix I and Proposition I.1, GLS Definition (5) and Theorem (3.1), and DPV Theorem B.5. I also read the root source-audit note, after inspecting the relevant primary interfaces. Its verdict was not treated as proof.

## Assessment

The completed stage provides a coherent standalone mathematical chain, conditional on the explicitly imported classical theorems. I identified no actionable major or minor finding. In particular, the rational nc-rank assertion previewed in stage 1 is now supported by both a rational construction and a quantitative lower proof. I did not find a counterexample, missing material hypothesis, or nontrivial unsupported step in the stage's main claims.

The distinctions that matter to a reader are maintained: rank asymptotics versus finite accuracy; real existence versus rational construction; full input dimension versus common nonlinear input rank versus noncommutative rank; output dimension versus effective quadratic output image; and formulation construction versus MILP solution time. The structural refinements preserve the actual input domain, and the thin-domain example explains why that obligation cannot be omitted. The hardness conclusion is correctly limited to fixed power-sublinear guarantees.

## Reconstruction and checks

1. **Finite covariance and certificates.** The scaling `Sigma/c_n` simultaneously enforces the covariance cap and all unequal energy budgets. The volume proof applies to the compact parity contacts from stage 1, including arbitrary integer ranges. The rotated shared monomial grid gives the factor-eight error margin without an output-count loss. I checked the signs in the Lagrangian certificate, the relative eigenvalue interval from the determinant bound, and the rational residual `tr(PRPR)`. The commuting reduction uses geometric means, so it does not incorrectly assume ordinary convexity of the energy-feasible set.

2. **Rational rank construction.** Rational bases of orthogonal subspaces preserve the required zero blocks even though the bases are not orthonormal. Domain normalization, coefficient heights, and the `0,K,ceil(K/2)` depths yield the claimed coefficient and encoding bounds. The lower proof correctly scales capacity by `D_H^(-2r)` and retains the rational box-volume denominator. IQS explicitly supplies the base-field shrunk subspace and rational intermediate-size control needed by this argument.

3. **Rational finite construction.** The exact penalty repairs every homogeneous budget and the spectral cap by scalar rescaling. Its normalized gradients have trace one. The proof sums an inequality for the stored rational iterates rather than assuming stable tracking of an exact trajectory. The near-active branch error includes the factor `n`; metric and scalar precision requirements remain polynomial because logarithmic spectral bounds are polynomial. Rational Jacobi rotations retain exact orthogonality and avoid any eigenvalue-gap assumption. The final rational covariance sandwich preserves energy feasibility and loses only `O(n)` additional bits.

4. **Output budgets and input quotient.** Grouped PSD energies correctly represent correlated and singular measurement budgets. The correlation-SDP repair returns an exactly feasible correlation matrix and a certified upper value, which serve different purposes in the outer algorithm. GLS Definition (5) supplies the exact distance/objective approximation convention used here. The general-body reduction restricts errors to the nonlinear output image by affine intersection, preserving graph containment even when original errors leave that image. DPV rounding and symmetry remove the potentially real ellipsoid center. The common-kernel quotient subtracts affine terms before projection and keeps an exact linear lift of the normalized zonotope domain.

5. **PSD structure and domain geometry.** The block lower proof uses expected nonnegative Jensen errors, unconditional domination, and the block determinant inequality. The logdet allocation lemma supplies a known interior ball, rational tangent separation, and exact central-ball repair; it does not assume a finite inequality representation of the body. Blockwise quotienting preserves a product domain precisely because the original blocks are disjoint. The diagonal, integer-feature and forest bounds retain the required volume terms, active-rank conditions, and rational row-length dependence.

6. **Hardness.** The Max-Cut symmetry produces the exact zero-count threshold. Independent copies give a parity-incompatible packing; the extra `8z^2` output changes the low case to optimum one and doubles the high-case packing. The replication inequality with fixed `q>1/delta` gives a polynomial reduction. No step assumes that a constructed MILP can subsequently be solved in polynomial time.

## Executed supplementary checks and limits

The following existing scripts were executed independently in this review, all with exit code zero:

- `check_covariance_algorithm.py`: 26 exact rational Jacobi contractions across six matrices; 40 penalty derivative and feasibility-repair checks.
- `check_block_logdet_repair.py`: 24 rational block repairs with exact spectral/body/objective bounds and 100-digit logdet checks.
- `check_nonlinear_input_rank.py`: 21 exact quotient/fiber identities and 21 rational LDL normalization checks.
- `check_precision_hardness.py`: 48 exhaustive Max-Cut gadgets, 5,040 augmented packing pairs, and 260 one-binary scalar-lift extrema.

These finite checks supplement the proof reconstruction. They do not implement or formally verify the full oracle algorithms. I did not compile or inspect the rendered PDF in this review, audit every bibliography entry's metadata, establish publication priority, or review the unwritten later-stage proofs. No manuscript or research files were edited. The absence of findings is limited to this review's coverage and is not a claim of certainty or formal verification.
