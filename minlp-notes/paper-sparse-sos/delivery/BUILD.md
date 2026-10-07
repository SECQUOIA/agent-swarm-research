# Build the manuscript

The source archive is self-contained. It requires a LaTeX installation with
pdfLaTeX, BibTeX, latexmk, and the packages named in `macros.tex`.

Run from the extracted source directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The resulting manuscript is `main.pdf`. No experiment, optimization solver,
network access, or files from the research repository are needed to build it.
An optional source consistency check uses Python 3.10 or newer:

```sh
python3 verification/check_sources.py
```

The author field is intentionally empty. Internal proof reviews and working
notes are not part of the submission source archive.
