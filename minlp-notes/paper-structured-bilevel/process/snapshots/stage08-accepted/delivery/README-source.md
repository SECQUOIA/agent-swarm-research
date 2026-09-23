# LaTeX source

This is the complete source of *Structured bilevel optimization with many
follower variables: Global responses, accuracy, and structural boundaries*.
The author field is blank.

From this directory, build with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The output is `build/main.pdf`. Requirements are a standard TeX Live installation
with pdfLaTeX, BibTeX and latexmk. No shell escape or surrounding repository is
needed. The source includes all seven sections, four appendices, bibliography,
figure and three table inputs. The tables are already generated; Python is not
needed to build the manuscript.

`SHA256.json` records the SHA-256 of every supplied file except itself. The
separate computational supplement contains the reproducible code and data.
