# Stage 2 revision record

Date: 2026-09-07. Revision agent: `paper_revision_agent`, separate from the stage author and the five independent reviewers.

All corrections and reader aids accepted in `reviews/stage2-round1/assessment.md` are implemented. No accepted issue remains unresolved. At this revision handoff, coordinator verification and stage 2 acceptance were pending. The coordinator subsequently accepted stage 2; see `WORKFLOW.md` and `stage2-accepted-snapshot.json`.

## Accepted corrections

| ID | Location | Change |
|---|---|---|
| S2-A1 | `sections/log-limits.tex`, paragraph after Theorem 4.4 (`thm:log-limits`) | Replace the unqualified log-lattice claim with the distinction between the equal-split pure-fragmentation reference and the nonlinear law. For monodisperse initial size `x0`, the reference stays on `log(x0)+(log 2)Z`; coagulation need not preserve that lattice. The nonlinear size law remains atomic on positive dyadic rational multiples of `x0`, a countable set closed under addition and halving. The limitation on inferring density convergence remains explicit. |
| S2-A2 | `sections/log-limits.tex`, after the Poisson-reference definition | State the sufficient stationary-increment condition of constant fragmentation rate and fixed fraction law. Explicitly allow stationary zero increments when the fragmentation rate vanishes almost everywhere, regardless of the unused fraction law, and note that changes on null time sets do not affect the reference law. |

## Accepted reader aids

- Identify the jump-count compensator at its first use in `sections/auxiliary-process.tex` as the integrated conditional jump rate, with the stopped expectation relation used by the proof.
- Define `D([0,S],R)` as right-continuous real paths with left limits, and explain that the `J1` topology permits small changes in jump times through continuous increasing time changes.
- Replace the Billingsley Chapter 2 locator with Theorem 8.2, as verified in the source review.

## Historical source corrections

At the coordinator's additional request, corrected the same unqualified lattice statement in `research/results/log-size-poisson-limit.md` and `research/reviews/log-size-poisson-proof.md` (paths relative to the repository root). Both now distinguish the reference lattice from the nonlinear atomic support and retain the no-density conclusion. The older review includes an explicit amendment dated 2026-09-07 so that the correction is not represented as part of its original review. No other research file was changed by this revision.

## Build and status

The isolated readability review found that one additional PDFLaTeX pass was needed to remove the final label-rerun warning. The Makefile now runs three PDFLaTeX passes after BibTeX, and `main.pdf` depends on the Makefile so changes to the build recipe trigger rebuilding. This retains the existing tools and resolves the observed reference-pass issue.

- Ran `make clean`, followed by `make -B`, rebuilding without auxiliary files. The command completed successfully and produced a 19-page `main.pdf` (407,661 bytes). Transcript: `/tmp/ramki-stage2-revision-build.log`.
- Checked the final `main.log` and `main.blg`: no warnings, unresolved references or citations, LaTeX errors, or overfull or underfull boxes.
- Used `pdfinfo` and `pdftotext -layout` to verify the artifact and inspect the revised passages. Extracted PDF text contains no unresolved-reference placeholders.
- Verified hashes against the stage 2 review snapshot: `main.tex`, `references.bib`, and all three accepted stage 1 mathematical source files are unchanged.
- Updated README, author status, and coverage records to report completed reviews and corrections, with coordinator verification pending. The stage 2 reviewer reports, assessment, and review snapshot are unchanged. No later-stage content or new result was added.

No second five-reviewer round was run; the coordinator assessment calls for verification of these minor corrections before the next stage.
