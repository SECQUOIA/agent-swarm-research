# Stage 03 author handoff

Status: author complete, ready for the coordinator to freeze the snapshot and dispatch five independent reviewers. This is not stage acceptance. The author has stopped editing manuscript files. No later-stage development was started.

## Files and scope

- `sections/03-predetermined.tex`: new self-contained section, approximately nine pages in the combined 25-page PDF.
- `main.tex`: includes Section03 after the accepted local-baseline section.
- `notation.md`: records the whole-line measure response, integrated moment, sharp supercritical constant, and local scaling notation.
- `claims-map.md`: records X1 as authored and awaiting independent review, with the new exact formula and proof obligations.
- `references.bib`: adds Buttazzo–Oudet–Velichkov (2015 preprint), explicitly identifying the cited Proposition 4.1.
- `reviews/stage-03/author-sanity-checks.json`: symbolic scaling residuals and 50-digit coefficient evaluations, not independent verification.

Claims D1–D4 are fully rederived: convexity for every positive moment, ensemble symmetrization, arbitrary-competitor moving-bump lower bounds, critical shell logarithm, fold lower bound, exact-budget graded upper designs, the sharp subcritical tangent certificate, and the sharp critical logarithmic coefficient. The root-counting density is 1/4 and paired-root averaging is written explicitly. The upper proofs retain the core, rootless, and regular-root contributions. No historical repository note is used as a proof.

## X1 development and proposed resolution

The draft proves the candidate exact supercritical equivalent

`P_q(M) ~ 2^((11q−12)/7) S_q M^((2−3q)/7), q>8/5`,

where `S_q` is the unit-mass L1 whole-line quartic-response moment infimum. The proposed formula from the source notes survives the full localization argument. Its additional conclusions and proof steps are:

1. Finite nonnegative mobility measures are used only as compactness objects for the scalar smooth-test supremum. A measure is never assigned a diffusion process.
2. A derivative-flattening construction proves that the singular part of a limiting measure has no effect on this one-dimensional scalar response. For each compact smooth test, flatten its derivative near a compact set carrying nearly all singular mass, correct the total derivative integral with a fixed smooth bump, and integrate. Source/reaction terms converge uniformly, absolutely continuous derivative energy converges, and singular derivative energy vanishes.
3. Compact tests give vague lower semicontinuity of the response; Fatou gives lower semicontinuity of its integrated positive moment.
4. The whole-line value is finite and positive. A fixed bump proves positivity; a positive graded tail `(1+|x|)^(-alpha)` with `1<alpha<min{2,6−8/q}` proves finiteness.
5. Exact mass scaling is `S_q(m)=m^{-(3q−2)/7}S_q(1)`. Thus singular or escaped mass cannot improve the optimum. Direct vague compactness additionally proves that the unit-mass L1 infimum is attained. No uniqueness, regularity, or explicit profile is asserted.
6. Rescaling arbitrary competing designs about both folds yields a local liminf for each. Integrating over disjoint parameter windows and allocating total limiting mass at most one gives equal mass 1/2 at the two folds and the exact factor `2^((11q−12)/7)`.
7. Recovery starts with an arbitrary near-minimizer, adds a small graded background, and spatially rescales to unit mass. The cost rises by at most `(1+epsilon)^((3q−2)/7)`. Thus smooth approximation or an optimizer-selection theorem is unnecessary.
8. On each cosine half-cell the exact coordinate `x=2 sin((s−s_j)/2)/ell` makes the folded potential exactly quartic. Choosing physical mobility proportional to its metric weight times the local density makes the derivative energy canonical. The metric stays between 1 and sqrt(2) over the entire cell, tends locally to one, and changes the mass by 1+o(1). A final scalar normalization imposes the exact budget.
9. A separate weighted natural-endpoint convergence lemma proves pointwise recovery even for unbounded integrable local densities with a positive graded background. It supplies energy bounds, source-tail control, local weighted derivative compactness, and membership of the limiting function in the minimal smooth energy completion. The auxiliary exponent is restricted below 2 so the finite-energy function is bounded by local Sobolev estimates; cutoff derivative errors then vanish. Compact derivative approximation with an integral correction closes the density step.
10. The graded background gives an integrable rescaled parameter envelope, with root-side power `−q(6−alpha)/8` and rootless power `−3q/2`. It covers the whole assigned parameter half, including offsets away from the fold. Dominated convergence supplies the full moment recovery, rather than only a compact-parameter limit.

The statement that every order-optimal design concentrates all mass remains false and is explicitly excluded by the half-uniform counterexample. The sharper proof does imply full and equally allocated limiting mass for sequences attaining the sharp equivalent. It does not identify a unique limiting profile.

## Author checks and proof boundaries

- Read the accepted Sections 01–02, the full moment source note and its critical review, and the plan/claims/notation ledgers.
- Rechecked the tangent-kernel derivative powers, root-density factor, critical four-sided logarithm, and uniform moving-arc error.
- Independently simplified the graded endpoint exponent, subcritical integrability exponent, folded curvature power, and final power of two using SymPy; residuals are zero.
- Evaluated the established C0, K1, and Kcrit expressions with 50-digit mpmath. The values are approximately 4.6474760094, 18.3860636501, and 2.02233076397. These calculations do not evaluate S_q or certify a discrete approximation to its minimum.
- The root coordinator independently discussed and checked the derivative-flattening, weighted-density, exact-coordinate, and mass-attainment arguments while this stage was being authored. Those checks are not a substitute for the required five independent reviewer reports.
- No mathematical gap is currently known to the author. The new whole-line measure lemma and the natural-endpoint recovery lemma are the highest-priority review targets because they close what was previously an open sharp asymptotic.
- The full-bulk equivalent invokes the accepted same-information, same-budget transfer theorem; no new joint bulk-diffusivity limit is claimed.

## Primary literature

Read the openly accessible primary preprint:

<https://arxiv.org/abs/1506.00141>

<https://arxiv.org/pdf/1506.00141>

Buttazzo, Oudet, and Velichkov, *A free boundary problem arising in PDE optimization*, 2015, Proposition 4.1, printed page 17. Its measure-valued reinforcement formulation and weak-star compactness/semicontinuity argument are explicitly credited in the text. The manuscript does not claim those methods themselves are new. The present whole-line folded-potential integrated-moment limit requires the additional singular-mass, escape, scaling, and recovery arguments above. A broader novelty comparison remains assigned to Stage 07.

No literature package was created or modified. The bibliography deliberately cites the inspected arXiv preprint and identifies it as such; no unverified journal metadata was added.

## Build

From `paper-uncertain-mobility/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

The final build succeeds and generates a 25-page PDF. The final log contains no LaTeX warnings, undefined references, overfull boxes, or underfull boxes. `git diff --check` succeeds. An initial build command was run from the repository root and therefore did not find `main.tex`; it was rerun in the manuscript directory. A missing `end{align}` and one long display were caught and corrected during the author build.

The coordinator may now freeze the unchanged source snapshot and dispatch the five reviewers.
