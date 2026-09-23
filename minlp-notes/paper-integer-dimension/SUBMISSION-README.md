# Integer Dimension in Convex Mixed-Integer Approximation of Nonlinear Graphs

This source package uses the standard LaTeX `article` class and BibTeX; no
journal template is required. The author and date fields are intentionally
blank, as requested.

Build from the package root with a standard TeX Live installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The resulting PDF is `build/main.pdf`. The package contains `main.tex`,
`macros.tex`, `abstract.tex`, `references.bib`, and all files in `sections/`.
All proofs and formulation constructions are in these sources; the manuscript
does not depend on unpublished repository result files. The bibliography
identifies the primary literature and specifies manuscript versions where
technical locators differ from the published version.

The repository's optional verification scripts and review records are separate
from the submission sources. Those scripts supplement the mathematical proofs;
no script or repository checkout is required to compile or read this paper.
