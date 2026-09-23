# Stage 05 author handoff

Author: `paper_stage5_author`. Prepared 2026-09-07. The stage is authored and ready for the required five independent reviews; it is not marked accepted.

## Scope and changed files

- Added `sections/05-exact-observation.tex` and its input in `main.tex`.
- Updated the O1/O2 authoring status in `claims-map.md` and added the local response/slope symbols to `notation.md`.
- Added the inspected cooling-fin precedent `AlexandersenSigmund2021` to `references.bib`.
- Added this record and `author-sanity-checks.py` / `author-sanity-checks.json` in this directory.
- No accepted section source was changed. Stage 06 was not started, and no writing or proof work was delegated.

## Results and proof coverage

1. The exact quadratic whole-line placement problem is solved over all nonnegative L1 fields of the prescribed mass. The polynomial profile, mass normalization, source representative, source/energy integrals, and sensitivity identity are derived directly. The flux vanishes at the central cusp and the two outer edges. The global bounded-slope certificate is justified for each arbitrary L1 competitor by cutoffs, mollification, and dominated convergence. Its equality case proves uniqueness almost everywhere. The whole-line source is treated as an energy-dual functional, not an L2 source or an infinite-wall stationary process.
2. The compact-wall theorem covers continuous rates with finitely many fixed, separated quadratic zeros. The lower proof uses the competitor's actual masses in disjoint fixed neighborhoods, including the zero-mass infinite-response case. Optimizing these local lower bounds gives the allocation proportional to curvature to the power −2/3. The upper proof completes the square directly on each support with zero flux and integrates the reciprocal potential outside. No assumed compactness, smoothness, or concentration of competing designs enters the lower proof.
3. The physical corollary first transfers the optimized leading value by the accepted same-budget theorem. It also verifies closability, zero-capacity endpoints, fixed-budget coercivity, and positivity comparison for the explicit degenerate localized trials. Their exchange flux obeys `||kh−1||2=O_eta(M^(1/10))`, and their bulk remainder converges to the accepted regular bulk value R0. These are fixed-profile statements; no uniform-in-offset bound near coalescence or additive bounded error for the optimum is asserted.
4. Exact observation is defined as an infimum over Borel policies with an exact budget for every offset. A single explicit policy gives the sharp upper mean: two lower-curvature quadratic profiles in the separated regime, a constant fold patch in the layer of width M^(2/7), and a uniform field on rootless offsets. Its curvature loss is `eta=(M/a^(7/2))^(1/10)`, larger than the support-to-root scale; a sufficiently large fixed fold cutoff ensures all supports fit. Explicit reciprocal-potential estimates, a fixed-interval coercivity argument in the fold patch, and Borel dependence of translations/dilations give a globally admissible policy with integrable domination.
5. The sharp oracle lower mean uses Fatou's lemma on near-optimal Borel policies and the pointwise arbitrary-competitor compact-wall theorem. It makes no expectation–infimum interchange or unproved measurable minimizer selection. The constant is `Kobs=22.404628230749...`, and the oracle/blind ratio is `1.218565792934... M^(1/20)`. The same-budget transfer proves the corresponding physical asymptotics.

The compact comparison with uniform diffusion explicitly invokes the potential-ordering proof of the accepted harmonic result, which only needs the local asymptotic and positive exterior potential. It does not silently apply that proposition's C2 statement to the present continuous rates.

## Self-verification

Run from the repository root:

```sh
python paper-uncertain-mobility/reviews/stage-05/author-sanity-checks.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -cd paper-uncertain-mobility/main.tex
```

The check script verifies exact symbolic polynomial/PDE and energy identities, computes the displayed constants at 70-digit working precision, and samples 1,920 points of the separated-policy lower potential bound over four small budgets and offsets on both sides of the ensemble. The sampled potential ratio is at least 1.00000829 and the largest sampled support-radius / comparison-neighborhood ratio is 0.105901. These are sanity checks only; the manuscript supplies uniform analytical proofs.

The script directly checks changed manuscript sources for trailing whitespace and unexpected control characters. A carriage return in an initial Borel subscript was identified during the author's pre-freeze audit with the coordinator and removed. The final scan passes.

The final build succeeds with no LaTeX warnings, overfull/underfull boxes, or unresolved references. The assembled PDF is 37 pages at this stage. PDF pages 30 and 34 were rendered and visually inspected: the local theorem, policy definition, oracle theorem, and long scaling displays fit and are readable. Final whole-manuscript inspection remains a later required stage.

## Literature boundary

The section attributes saturated-gradient methods to the existing Buttazzo–Oudet–Velichkov reference and constant optimal gradients in fixed-volume cooling-fin design to Alexandersen and Sigmund (2021), DOI `10.1109/ITherm51669.2021.9503196`, proceedings pages 24–30. The coordinator obtained the institutional accepted manuscript; the author inspected its title/metadata and printed pages 1–3, including the thickness-dependent derivative coefficient, fixed-volume constraint, and constant-slope optimality condition. The bibliography links the institutional copy without redistributing it. The fin model has a base load and constant reaction; the present explicit local calculation has a uniform source and quadratic killing. No broad novelty claim is made for the optimization framework or the constant-gradient principle. The final-stage literature audit remains necessary.

## Suggested independent review emphasis

Please audit the smooth-test/global certificate and uniqueness; the unrestricted local-mass lower bound; the explicit coefficient's closure and endpoint domain; fixed-profile bulk remainder convergence; all paired-root factors; the scale separation in the measurable recovery policy; fold free-endpoint coercivity and reciprocal tails; and the Fatou/dominated-convergence proof at the policy level. The author has no unresolved mathematical question within this stage's scope.
