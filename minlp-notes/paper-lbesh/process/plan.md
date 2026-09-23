# Paper development and review plan

Task: produce a standalone, submission-ready anonymous LaTeX manuscript on logic-based extended supporting hyperplanes for convex GDP, with a complete topic-specific evidence package. Preserve existing research sources and frozen experiments unless a verified defect requires an explicitly documented correction.

## Stages

1. **Contribution and literature.** Establish the exact research question, complete the source and development inventory, verify related work, and write the introduction and related work in a compilable manuscript scaffold.
2. **Mathematics and algorithm.** Write self-contained model definitions, algorithm, conditional convergence and residual results, counterexamples, representation diagnostic theory, and implementation contracts. Resolve any mathematical gaps found in independent review.
3. **Computational evidence.** Write the full reproducible study, generator and reference constructions, empirical diagnostic, ablations and follow-ups. Derive manuscript tables and figures from preserved records and verify all numerical claims.
4. **Complete manuscript and standalone package.** Integrate abstract, discussion, conclusions, appendices and reproducibility materials; improve exposition and verify relocated paper/source/supplement builds.
5. **Full-manuscript acceptance review.** An integration author checks the complete submission; five independent reviewers examine correctness, contribution, completeness, evidence and readability. Complete all valid corrections and repeat the five-reviewer cycle whenever major issues occur.

## Required cycle for every stage

- A designated author subagent completes the bounded stage before reviews begin.
- Five reviewers independently inspect the completed stage. They do not read other current reviewers' reports before submitting their own. Reviewers write separate reports and do not edit manuscript sources.
- The lead assesses every criticism, records its disposition and severity, and sends all valid major and minor findings to a different correction subagent.
- If any accepted major finding occurs, five independent reviewers review the corrected stage again. The next stage begins only after a round has no major findings and all accepted minor findings are corrected.
- Stage snapshots or source fingerprints and all actual targeted verification commands/results are retained. No project-wide checks or CI inspection are used.

## Scientific boundaries

The established cut family is perspective outer approximation. The intended original contribution is a controlled computational and methodological study of radial versus point separation in an NLP-assisted GDP implementation. No claim of a new cut family, general cut dominance, universal solver superiority, exact numerical certification, or an effective separation-only implementation is presumed. The residual-calibrated fractional theorem must be distinguished from the fixed-cutoff implementation. Mathematical results, numerical evidence, and scientific interpretation must remain consistent.

Authorship, affiliation, funding and a public data DOI will not be invented. The manuscript can be ready for anonymous review without journal-specific formatting or fabricated administrative declarations.
