# Build and numerical reproducibility record

## Stage 0 scaffold, 2026-09-07

Author ran, from `paper-uncertain-mobility/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
pdftotext main.pdf -
```

Build succeeded with latexmk 4.83 and pdfTeX 3.141592653-2.6-1.40.25 (TeX Live 2023/Debian), producing one-page `main.pdf`. The initial outline-rerun notice was resolved by latexmk's second pass. The final log contained no unresolved-reference or citation warning. Text extraction confirmed the title, date, and explicit scaffold status. This is not a full visual inspection or final manuscript build.

No numerical claim or figure is included in the scaffold. Numerical reproducibility and final PDF inspection remain mandatory Stage 7 and final-audit work, with exact commands and tool versions to be recorded here when performed.

## Stage 07 assembled draft, 2026-09-07

The complete numerical command was run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python paper-uncertain-mobility/numerics/reproduce.py
```

It generated the circle trial/refinement data, 9 center optimizations, independent parameter re-evaluations, two vector PDF figures and numerical table rows. After the figure layout was enlarged for readability, `python numerics/reproduce.py --plots` regenerated artifacts from the saved data. Numerical versions: Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, Matplotlib 3.11.1. The data include optimizer feasibility, statuses and tangent gaps. See [the Stage 07 handoff](stage-07/author-handoff.md) for the exact meaning and limits of these checks.

From the manuscript directory, the final author build was:

```sh
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

It succeeds with 54 pages, no unresolved references/citations and no LaTeX warnings or overfull/underfull boxes, using the same TeX toolchain as Stage 0. Explicit source scans find no control-byte or trailing-whitespace issue. The author visually inspected front matter, numerical figures/tables and references, and enlarged the three-panel figure after inspection. All-page inspection and the complete five-reviewer manuscript audit remain coordinator tasks after Stage 07 acceptance; this is an author build record, not final acceptance.

## Final-review corrections: clean build, 2026-09-07

After the five independent whole-manuscript reports and coordinator adjudication, the separate fixer corrected the accepted minor issue groups, including the coordinator’s positive-mass case-label clarification. From the manuscript directory, the fixer removed the existing build artifacts and rebuilt with:

```sh
latexmk -C main.tex
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

The clean LaTeX/BibTeX build succeeded and produced a 54-page PDF. The final log has no unresolved references or citations, LaTeX warnings, or overfull/underfull boxes. The toolchain remains latexmk 4.83 and pdfTeX 3.141592653-2.6-1.40.25 (TeX Live 2023/Debian). Numerical code, stored data, and figure PDFs were unchanged; no numerical recomputation was needed for these wording and notation corrections.

Direct source scans and frozen-manifest comparisons are recorded in [the final correction record](final/round-01/corrections.md). The rebuilt PDF SHA-256 is `260be943f47f06955b4b78c6baa158ebbe44394009b008ea3c4c96cb0eef2dd3`. Coordinator inspection of the affected pages and the final acceptance decision are separate from this build record; consult the [review ledger](README.md).

## Coordinator final verification and acceptance, 2026-09-07

The coordinator verified the corrected source hashes, the clean final build log and the 54-page PDF hash `260be943f47f06955b4b78c6baa158ebbe44394009b008ea3c4c96cb0eef2dd3`. The exact clean-build commands and toolchain are recorded immediately above. No numerical input or generated figure/table changed during final corrections, so the documented numerical reproduction and independent certificates remain applicable.

All 54 pages have now been visually inspected. A complete final rerender at 72 dpi differed from the inspected review version only on pages 2, 20, 30, 52; these four pages were inspected separately and passed. The remaining 50 pages were pixel-identical. All valid final-review findings have been corrected and verified. The [final acceptance](final/acceptance.md) identifies accepted source snapshot `26b6cdc95672f565c1a5071fdb735622e3c99136f2596daed8727917ee0c88fb` and the preserved five-reviewer/correction record.
