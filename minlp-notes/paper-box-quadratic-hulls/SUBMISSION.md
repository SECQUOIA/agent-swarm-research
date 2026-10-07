# Manuscript sources

**Title:** Quadratic hulls on boxes: valid inequalities and semidefinite
representability

This is the anonymous source package for the complete manuscript. The main
text and all proof appendices are included in `main.tex`. No files from
the research repository or local literature library are needed to typeset it.

Build with a standard TeX installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The package includes the verified bibliography in `references.bib` and the
generated `main.bbl`. For a build without BibTeX, run `pdflatex main.tex`
twice using the supplied `main.bbl`. Authors and a date are intentionally
omitted.

The contact diagram is supplied as a vector PDF. Its optional Python
generator uses Matplotlib and NumPy; running it is not required to typeset
the manuscript.

The numerical companion is distributed separately as `companion.zip`. Its
record inspector checks archived tables and source hashes without solving
optimization models. The manuscript describes the scope and limitations of
the archived experiments and separates their numerical results from exact
mathematical certificates.
