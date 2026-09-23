# Stage 2, round 1 — reviewer 04

Primary lens: rational nc-rank construction, rational subspace heights, capacity constants, and uniform encoding bounds.

Major findings: 0

Minor findings: 1

## Snapshot and coverage

All six actual SHA-256 values match `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I read all 1,546 lines of the stage-2 section, its bibliography, the process/protocol, and the coverage inventory. I had reviewed the entire stage-1 draft in the previous assignment and reread the relevant corrected stage-1 dependencies: parity contacts, shared products, principal compression, real shrinking, covariance, the finite capacity lower bound, and the rational-rate preview. I checked the stage-2 coverage locations for all thirteen canonical developments and the six explicitly substantive supporting developments, including the certificate, commuting reduction, benchmark gap, thin-domain obstruction, and oracle/numerical lemmas.

Repository proof comparisons were deepest for the complete `results/quadratic-ncrank-rational-construction.md`, its supporting review, the finite covariance result, the general-output-body reduction, and the complete supporting covariance-certificate and block-logdet-oracle notes. I also compared the rational Jacobi note and inspected relevant existing checkers. The original result and prior review conclusions were not treated as proof. I read the root source-audit note after independently checking the relevant primary statements.

Primary-source verification used the cached IQS Theorem 1.5 and Lemma 5.3, GGOW Theorem 2.18, GLS1981 Definition (5) and Theorem (3.1), DPV Theorem B.5 and its ellipsoid convention, Zhang–Sra Corollary 8, and Criscitiello–Boumal Proposition I.1. The primary texts support the imported interfaces actually used here. In particular, the cited GLS1981 optimization convention compares with all points of the original body, so there is no missing conversion from an eroded-body optimum.

Limits: I did not re-prove the imported nc-rank, ellipsoid, or weak-optimization algorithms, implement the complete outer geodesic algorithm, audit every bibliographic metadata field, compile or visually inspect the combined PDF, or independently read all 196 indexed notes. Checks below are finite supplements to the proofs. Later-stage claims were checked for their stated scope, not proved.

## Assessment

I found no major mathematical defect. The stage supplies the promised complete rational nc-rank argument, including the lower bound uniform in rational input height. Its arithmetic and geometric constants are consistent with the stage-1 finite capacity bound. I also found the broader finite-covariance, oracle-body, structured-domain, and hardness proof chains coherent within the verification limits above. The remaining finding is a local notation collision, not a false theorem or a substantive proof gap.

## Finding

1. **MINOR — input widths reuse the output-coordinate notation.** Location: `sections/02-quadratic-finite.tex`, lines 55–81, proof of `thm:finite-covariance`, especially the definition `w_i=sum_k |U_ki|` at line 56 and the error expression `|w_j-f_j(x)|` at line 71. The same indexed symbol denotes fixed input-coordinate widths and variable output coordinates within one calculation. Their index ranges can overlap, so a literal reading gives two incompatible meanings for `w_j`. The intended proof is clear from context, and its estimate is correct. Rename the input widths consistently in this proof and `eq:covariance-grid`, for example to `b_i`, while retaining `w_j` for output coordinates. This is an expository notation repair only.

## Independent mathematical reconstruction

The rational nc-rank proof, lines 245–337, was checked in detail:

- IQS Theorem 1.5 returns a maximum-deficiency subspace over the base field and explicitly bounds rational intermediate and final data; Lemma 5.3 supplies field-extension invariance. The statement is therefore stronger than an arithmetic-operation count and meets this proof's actual need.
- For rational `U` and `V=sum_j H_j U`, the spaces `Z=U intersect V^perp` and `W=V intersect U^perp` are orthogonal, satisfy `H_j Z subset W`, and have dimension difference `n-r`. Rational bases need not be orthonormal. Congruence by their concatenation with a basis of the orthogonal complement therefore preserves the claimed zero blocks.
- Nullspaces, intersections, inverses, and enclosing intervals constitute a fixed number of rational linear-algebra stages. Clearing denominators and applying determinant bounds controls their heights. Each row of the inverse transformation is nonzero, so its range on a full-dimensional box has positive width. Retaining the original box inequalities is necessary and is done explicitly.
- The transformed monomial coefficient sum `C` has polynomial height. The dyadic offset is computable by exact comparisons and has polynomial magnitude. Depths `0`, `K`, and `ceil(K/2)` give every nonzero monomial a residual-width product at most `2^-K`. The resulting count is `(r/2)k+(r/2)b+dim(Q)/2` or smaller. Coefficient length is additive in `k`, and the numbers of rows and auxiliaries are linear in `k` times a polynomial in fixed input length.
- Clearing Hessian denominators multiplies the completely positive map by `D_H^2`, hence its capacity by `D_H^(2r)`. GGOW Theorem 2.18 applies to the resulting unnormalized integral Kraus operators and gives `r^(-2r)`, without an entry-magnitude normalization assumption.
- Every positive rational box width is at least the reciprocal product of its endpoint denominators. Thus the principal slice has volume at least `E_B^-1`. Substitution into the stage-1 finite bound and `omega_r^(2/r)<=4` gives exactly the printed denominator `16 D_H (r+2) sqrt(mr) E_B^(2/r)` and the explicit logarithmic lower overhead. The proof dispatches rank zero before divisions by `r` or the definition of positive `C`.
- Coordinate-deletion rank tests can find the principal restriction: the Hermitian principal-compression lemma applies after every successful deletion. The finite lower bound itself only needs existence.

The other principal checks covered:

- Covariance rescaling by `max(4,n/4)`, the contact-volume constant, the shared symmetric residual matrix, and the factor-eight error margin. The graph LP has the correct `sqrt(2)` demand constant. The commuting reduction uses geometric means rather than unjustified ordinary averaging of indefinite energies.
- The determinant certificate's Lagrangian gradient and relative spectral interval `[det P,1/det P]`, including the zero-log-determinant case.
- Exact rational Jacobi orthogonality, contraction, common-denominator growth, and gap-free matrix-function estimates. The outer penalty gradients are positive semidefinite with trace one; the branch-value and gradient errors yield the printed inexact subgradient budget. The recurrence telescopes on stored rational iterates and uses only the distance-dependent curvature factor from the cited comparison inequality.
- Correlated budgets as sums of squared scalarized Hessians, their exact rational double-sum implementation, and the treatment of zero energies. For the correlation SDP, the repaired matrix is exactly positive semidefinite with unit diagonal; the normalized lower and upper objective values suffice for both a near-active gradient branch and final repair.
- Effective output-image equality in both directions, including intersecting a formulation whose original errors leave the image. Symmetry removes the ellipsoid's possibly irrational center. The input quotient retains affine terms along fibers, and rational LDL normalization gives the stated domain-volume loss.
- The logdet hypograph's inner ball and weak separator, and the central-ball convex-combination repair. The PSD block argument uses first moments and unconditional domination; blockwise quotienting preserves a product domain because the original blocks are disjoint.
- Diagonal constants, integer-feature determinant volume, forest face tiling, and the explicit thin-domain example. The Max-Cut reduction distinguishes zero and positive optimum, and the replicated parity packing plus one-bit augmentation proves the stated power-sublinear hardness without claiming a sharper universal linear barrier.

## Executed checks

- Snapshot comparison: **PASS**, all six files.
- `python code/quadratic_rank/check_shrunk.py`: **PASS**, 20 exact nonorthogonal congruences, symmetric shrinking, block zeros, and precision sums.
- `python code/quadratic_rank/check_covariance_algorithm.py`: **PASS**, 26 exact rational Jacobi contractions across six matrices and 40 penalty derivative/feasibility-repair checks.
- `python code/quadratic_rank/check_block_logdet_repair.py`: **PASS**, 24 rational repairs with exact spectral/body checks and 100-digit logdet checks.
- Independent inline SymPy checker: **PASS**, 108 exact depth/error cases on twelve rationally transformed three-input star systems. It reconstructed rational `Z,W,Q`, normalized nontrivial rational boxes, checked every original box vertex is retained by the enclosing coordinates, and verified each transformed output's residual bound at precisions `k=0,...,8`. This checker tests structural and arithmetic consequences; it does not implement IQS or prove asymptotic bit complexity.

No manuscript or research source was edited. No subagents were used.
