# Reviewer 09 — stage2-round1

Primary lens: common nonlinear input rank, affine fibers, zonotope separation, rational LDL normalization, and domain-volume losses.

Major findings: 0

Minor findings: 0

## Assessment

I found no concrete mathematical or implementation defect in the reviewed stage. In particular, the common-input quotient theorem preserves the formulation minima even when the affine output varies along a quotient fiber. Its rational normalization gives the claimed domain-volume bound, and that bound enters the covariance comparison with the correct sign. The argument retains an exact linear lift of the actual domain throughout.

This is a bounded independent review, not formal verification, a complete implementation of the proposed algorithms, or a claim of publication priority.

## Snapshot verification and coverage

I read all 1,546 lines of `sections/02-quadratic-finite.tex`, the stage task and lenses, `PROCESS.md`, `reviews/PROTOCOL.md`, the bibliography, and the stage-2 coverage mappings and supporting-development inventory. I reread the stage-1 dependencies for representation conventions, parity contacts, shared prefix products, principal compression, symmetric shrinking, covariance volume, and the finite capacity bound. I had also reviewed the entire preceding stage before its correction pass; this review uses the current dependency statements.

All six recomputed SHA-256 hashes agree with `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

The thirteen canonical stage-2 results and six substantive supporting developments listed in the coverage inventory have identifiable treatment in the stage. I did not audit every auxiliary note in the full multi-stage inventory. I read the original nonlinear-input-rank result and both associated proof audits, consulting the audits only after reconstructing the reduction. I independently compared the principal imported interfaces with cached primary sources, rather than relying on the root source-audit conclusions.

## Full-stage mathematical checks

- **Finite covariance and certificates, lines 22–234:** the covariance cap and factor-four energy rescaling give the stated lower bound. The rotated shared monomial grid gives its factor-eight error margin with the claimed count. The volume correction is valid on compact convex subdomains. The residual certificate uses the correct Lagrangian inequality and relative spectral interval. Geometric sign-flip averaging preserves previously imposed symmetries in the commuting reduction. The dimension-gap example uses a valid, deliberately nonsharp volume bound and still proves the stated order.
- **Rational construction, lines 245–608:** rational bases preserve the zero blocks because orthogonality is between subspaces. The denominator and box-volume estimates yield the displayed uniform lower rate, with capacity scaled by the necessary power `2r`. The Jacobi contraction and common-denominator argument avoid spectral-gap assumptions. I checked the exact penalty, trace-one normalized gradients, bounded metric search region, local rounding recurrence, branch-selection error budget, and the final feasible covariance/grid sandwich. The proof supplies the rational rate previously previewed in stage 1.
- **Output budgets, lines 614–883:** grouped PSD energies preserve the covariance and shared-error arguments, including singular measured directions. The correlation-SDP repair preserves exact PSD feasibility and unit diagonal, while providing both a near-active branch and an upper-value certificate. The effective output image reduction uses an affine intersection in the reverse direction, so it does not presume that errors of an arbitrary original lift already lie in that image. Output rounding loses only a term controlled by the reduced quadratic output dimension.
- **Input quotient, lines 894–975:** checked in additional detail below.
- **PSD structure and domains, lines 1000–1447:** checked the logdet hypograph's explicit interior ball, weak tangent separator, and central-ball feasibility repair; the block first-moment bound and determinant inequality; the blockwise product-domain hypothesis; the diagonal constants and scalar algorithm; integer-feature minor volume; forest tiling volume; and the thin-domain counterexample. No volume factor is silently discarded in the domain reductions.
- **Hardness, lines 1456–1546:** zero dimension is equivalent to the stated Max-Cut threshold on the restricted family. Independent parity packing and the one-bit positive-optimum appendage give the claimed gap. Fixed polynomial replication excludes the stated power-sublinear guarantees. The final paragraph correctly avoids claiming a sharp linear barrier or hardness of solving the constructed MILP from the count argument alone.

## Detailed input-rank check

At lines 905–919, `F_U U` is the orthogonal projector onto the common Hessian row space. Symmetry gives `H_j=U^T G_j U`. An explicit affine remainder is `(a_j+H_j c)^T x+b_j-c^T H_j c/2`; subtracting it before projection leaves a nonlinear function of `z` alone. Thus a reduced witness may use a different original preimage of `z` without changing the error after the affine term is restored. Keeping original `x` as a continuous auxiliary proves that both projection directions preserve linearity/convexity and integer count.

At lines 921–938, the separator LP gives `h^T z >= (1/2) sum v_i+1`, while every point of the zonotope has `h^T y <= (1/2)||U^T h||_1 <= (1/2) sum v_i`. Strict separation permits rescaling the gap to one. The selected column minor provides the explicit positive inner radius; its potentially poor conditioning affects bit length, not the final additive dimension loss.

At lines 940–957, rational LDL factorization and dyadic square comparisons give `A <= R^T R <= 4A`. If `||y|| <= 1/beta_r`, then `R^{-1}y` belongs to the inner ellipsoid, proving the inner ball direction. The outer ellipsoid gives `||Rz|| <= 2`. Consequently the quarter-scale normalized domain lies in the unit cube and contains a ball of radius `1/(4 beta_r)`. Its inscribed cube has side `1/[2r(r+1)]`, including at `r=1`, so the displayed volume loss is correct.

At lines 959–974, the covariance comparison uses the reduced output Hessians and the ellipsoid in their effective output coordinates. The loss is the sum of the dimension-`r` covariance constants, negative log domain volume, and `(r/2) log beta_d`, with `d <= r(r+1)/2`. Every term is `O(r log(r+1))`; there is no ambient-dimension factor in the additive count. Original inputs remain in the exact domain lift. Positive input rank ensures positive nonlinear output-image dimension before rounding.

## Primary-source checks and limits

I checked the following cached primary material:

- IQS Theorem 1.5 and Lemma 5.3: the theorem explicitly returns a shrunk subspace and gives polynomial rational intermediate/final data sizes; the lemma provides field-extension invariance.
- GGOW Theorem 2.18, checked in the previous stage review and used here only after clearing denominators: its integral Kraus-matrix hypothesis and capacity scaling match the proof.
- Zhang–Sra Corollary 8 and its proof: the comparison factor depends on distance to the comparison point. Its unprojected triangle inequality followed by nonexpansive projection supports the manuscript's recurrence even when stored iterates lie in the slightly larger ball.
- Criscitiello–Boumal Proposition I.1: the stated curvature lower bound is `-1/2`, permitting the weaker bound used here.
- GLS1981 Definition (5), Definition (6), and the local theorem context: weak optimization compares with every point of the original body. I visually inspected the cached image of printed p.172 to confirm that the weak separator normal has norm **at least** one. This resolves the potentially consequential OCR ambiguity and matches the manuscript's normalization.
- DPV Theorem B.5: its factor is `(d+1)sqrt(d)`, it returns a rational ellipsoid matrix with the stated small-volume alternative, and it allows the center to be real. Symmetry removes the center from both inclusions by convex averaging. The chosen rational volume threshold rules out the small-volume branch.

I did not independently audit all publication metadata or retrieve every adjacent reference (for example Cao and Del Pia). The relevant spectral, covariance, and Grothendieck arguments are proved in the manuscript; no new priority conclusion is based on those unchecked metadata. I did not compile LaTeX or inspect the combined PDF. I did not implement the full geodesic optimizer or classical oracle rounding algorithm.

## Executed checks

1. Ran the existing exact SymPy checker `code/quadratic_rank/check_nonlinear_input_rank.py`: **21 quotient/affine-fiber cases and 21 LDL sandwich/inverse-map cases passed**.
2. Independently wrote and ran an inline SciPy LP checker for the zonotope oracle. It tested **21 cases** with ambient dimensions 2–7 and reduced dimensions 1–4, using full-row-rank integer generators with overlapping columns. Each case tested a feasible membership query, an explicitly exterior query, feasibility of the proposed separator LP, its unit separation gap, and validity against every cube vertex image. All passed to numerical tolerance `1e-8`. This checks the displayed LP construction; the polynomial-bit claim relies on the exact rational LP argument, not floating-point output.

## Findings

No concrete MAJOR, MINOR, or QUESTION finding is submitted. The checks and limits above specify the extent of that conclusion.

No manuscript, bibliography, or original research files were edited.
