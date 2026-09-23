# Stage 2, round 2 — correction

Date: 2026-09-17. Implemented the sole accepted minor finding in `stage2-r2-adjudication.md` (overlapping R1/R2/R4/R5).

The closing paragraph of `sections/02-cyclic-oxides.tex` now closes a persistent concurrent-over-delayed benefit claim only when the uncertainty interval for the predeclared direct wet P-minus-R contrast excludes a consequential advantage. The Dsteam interval assesses whether steam modifies that benefit. Individual arm recovery bounds remain separate conclusions; they cannot substitute for the direct comparison. Updated `evidence/stage2-cyclic.md` to record this distinction.

No experiment, numerical result, source claim, or other chapter was changed. No further reviewer round is required by the adjudication.

Validation: `latexmk -pdf -interaction=nonstopmode -halt-on-error -cd manuscript/main.tex` passed and produced a 16-page PDF. Final LaTeX/BibTeX logs have no warnings, errors, undefined references/citations, or overfull/underfull boxes. The water source SHA-256 remains `34792454be1aa5930c992591ba95390a898726d0620dc8effbeee92d622f7a3c`.

Ready for parent verification and Stage 2 closure.
