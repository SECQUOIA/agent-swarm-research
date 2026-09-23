# Stage 3 author report

Author: `paper_stage3_author`. Date: 2026-09-07. Status: five independent reviews and accepted minor corrections are complete; coordinator verification and stage 3 acceptance are pending. See `stage3-revision.md`. No reviewers were dispatched by the author and no later stage was started.

Added three sections (`last-event.tex`, `daughter-comparison.tex`, `critical-last-event.tex`), `appendices/product.tex`, and the script/JSON in `supplement/`. Added inputs and two verified bibliography entries. Updated every Stage 3 coverage row, README, and the Stage 3 workflow status while preserving coordinator history.

## Proof coverage and decisions

Read the three assigned result notes, all five corresponding proof/literature reviews, the original verification script/JSON, and the accepted manuscript and development records. The assigned claims now have complete proofs, rather than citations to research notes.

1. The controlled first-event hazard has mean `q u_(t,T)` with parent-dependent daughters. Its fractional tail proves finite last time under every control. The best scalar Jensen coefficient, exponential moments, future-path TV comparison, exact window means, conditional means, and higher count-moment bounds are included. Common innovations evaluate each process's own daughter kernel after divergence.
2. The all-rate benchmark equations and conditional convex inequalities are proved with only a first hazard moment. The infinite-horizon comparison uses L1 convergence rather than monotonicity of normalized size. The positive epsilon family approaches the extreme envelope with an explicit residual estimate. Zero fragmentation gives the exact deterministic hazard.
3. The optimal all-rate overlap coefficient `1-w_ext(1)`, critical rational envelope, constants `1/2` and `1-Psi(1)`, and common upper constant one are covered. Positive mean-one finite-support population preparations establish all sharpness claims within accepted existence assumptions.
4. For equal splitting, the product recurrence cancels the negative coagulation term. The remaining pair integrand is bounded by one; accepted total variation continuity gives a continuous last-event density. The Laplace PDE and exponential-sum mixture have explicit derivations. General critical daughters use conditioning at each coagulation stopping time before compensating the projected future mark, yielding an integrated density without time regularity of the kernel.
5. The rational envelope gives the lower calendar-time tail and exponential-moment bracket, including divergence at `r=b`. A realizable two-point example proves the optimal instantaneous coefficient `b`. Another strictly positive two-point family excludes every fixed positive power-law lower dissipation estimate, with every positive moment finite for each population. No claim excludes every conceivable scalar estimate or determines the exact time exponent.
6. The appendix proves the periodic large-size product expansion, endpoint agreement, explicit remainder and its quadratic/cubic refinement, and the rational overlap certificate. The pure-coagulation Borel benchmark is derived explicitly: `h ~ sqrt(2) exp(-bt/2)`, showing that the robust fractional-moment exponent need not be sharp.

No accepted mathematics required correction. New results use `def:solution`; all sharpness populations have finite second moment and therefore solutions by `thm:existence`. The source notes' older existence caveats were not copied.

## Primary sources checked

- [Bertoin–Biane–Yor, author manuscript](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf): equations (1.3), (1.6), and Theorem 1.1(i) give exactly the exponential sum/product after scaling by one half. The [author's publication record](https://www.math.uzh.ch/member/bertoin/publications) verifies 2004, volume 58, editors, and pages 45–56. The product is explicitly attributed as classical.
- [Rüschendorf–Schnurr–Wolf, primary preprint](https://arxiv.org/abs/1505.02925) and [publisher record](https://doi.org/10.1017/apr.2016.63): authors, 2016, volume 48(4), pages 1015–1044, and generator-comparison scope verified. This is methodological context; our bounded martingale proof checks its own hypotheses.
- [Bertoin (2009), primary article](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf): rechecked the classical Golovin–Borel formula, equation (3), and retained its accepted entry. The last-event asymptotic is our explicit deduction from that known formula, not attributed as a verbatim theorem of the article.

No files under `literature/` were accessed or altered. No literature package was ingested and no publication-priority claim is made.

## Validation

`make` completed: 30-page PDF, no final LaTeX/BibTeX warnings, undefined references/citations, or overfull/underfull boxes. Transcript: `/tmp/ramki-stage3-build.log`. Extracted PDF text was inspected.

The supplement ran successfully and reproduced the research JSON byte for byte; the copied script is also byte-identical. Independently reran the appendix's exact Fraction assertions proving both strict 30-decimal endpoints. Floating-point counterexample values remain illustrative.

At the author's handoff, SHA-256 checks against `stage2-accepted-snapshot.json` confirmed that the accepted model, fractional moments, auxiliary process, log limits, existence appendix, and Makefile are unchanged. Existing bibliography entries were retained. No unresolved proof issue was identified by the author. The subsequent five independent reviews and corrections are recorded in `reviews/stage3-round1/` and `stage3-revision.md`.
