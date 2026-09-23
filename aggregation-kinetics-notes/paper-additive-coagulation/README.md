# Additive coagulation–fragmentation paper

The completed manuscript is **Sampling-law separation and finite nonlinear corrections in additive coagulation–fragmentation**.

- [Read the PDF](main.pdf): revised after an external referee review; see [the revision record](development/referee-revision.md). Four appendices and a separate [supplementary note](supplement/observation-design.tex).
- [LaTeX entry point](main.tex).
- [Reproducible numerical and exact-arithmetic supplement](supplement/README.md).
- [Claim-level repository coverage](development/COVERAGE.md).
- [Final review assessment](development/reviews/full-round1/assessment.md) and [development workflow](development/WORKFLOW.md).

Run `make` in this directory to build with PDFLaTeX and BibTeX. Use `make -B` to force a full rebuild. The supplied figure PDF allows the paper to compile without Python or C++; those tools are needed only to reproduce the supplement. No journal class or external bibliography manager is required. Author names and affiliations remain blank for the researchers responsible for submission to supply.

All five writing stages were accepted through the internal review process recorded in the [final report](development/FINAL-REPORT.md). A subsequent external journal-style review found no mathematical error but required a major revision for framing, scope, references, and proof presentation; the changes are listed in [the revision record](development/referee-revision.md). The hashes in `development/final-accepted-snapshot.json` describe the pre-revision sources.

The paper covers instantaneously sharp fractional moments and number–mass separation; controlled auxiliary paths and finite nonlinear log corrections; transport and logarithmic limits; last-event tails, daughter-law extrema and exact critical representations, with the critical exponent reduced to a deterministic overlap rate and a conjectured value; finite-population discrepancies and retained simulations; count-neutral and power-kernel results; and Fourier identification with explicit observation limits. Supporting preparation and initial-rate algebra is in a supplementary note.

Writing resolved gaps in the earlier notes. The paper supplies measurable-parent existence and uniqueness in the locally bounded second-moment class, justifies unbounded moment balances, and proves the instantaneously sharp entropy-production coefficient. It also corrects earlier lattice and identification-boundary wording. Classical probabilistic, transform, and mixture-model ingredients are explicitly attributed. The exact critical last-event exponent and stable full noisy daughter inversion are not claimed to be solved.

The numerical supplement contains all nine retained particle runs and 90 snapshots, code and saved data, a six-panel figure, and exact rational checks. The simulations illustrate separation and the gap between certified and observed decay rates; no continuum PDE comparison or independent numerical proof of the growing-time discrepancy theorem was computed. Final accepted source and PDF hashes are in `development/final-accepted-snapshot.json`.
