# Stage 1 author report — current manuscript

Completed 2026-09-13. Scope: introduction, precise model/checking contract, primary-literature positioning, and reconciliation of topic inventory. No checker code or other paper folder was changed.

## Changes

- Rewrote the contribution around the actual integration and reliability findings. Removed the earlier qualified absence/priority sentence: the evidence supports exact semantics + rigorous cuts + master identity + rational replay as the concrete contribution, without proving priority for the combination.
- Replaced stale open-blocker inventory with the repaired current state, explicitly mapping both reproduced upstream checker defects, twelve exact proof failures, exact-expression/domain repairs, half-lines/free coordinates, source-model equivalence and invalid returned points, producer/checker dependencies, frozen replay, and exact primal witnesses.
- Set current historical totals to 188 verified, 92 rejected, nine missing, all 289 accounted for; 269 is identified only as historical acceptance.
- Made the box-domain contract explicit. Functions are finite/convex on the declared box; normalization of nonlinear row direction, loaded binary64 leaf semantics, pre-extraction rewrites, trusted model execution, singular derivatives, master constants/sense, and checked primal upper bounds are explicit.
- Clarified the distinction between complete replay, partial checking, and proof-assistant coverage. No new formalization is claimed at this stage.
- Cleaned combined journal/volume/page BibTeX fields into conventional separate fields.

## Literature findings

Read local literature instructions, relevant existing review notes, the five requested current topic notes, checker README, curvature/domain implementation, and local Halbig extracted text. Rendered and visually checked Halbig `original.pdf` PDF page 18 (printed p.17): Algorithm 3 removes integrality and solves the continuous problem with the certificate-plane halfspace; Section 4.3 separately calls the linear (M)IP integer-freeness problem. Removed the temporary page image after inspection.

Online refresh identified Wood et al.'s published Journal of Symbolic Computation 135 (2026), 102543, DOI `10.1016/j.jsc.2025.102543`; the former 2025 preprint-only citation was stale. The open v4 scope separates the Why3 logical theorem from the executable translator. Added pinned CakeML VIPR software with restrained coverage description, and Szeider's July 2026 CP paper on black-box ILP VIPR construction (primary publisher abstract/metadata inspected). CakeML latest path-history API query was checked, but the citation deliberately points to the earlier immutable source actually inspected.

Sources and URLs are recorded in `evidence/literature-review.md`. No local literature packages, generated literature index/bibliography, user-supplied originals, or external projects were modified. No broad novelty claim remains.

## Validation

Built the two-section manuscript and bibliography using PDFLaTeX/BibTeX in `build/`. Initial latexmk picked up an old root bibliography; explicit `bibtex build/main` followed by two PDFLaTeX passes resolved the new citations. The final `build/main.log` has no undefined citations/references, LaTeX warnings, or overfull/underfull boxes. This is an initial-section build, not a claim that the full paper is complete. Routine code tests belong to root's independent current audit; no checker change required rerunning them here.

## Later-stage obligations

Develop and review detailed mathematical proofs, restricted proof-kernel rules, any actual Lean coverage, complete experimental section, and supplement packaging. Keep the exact source/format and trusted-library assumptions in later sections. If new experiments or source repairs alter results, update the introduction's fixed historical cohort only when justified; report new generation separately. No unresolved Stage 1 mathematical or literature issue was found that invalidates the scoped paper. Completion of later stages and five independent Stage 1 reviews remains required.
