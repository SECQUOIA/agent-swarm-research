# Completed manuscript and verification record

The paper is complete in `paper-additive-coagulation/`. Its PDF has 55 pages, 12 main sections, five appendices, 23 references, and 44 formal mathematical statements. Those statements include supporting lemmas and established-method specializations; they are not 44 claims of independent novelty.

## Scientific content

The central argument connects sharp normalized fractional-moment decay to separation of number and mass sampling. It supplies a finite nonlinear correction on auxiliary number paths, exact extended transport cost, logarithmic limit transfers, controlled last-event tails, and sharp daughter-law comparisons. Critical identities give exact last-event observables, a density, optimal overlap constants, and rigorous scalar-dissipation obstructions.

The physical finite-population analysis proves nearly maximal mass-CDF discrepancy on a sufficient logarithmic horizon from exactly matched initial data, while normalized count remains accurate on sublinear horizons. The exact count law and its classical diffusion scaling are developed separately. Nine retained simulations illustrate the sampling separation and have a self-contained reproduction package.

The inverse application proves exponentially accurate Fourier factorization and exact structural identification despite additive coagulation. A separate independent-sampling theorem gives a fixed-frequency ratio certificate and a sufficient observation-time balance. Count-neutral classification, observable rigidity, power-kernel stationary exclusion and counterexamples, preparation constraints, and initial-rate tomography complete the related repository material.

## Developments beyond transcription

- A weighted-variation construction proves global existence and uniqueness for measurable parent- and time-dependent expected daughters, under finite initial second moment and within the locally bounded second-moment class.
- Convex tangent truncations justify the full second-moment and entropy balances. The entropy-production lower bound is improved to the sharp coefficient `lambda m^2 log 2`, with actual-solution initial right-derivative sharpness.
- The controlled fragmentation path dichotomy and the general critical last-event density have direct proofs with the required measurability and stopping-time arguments.
- Review corrected an erroneous nonlinear log-lattice claim and an overstatement of the fraction-one identification boundary. The relevant source notes were amended. Expected daughter count and mass also suffice for the second-moment daughter bounds; an unnecessary eventwise-binary restriction in an old note was removed.

## Review and validation

Five sequential writing stages each had one author and five independent reviewers. A separate agent corrected every accepted finding. No stage had an accepted major issue, so no major-triggered repeat was needed. Five fresh reviewers then independently checked the full manuscript and all 44 formal statements. All five final reports recommend acceptance with zero major and zero minor issues. There are 30 written review reports, with frozen snapshots, coordinator assessments, and separate revision records.

The reviewed PDF builds cleanly with PDFLaTeX and BibTeX. Multiple private forced builds passed. All pages were visually inspected during full review; the figure and tables were also inspected at larger scale. Citations and references resolve. The full nine-run simulation dataset was independently reproduced during Stage 4, including 6,588,932 events; the independent count diagnostic and a sanitizer audit passed. Exact rational arithmetic certifies the overlap interval and the positive power-kernel counterexample bound. Narrow supplement checks passed again in the full review.

## Scope limits retained

The paper does not determine the exact critical calendar-time last-event exponent, claim stable whole-law recovery from noisy Fourier data, or identify the first finite-population breakdown time. It does not infer independent samples from interacting particles or claim that the numerical runs compute a continuum PDE comparison. These are explicit boundaries of the proved results, not unresolved proof steps. Classical ingredients are attributed, and literature searches do not certify publication priority or future citation impact.

The final coordinator assessment is `reviews/full-round1/assessment.md`. Final source and artifact hashes are recorded in `final-accepted-snapshot.json`. No additional research direction was started after completion.
