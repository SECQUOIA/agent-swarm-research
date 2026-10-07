# Building the manuscript

This archive contains the complete anonymous LaTeX manuscript and its
bibliography. It needs a standard TeX installation with `latexmk`, `pdflatex`,
and BibTeX; TeX Live 2023 or later is sufficient.

From the directory containing `main.tex`, run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The result is `main.pdf`. No repository checkout, source literature files,
computational results, external figures, network access, or custom LaTeX style
is required. The author and date fields are intentionally empty.

The source files are `main.tex`, `macros.tex`, `abstract.tex`,
`sections/01-introduction.tex` through `sections/07-discussion.tex`, and
`references.bib`.
