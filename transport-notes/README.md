# Transport theory research

This repository develops and checks theoretical transport results relevant to soft matter, complex fluids, interfaces, and diffusion. Work began on 2026-09-06 with an existing local literature library; the only tracked file before this work was `.gitignore`.

Results distinguish mathematical verification from novelty. Targeted literature audits found established ingredients and no exact matches to the principal design and measurement-resolution laws. Search and access limits remain explicit; absence of a match does not prove novelty.

The strongest developed contribution concerns mobility design for uncertain kinetic defects: optimal placement changes the divergence of transport moments, and the precision of defect measurement determines which design scaling is attainable. These results extend to generic smooth kinetic folds and finite bulk diffusion. An earlier [surface-exchange crossover](notes/result-surface-exchange.md) and exact deterministic placement solutions supply the common model and local theory.

## Research records

- [LaTeX manuscript: Designing surface transport under uncertain kinetics](paper-uncertain-mobility/README.md): full proofs and reproducible numerical evidence. Its new proofs of the sharp supercritical coefficient and finite-ratio measurement crossover supersede the historical notes' open-status statements for those two limits.
- [Results guide](RESULTS.md): verified theorems, candidate contributions, and known-result boundaries.
- [Working-paper draft](notes/working-paper-kinetic-defects.md): the common model, principal transport and design results, proof outlines, and literature boundaries.
- [Companion draft](notes/working-paper-uncertain-mobility.md): uncertain kinetic patterns, optimal moments, measurement resolution, and finite bulk transport.
- [Closing report](notes/final-research-report.md): strongest contributions, verification, and remaining limits.
- [Research log](notes/research-log.md): decisions, current work, and evidence status.
- [Numerical verification](notes/numerical-verification.md): reproducible checks and their limits.
- [Surface-exchange prior art](notes/singular-exchange-prior-art.md): known ingredients, candidate advance, and access gaps.
- [Degenerate surface mobility](notes/degenerate-surface-mobility.md): when surface motion fails to restore finite dispersion.
- [Traveling channels](notes/exploration-soft.md): verified physical corollaries and an inverse-transport nonuniqueness construction.
- `notes/`: derivations, literature comparisons, and independent reviews.
- `scripts/`: reproducible mathematical and numerical checks.
- `results/`: generated verification output.
- `literature/`: pre-existing local knowledge base, excluded from Git. Its contents have their own instructions and citation conventions.

Development stopped at the user's request after the current results were checked and documented. Explicitly labeled conjectures are not counted as verified results.
