# Independent review: Stage 00, round 01, reviewer 5

Reviewer: `paper_reviewer_5`. Date: 2026-09-07.

**Verdict: accept this preparation stage. No major or minor defects found within its stated scope.** This verdict does not accept any candidate theorem or certify the novelty of later mathematical results.

## Scope and independence

I read `PLAN.md`, `claims-map.md`, `notation.md`, `README.md`, all three LaTeX source files, the review-ledger instructions, all three review templates, the Stage 00 author handoff, and the build record. I compared the scope against `notes/working-paper-uncertain-mobility.md`, treating its historical review labels as untrusted. I did not read the other reports in this round or coordinate findings with their authors.

Principal reviewed source hashes (SHA-256):

| File | Hash |
|---|---|
| `PLAN.md` | `943457d6888a441c054a0e23b5c3dc69ac0bc6262e71387dc1cf9aca81cdb14a` |
| `claims-map.md` | `aae5c9883aa3de7c81b5a916a76f9c9ea7634ce3ddc93a39597f7663fa8342f6` |
| `notation.md` | `6fbcb755c8306fa62f40554696864fe766268b6115d661d3f98be1c9f2d1739b` |
| `main.tex` | `11f0cd99bd54159fbceec18943ecb3abbf2a5e33c72ff46782189dcc135b5c13` |
| `preamble.tex` | `69757a0786a132d9f837548aadfe1bd55e7503acb870508d66234e2d74e54572` |
| `sections/00-status.tex` | `14fae1d9eaf46dfdae00c2722feed48b67f24a5d25f358c3586bdac2260702c2` |

## Checks performed

1. **User workflow.** The plan requires one author, five independent reports, coordinator adjudication of every issue, a different correction agent, and a repeated five-reviewer round whenever valid major issues occur. Remaining minor issues must be fixed before the next stage. The final complete-draft review repeats this process and assesses the assembled paper. Snapshot tracking and reopening invalidated dependencies make the process auditable. These provisions faithfully implement the requested sequence.

2. **Topic coverage and reader dependencies.** The inventory includes the baseline random response, optimized moment regimes, critical constant, generic folds, exact observation, finite precision, finite-bulk transfer, numerical counterexamples, and relevant negative examples. The deterministic quadratic placement result is included where needed rather than left as a prerequisite in an unwritten companion paper. The exclusions concern separate transport questions and do not remove a necessary argument from the uncertainty paper.

3. **Proof-audit coverage.** The planned work explicitly addresses the main hazards visible in the source draft: arbitrary integrable designs rather than fixed smooth shapes; whole-line constant sources outside ordinary L²; unbounded coefficients and vanishing mobility; uniformity near merging roots; measurable observation policies; the distinction between an inverse identity and an extended lower bound; physical dispersion versus a functional defined by fiat; and constants versus order estimates. In particular, the sharp supercritical constant and interior measurement crossover remain marked as unfinished investigations. The preparation stage does not use historical verification labels to resolve them.

4. **Notation and units.** The ledger distinguishes the beta function from the physical prefactor, flow dispersion from molecular diffusion, exact-observation value from order notation, and unrooted moments from their roots. The physical scaling in the inventory is consistent: the integral mobility budget scales as a rate times length cubed, whereas the integrated inverse response scales as length divided by rate. The explicit warning that the physical prefactor alone does not dimensionalize a canonical coefficient prevents a material ambiguity in the source draft.

5. **Numerical reproducibility plan.** Stage 7 requires rerunning calculations actually used, grid and independent parameter-quadrature refinement, domain and tail specifications, lower certificates for optimization claims, and explicit separation of trials, discrete optima, and continuum values. The stage explicitly retains the finite-budget reversal of an asymptotically preferred shape. No absent numerical reproduction is a Stage 00 defect because the current PDF contains no numerical result.

6. **Independent build.** I first checked the documented build command, then performed a fresh build into a new temporary output directory using `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=<temporary directory> main.tex`. The fresh build exited with status 0 and produced a one-page PDF. Text extraction confirmed the title, date, and explicit scaffold status. This check is stronger than an up-to-date no-op build, but does not replace the final required visual inspection.

## Findings and limitations

There are no actionable findings in the present scaffold. The bibliography, theorem proofs, final reading order, actual figure provenance, and complete PDF inspection are explicitly assigned to later stages; their absence is appropriate here. The existing source results still require the fresh mathematical and literature checks identified by the plan. This report accepts the preparation and audit structure only.
