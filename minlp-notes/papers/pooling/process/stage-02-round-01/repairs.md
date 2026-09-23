# Stage 2, round 1: accepted minor repairs

Implemented the two corrections accepted in `adjudication.md`. The repaired section and bibliography are frozen for root inspection.

1. **R10-1:** In `bibliography.bib`, added `pages = {4:1--4:70}` to the AAM entry, changed its note to `ETR-INV locators refer to arXiv:1704.06969v4`, and changed its URL to `https://arxiv.org/abs/1704.06969v4`. Preserved its citation key, 2022 issue year, article number, DOI, and other metadata. Added the Toolbox note `Locators refer to arXiv:1912.08674v1` and changed its URL to `https://arxiv.org/abs/1912.08674v1`. All eight existing references remain; the other six entries are unchanged.
2. **R15-1:** In `sections/02-algebraic-complexity.tex`, replaced exactly three phrases: “the strict product constraint” with “the quality constraint at $j_1$”, “the lax product capacity” with “the capacity at $j_2$”, and “the strict quality condition” with “the quality condition at $j_1$”. No mathematical formula or proof step changed.

Validation completed:

- Compared the section and bibliography with `process/snapshots/stage-02-round-01.tex` and `process/snapshots/stage-02-round-01.bib`. The diff contains only the changes listed above.
- Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` successfully (exit 0). BibTeX and pdfLaTeX completed, producing the 22-page `main.pdf`; latexmk reports all targets up to date.
- Inspected the final `main.log` and `main.blg`: no LaTeX or BibTeX errors, warnings, undefined references/citations, or overfull/underfull boxes. BibTeX processed all eight entries and reports `warning$ -- 0`.
- Extracted text from PDF pages 21–22 and visually inspected both rendered pages. AAM displays `69(1):4:1–4:70, 2022`, the exact v4 URL and note; Toolbox displays the exact v1 URL and note. The bibliography is legible without clipping, and all eight references appear.
- The foundations SHA-256 before and after repair is identical. Accepted foundations were not edited. No later-stage work was performed.

Final SHA-256 hashes:

```text
8abd1d862cc58d23ee4671f2610c02ca04c27390353ba023b442325565514e67  sections/02-algebraic-complexity.tex
e471636f729e53603d572d17aba6fa7c41306a2aeba666995bb1650ec3c94b1e  bibliography.bib
be6256a4ad55a371cc280523072277ac682518ab3527cc82f496e78d17ea97bf  sections/01-foundations.tex
```
