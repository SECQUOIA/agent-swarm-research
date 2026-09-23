# Final whole-manuscript coordinator audit

Date: 2026-09-07. Review snapshot: `e5a8cd3e390d1b7afa16481b35bcd01944a8111bce55e2ffaf1570f40ebc899d`.

The final five independent reviews are running. This record is the coordinator's own work, not a replacement for them and not supplied as evidence for their reviews.

## Cross-section checks

The scalar class deliberately includes nonclosable coefficients, while physical transport uses minimal closed forms. The positive uniform mixture is Borel, has the same per-observation budget, is closable even for unbounded integrable diffusivity, and supplies the physical recovery needed by all later optimum comparisons. The model assumes zero longitudinal wall advection and nonzero stationary mean speed; the equilibrium and dimensional factor are consistent with that convention. Uniform policy coercivity explicitly makes the general information infima finite, so the ratio theorem does not divide infinite values.

The stationary coefficient follows from the nonnegative spectral measure of the centered velocity. A zero-mode projection gives an infinite limit, consistently with the variational supremum; no ergodicity assertion is needed for an arbitrary degenerate field. Positive backgrounds supply the spectral gap where finiteness is claimed. The axial Brownian term is square integrable under the stated stationary integrability assumptions and has zero conditional mean, giving no advective covariance.

For the supercritical problem, the derivative-flattening argument removes singular measure mass for this smooth-test convention. Vague lower semicontinuity, the exact mass scaling and positivity of the local infimum exclude both escaped and singular mass in a minimizing sequence. The local graded tail can be chosen with 1<alpha<min(2,6-8/q) precisely for q>8/5. The natural-endpoint proof uses a local derivative lower bound, an integrable source tail and bounded limiting functions to justify cutoff recovery despite unbounded coefficients. In the circle recovery, the exact sine coordinate keeps its Jacobian uniformly bounded; the mass normalizer tends to one and the global graded envelope controls the parameter tails. These are substantive requirements beyond dimensional scaling.

For finite precision, attained local minima need neither uniqueness nor an elementary formula. Conditional lower bounds use arbitrary pushed-forward mobility measures and restore any missing absolutely continuous mass monotonically. The exact-coordinate upper construction has a common field for each bin with exact budget; uniform local values are summed only after fold-bin contributions are controlled. The coarse joint limit has its own scale-separation proof, rather than following merely by taking the large-ratio endpoint of a fixed-ratio limit.

The two Stage07 trial consequences were independently checked: the unrounded mean coefficient follows from a global one-sided form comparison and the unrestricted lower bound; the distance-based critical coefficient follows by retained fold-neighborhood comparison and lower-order omitted regions. Numerical tangent values concern only the finite-dimensional, finite-quadrature problems. The revised text explicitly recognizes when optimization uncertainty exceeds mesh or domain differences.

## Complete PDF inspection

All 54 pages of the pre-correction Stage07 PDF were rendered at 72 dpi and visually inspected in nine six-page sheets; both vector figures were additionally inspected at higher resolution. After Stage07 corrections, all 54 pages were rendered again at the same resolution. Pixel comparisons found only pages48,49,51 changed. The coordinator separately inspected all three updated pages. The other51 page images were pixel-identical to the inspected images. No clipping, overlap, missing glyphs, equation-number collisions or broken figure/table layout was found.

Current PDF SHA256: `46adbd0096320ecd7fff2ae878d17be1198f6f37fb64d834e43477ebdce250c9`.

If final corrections alter the PDF, repeat rendering/comparison and inspect every changed page before delivery. The final acceptance record must also preserve the clean build and full review disposition.

## Minor finding: avoid reusing the rate-anchor symbol

`sections/03-predetermined.tex:75` and `sections/04-generic-folds.tex:141` use kappa as a freely chosen small bump-width factor. Section01 already reserves kappa for the uniform lower bound on the integrated exchange rate. The local proof is valid and the constants can be chosen independently; this is a notation clarity issue, not a mathematical gap. Rename the bump factor to a distinct local symbol, for example delta_*, in both proofs and their immediately accompanying wording. Preserve kappa for the rate anchor. The separate fixer should make this minor correction after all final reports have been adjudicated.

## Minor finding: state fabrication constraints as an unstudied class

`sections/08-discussion.tex:49–51` groups a mobility cap, mandatory positive background and fixed fabrication length as constraints that “can obstruct the shrinking scales.” The constraints are outside the proved class, but this wording can imply a common established effect on the asymptotic scales. A fixed positive cap need not bind the explicit small-budget profiles, whose peak amplitudes decrease. No extension of the theorem is needed here. Replace the sentence with a precise scope statement that the theorems concern the stated integral-budget class and do not establish optimal values under additional pointwise, background or fabrication constraints. This is a minor qualification of discussion language; no theorem or new capped-design investigation is requested. The statements in Sections 03/05 that such constraints change the admissible problem are already accurate and need no change.

## Adjudication cross-check: a regular physical normalization case

Reviewer4 independently supplied a useful constant-rate disk check, retained in that report. The coordinator verified its factors directly: for disk radius R, bulk speed U and constant desorption k, V=U R/(R+2K), J=P/k, and the mean-zero radial bulk solution has derivative -(U-V)r/(2D_b). Its derivative energy is (U-V)^2 pi R^4/(8D_b), its boundary trace is constant, and the Schur penalty vanishes. Thus the finite-bulk formula has remainder (U-V)^2 pi R^4/(8D_b Z). The exchange term chi P/k also agrees with the elementary perfectly mixed two-state occupation-time coefficient U^2 A^2 KP/(k Z^3). This is a normalization check, not a claimed new paper result.

## Final correction verification and delivery inspection

All five final reports were read in full, and their findings were adjudicated before assignment to the separate fixer. The coordinator read the final correction record and the complete unified diff, verified all ten corrected-file hashes, checked the unchanged numerical artifacts and bibliography, and confirmed the intended notation and positive-mass case changes. No new substantive issue emerged. The source patch is preserved in `round-01/corrections.patch`.

The delivered PDF was rendered in full at 72 dpi. Only pages 2, 20, 30, 52 differed from the previously inspected final-review PDF. Each changed page was separately viewed at original rendering resolution; all were legible, without clipping or overlap. The other 50 page images were pixel-identical. This completes all-page inspection of the final 54-page artifact. Its hash is `260be943f47f06955b4b78c6baa158ebbe44394009b008ea3c4c96cb0eef2dd3`. The final source and artifact records are in `accepted-snapshot.json` and `artifacts.json`.
