# Standalone manuscript source

This archive contains the anonymous manuscript, its bibliography, all table
sources, and its vector figure as TikZ source. No computational code is needed
to build the paper. Author and affiliation fields are intentionally empty.

From this directory, use TeX Live with pdfLaTeX, BibTeX, latexmk, and the packages
loaded by `main.tex` (including Latin Modern, TikZ, natbib, and cleveref):

```sh
sha256sum -c MANIFEST.sha256
SOURCE_DATE_EPOCH=946684800 FORCE_SOURCE_DATE=1 latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The result is `main.pdf`. The delivery build used TeX Live 2023/Debian and
latexmk 4.83. Fixed build time and suppressed PDF dates and identifiers make
repeated builds byte-identical with the same TeX environment; a different TeX
distribution or font version can change PDF bytes. The manifest covers the
archive's input files, excluding the manifest itself and subsequent build output.

The separate computational supplement supplies the runnable implementations,
independent checks, raw measurements, and table generator. The supplied table
files reproduce the reported measurements; the manuscript does not claim that
timings are portable between machines.
