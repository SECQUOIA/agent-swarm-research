# Stage 3 independent review 1

Verdict: **PASS. No required major or minor issue identified.**

I read the complete frozen Stage 3 manuscript, both appendices, bibliography, macros, README, and all four checkers. I compared the integration changes with Stage 2. I did not read other review reports or modify manuscript inputs.

## Scientific and editorial assessment

- The abstract, introduction, foundations, and conclusion consistently state the consequential modeling assumption: independently specified positive voltage and signed injection intervals, with simultaneous singleton voltage/injection bounds permitted. The manuscript expressly distinguishes this class from fixed-source-voltage demand feasibility, relaxation-exactness subclasses, and lossless fixed-magnitude AC hardness. It does not imply hardness after removing the constraints its gadgets require.
- The main claimed contribution is precise: a rational solution-preserving electrical realization followed by simultaneous graph/data restrictions. Known arithmetic, crossover, triangulation, winding, and polynomial-minimum tools are credited. The qualified priority sentence refers to the restricted resistive model and the prior results discussed, rather than claiming that all ingredients are new.
- I rechecked the complement/addition/inversion algebra, free-injection estimate, copy allocation and size bounds, generalized crossover ranges, connector degree argument, and harmonic subdivision. I found no failure of the claimed unique extension, including repeated or unused variables and degenerate empty source systems.
- The revised linear-size quadratic AC formula has four real variables per bus and one per edge; root-normalized difference equations enforce integral shifts without integer quantification. The sign convention agrees with the displayed explicit lift. The manuscript distinguishes ordinary real differences, principal angles, and reference-fixed boxes; one-sided reactive intervals are correctly explained by exact saturation. It does not claim the false fixed-principal-window equal-angle implication.
- Rational universality is confined to compact basic closed sets over the rationals. I checked the denominator-protection/inverse-identity proof and the three-quadrant obstruction. The separate triangulation-based topological theorem and designated algebraic-coordinate argument retain their correct broader/narrower scopes. Appendix A gives sufficient algebra and range reasoning to stand independently of the disputed Boolean preprocessing claim.
- The tiny-residual family is expressly the ordinary bounded-degree fixed-data construction. The abstract and conclusion no longer suggest that its residual guarantee survives planarization. The recurrence, one-violating-bus calculation, two-sided transfer constants, compact minimum argument, gap-promise rounding, and reactive energy estimates are internally consistent. Their significance is accurately described as a limitation of residual-only certification, not a lower bound on all exact algorithms.
- The eight small examples have the stated exact outcomes. Removing solver anecdotes improves the appendix's evidence: the current claims match exact proofs and reproducible checks, and finite tests are explicitly not treated as quantified proofs.

## Literature checks

I independently checked the local primary text of *Dynamic Toolbox for ETRINV*, Definition 4, Theorem 1, and Lemma A. The manuscript uses the same rational-coordinate definition and accurately identifies the unconstrained inactive-branch auxiliary issue. I also checked the local primary Jeeninga Part I model and Theorem 3.18: the absence of operating voltage restrictions and the demand-set convexity distinction support the manuscript's model comparison.

Fresh targeted web searches for power-flow existential-real/ETR completeness and resistive semialgebraic feasibility did not identify a directly matching prior restricted electrical realization. Those searches are limited negative evidence, not proof of priority; the manuscript's qualified language is appropriate. I did not identify a necessary additional citation from those results.

## Reproducibility and presentation

I copied the frozen package to `stage3-review1-validation/` and independently ran all four exact checkers with Python assertions enabled. All passed with the advertised counts. A clean `latexmk` build completed successfully and produced a 31-page PDF with no warnings, undefined references, overfull boxes, or underfull boxes in the final log. I visually inspected the supplied first-page render; the title, abstract, and introductory text are readable and unclipped. This was not a separate all-page visual audit.

All 18 members of `submission.zip` match the corresponding frozen Stage 3 files byte for byte. The portable README correctly documents dependencies, the no-optimization assertion requirement, exact-check limitations, and the separately supplied PDF. Blank author metadata is explicitly documented and remains an administrative input for the author, not a mathematical defect.

No optional stylistic change is needed for acceptance of this stage.
