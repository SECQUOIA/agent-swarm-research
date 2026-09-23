# Stage 3 author record

Scope: shared physical reservoirs, subsystem and joint probability accuracy, and information. Created `sections/shared-baths.tex`, added its input in `main.tex`, and added the explicitly discussed Ramírez-Hernández–Larralde–Leyvraz reference to `refs.bib`. No mathematical claims in the earlier sections were changed.

## Coverage

- Exact centered power-law bath for two identical independent copies, with a global weight bound by one.
- Full-state convergence to the canonical product conditioned on opposite phases for `N << c_N << N^2`, using only positive limiting phase weights and conditional square-root-N tightness.
- Exact limiting joint TV `w_-^2+w_+^2` and full one-copy marginal TV `|w_-−1/2|`.
- A separate proof of full microscopic mutual-information convergence to `log 2`, using bounded likelihood integrals and the relative-entropy chain rule.
- Optimized joint canonical threshold `c_N >> N^2` for any fixed number of identical copies, by the Stage 1 weak-support theorem. This needs only the macroscopic two-atom limit, with arbitrary deterministic energy centering.
- Fixed-copy, fixed-phase-count selection for every `0<=k<=m`, including endpoint cases. Derived full marginal/joint TV and total correlation `m H(k/m)−log binomial(m,k)`.
- A proved finite-size temperature-balancing lemma for bounded spin energies, with the correct sign and phase ratio. For the short-range moment decomposition, the conditional auxiliary bond kernel is retained at beta_c while the spin law is reweighted to beta_N; its bounded joint likelihood preserves moments and exceptional mass. Independent kinetic variables are treated separately through their exact Gamma/product-Gaussian KL formula; no globally bounded unbounded-energy likelihood is claimed.
- Application of the shared results to the newly verified plain mean-field and fixed-dimension short-range Potts models. The isolated-copy thresholds persist after the specified temperature shift because positive phase moments and exceptional-event bounds persist.
- Linear-capacity centered boundary `c_N/N -> gamma>0`: opposite-phase selection, weak Gaussian fluctuation tilt, covariance and conditional variance formulas, microscopic marginal TV, Gaussian-CDF expression at balance, and full microscopic mutual information.
- An explicit full joint TV limit at the linear boundary, both as a bounded scalar Gaussian expectation and as a normal-CDF formula. This follows directly from the positive-likelihood set and completes the joint/marginal comparison.

## Critical proof checks and choices

1. Every shared-bath theorem uses actual disjoint phase events on the one-copy state space. No auxiliary latent Gaussian label is silently substituted for an observable phase partition. In the microscopic applications, the existing Voronoi spin cells or actual midpoint energy events supply the needed partitions.
2. The broad phase-selection window requires only tightness, not a Gaussian limit or positive within-phase variance. Thus it includes the pure-spin mean-field model even though its disordered energy limit is degenerate.
3. The bath is centered at the selected mixed total energy, and its weight is globally at most one. This controls rare interphase events and far tails without imposing an unverified envelope or interpreting a signed remainder probabilistically.
4. The two-copy joint-threshold corollary centers the total energy before scaling. The abstract result does not require separate limits for the absolute phase centers divided by N.
5. Mutual-information convergence is never inferred from TV or weak convergence alone. The joint proof uses boundedness and continuity of `W log W` on `[0,1]`; the marginal proof uses globally bounded likelihood ratios and uniform continuity of `r log r` on a fixed compact interval. All finite-N divergences used in the chain rule are finite.
6. The fixed-count proof treats zero limiting marginal phase weights at `k=0,m` through continuity at `r=0`. The original canonical phase weights are still strictly positive. The limit of total correlation at those endpoints is zero.
7. Temperature balancing is stated for a prescribed target sequence. The common bath uses the same inverse temperature as that sequence. The resulting canonical marginals are compared with the balanced reference at `beta_N`, not the original unbalanced reference at `beta_c`.
8. At linear capacity, same-phase deviations are order N and the argument of the bath logarithm need not be small. Their suppression uses the exact inequality and cutoff. The zero-centered Taylor expansion is used only within opposite-phase windows.
9. The linear-boundary Gaussian formulas assume **both** phase variances are positive. The pure-spin mean-field model is explicitly excluded from those positive-variance formulas while remaining included in the other shared results. Plain sufficiently-large-q short-range spins satisfy both positive-variance conditions in every fixed dimension covered by Stage 2.
10. The covariance statement is about the weak limiting Gaussian law; no convergence of arbitrary microscopic second moments is asserted from weak convergence alone.
11. The finite-N approximation at linear capacity retains the actual microscopic canonical laws and changes only their bounded energy likelihood. That approximation converges in full TV to the exact bath law. It is not an assertion of microscopic TV convergence to Gaussian densities.
12. The marginal linear-boundary proof explicitly handles uniformity on compact energy windows by a finite-grid/weak-convergence argument and controls the rest by tightness and bounded likelihoods.
13. The new scalar joint-TV formula was derived by integrating `Q−P` over the positive-likelihood set. The coordinator independently reproduced it and checked it by scalar quadrature for disparate parameters; see `reviews/stage-3-coordinator-investigation.md`. The existing unequal-variance covariance, marginal TV, and KL cancellation formulas were also independently checked by the coordinator.

## Source use and attribution

Read `research/shared-bath-phase-correlations.md`, its full independent mathematical review, and `research/verification/shared-bath-prior-art.md`. The manuscript includes its own proofs and refers directly to already verified theorems in Sections 2–3, rather than repeating their derivations.

Rechecked the retained primary text `research/sources/ramirez-etal-2008-zeroth.txt`, especially the discussion surrounding its Figure 3. The opening attribution is narrow: opposite phases and exchanged assignments in coupled negative-specific-heat systems were already observed. The citation does not attribute the present external-bath scaling or full-law TV results to that work, and the stage makes no unsupported priority claim. Bibliographic entry: A. Ramírez-Hernández, H. Larralde, F. Leyvraz, *Violation of the Zeroth Law of Thermodynamics in Systems with Negative Specific Heat*, PRL 100, 120601 (2008), DOI `10.1103/PhysRevLett.100.120601`, arXiv `0802.1748`.

Broader prior-art discussion and publication positioning remain the planned synthesis stage.

## Deliberate scope boundaries

The copies are identical and independent in the canonical reference, and interact only through the additive reservoir constraint. The number of copies is fixed. Linear-capacity conclusions are for the specified centered calibration, not an optimization over arbitrary total energies. There is no claim about dynamical independence, switching times, nucleation rates, growing copy counts, or generic directly interacting subregions.

The linear formulas with zero phase variance are not asserted. A degenerate Gaussian extension could be considered separately, but is not needed to cover the stated microscopic examples and was not added to this stage.

## Compilation and review status

`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` produces a 27-page combined draft. The final log contains no undefined citations or references, LaTeX warnings, or box warnings. Stage 3 is ready for the user-required five independent reviewers.
