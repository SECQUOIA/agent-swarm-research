# Reviewer 01 — stage2-round1

Primary lens: adversarial end-to-end validity, hidden assumptions, counterexamples, and exact scope.

Major findings: 0
Minor findings: 1

## Frozen files and review coverage

I checked these SHA-256 hashes with `sha256sum`. Every value agrees with `reviews/stage2-round1/snapshot.json`.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I read the complete 1,546-line stage-2 section, the stage task and lenses, process/protocol, bibliography, and coverage inventory. I re-read the accepted stage-1 representation, parity, principal compression, symmetric shrinking, and covariance dependencies, using my preceding complete stage-1 review for the other unchanged construction ingredients. I compared the corresponding proof portions of all thirteen stage-2 canonical result files. Supporting-note comparisons included rational Jacobi matrix functions, block logdet allocation, covariance certificates, commuting reduction, the thin-domain obstruction, and the covariance benchmark gap. The stage-2 coverage rows have identifiable manuscript locations for their stated substantive developments.

The following primary-source interfaces were checked directly in the cached source texts, not inferred from audit verdicts:

- IQS Theorem 1.5: a maximal base-field shrunk subspace is an output, and the rational case explicitly bounds intermediate and final data sizes; Lemma 5.3 gives field-extension invariance.
- GGOW Theorem 2.18: the unnormalized integral Kraus-operator capacity is at least `r^(-2r)`.
- Zhang–Sra Corollary 8 and its proof: the one-step distance inequality uses the distance to the comparison point in the curvature factor and remains useful with projection.
- Criscitiello–Boumal Appendix I: the specified affine-invariant metric is Hadamard and Proposition I.1 gives the lower curvature bound `-1/2`.
- GLS 1981 Definition (5) and Theorem (3.1): weak optimization has the stated distance and objective guarantees against the original body, with known inner/outer balls. This particular source does not introduce the eroded-body comparison that could otherwise invalidate the repairs.
- DPV Theorem B.5: strong-oracle rounding has the specified rational ellipsoid matrix, potentially real center, and `(d+1)sqrt(d)` inclusion factor.

I subsequently read `verification/stage2-root-source-audit.md` as a cross-check, not as a substitute for these inspections.

Limits: I did not implement the full IQS, ellipsoid, or outer rational geodesic algorithms; I checked their required source interfaces and the manuscript's reductions and error accounting. I did not independently verify every bibliography entry or publication-priority claim, inspect all 196 supporting notes, compile LaTeX, or visually inspect the PDF. The review covers the completed stage, not undrafted stages 3–4.

## Overall assessment

I found no major mathematical issue. The rational noncommutative-rank preview is now supported by a complete argument at the promised level: rational shrinking, basis-height control, exact interval normalization, dyadic allocation, and the principal-slice integral-capacity lower estimate account for the formerly deferred obligations. In particular, the capacity rescaling exponent is correctly `2r`, and the box-volume denominator bound is sufficient without finding the principal set algorithmically.

The finite-accuracy chain is coherent. Contact covariances satisfy the stated cap and energy bounds; the rotated shared grid contains the exact graph and controls all outputs with a factor-eight margin. The geodesic exact penalty repairs feasibility with precisely the log-determinant cost stated. The branch-gradient normalization, polynomial search radius, stored-iterate recurrence, local rounding, and final rational covariance sandwich support the claimed dimension-only additive loss. The proof does not rely on a well-conditioned exact eigenbasis.

The grouped and total-absolute-error arguments retain a common monomial error matrix. Their rational algorithms handle cancellation in rational energy sums through positive rational lower certificates. The correlation repair gives both a feasible near-active branch and an upper value for final scaling. Output-image restriction and input-kernel projection preserve graph containment even when original errors leave the nonlinear image or affine terms vary along fibers. The domain-volume loss is retained before normalization.

The positive block bounds use positivity and unconditionality in the required places, and the separate block quotient preserves a product domain because the original coordinate blocks are disjoint. The integer-feature and forest bounds retain their actual normalized image volumes. The thin-domain and growing-dimension examples distinguish limitations of the hypotheses and benchmark from complexity hardness. The Max-Cut amplification and scalar appendage correctly give the promised positive-optimum lower packing and exclude fixed power-sublinear guarantees, without claiming to exclude every sublinear overhead.

These are bounded review conclusions; no absence-of-error certainty is claimed.

## Finding

1. **MINOR — an input-width symbol collides with the visible output vector within the same proof.** Location: `sections/02-quadratic-finite.tex`, lines 55–61 and 71–73 in the proof of `thm:finite-covariance`; the width notation is reused at lines 79–81 and in later references to the grid. The quantities `w_i=sum_k |U_ki|` are fixed side widths of the rotated input box, while `w_j` in `|w_j-f_j(x)|` denotes a coordinate of the variable output vector from the representation model. With `n=m=1`, the same symbol `w_1` consequently denotes both the fixed width one and the varying approximation output in adjoining formulas. The intended argument is clear from context, so this is a notation/exposition defect, not a mathematical counterexample. Rename the input widths, for example to `b_i`, throughout this grid construction and its direct references, keeping `w` for the visible output. The later integer-feature subsection can use its own explicitly scoped width notation, though consistent width notation would help there too.

## Independent executed verification

I ran an independent NumPy/SciPy check with fixed random seed 731, dimensions 1–6, and twenty cases per dimension. It used noncommuting symmetric Hessians and positive definite matrices constructed from symmetric matrix exponentials.

- All 120 cases passed the trace-one normalized energy-gradient check, agreement with a centered finite-difference directional derivative to tolerance `1e-7`, and a midpoint geodesic convexity inequality.
- For the 112 cases whose comparison point lay in the selected projection ball, the projected one-step distance inequality passed to tolerance `1e-9`, with the actual comparison-point distance used in `d/tanh(d)`.

These finite checks support the analytic formulas; they do not prove the universal convergence or bit-complexity claims. I also manually recomputed the inexact-oracle and telescoping constants, correlation repair loss, rational grid determinant loss, diagonal overhead bound, and the positive-optimum packing count.

No manuscript or research files were edited, and no subagents were spawned.
