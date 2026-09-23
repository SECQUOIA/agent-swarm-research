# Catalysis research portfolio

Read [main.pdf](main.pdf) for the complete manuscript. It recommends four main programs, followed by a concise shortlist. The text distinguishes published observations, calculations using published data, and proposed experiments. It reports no new experimental measurements.

The source entry point is [main.tex](main.tex). All section inputs are mandatory, so a missing chapter fails the build.

| Order | Source | Focus |
|---|---|---|
| Overview | [00-introduction.tex](sections/00-introduction.tex) | Ranked recommendation, selection rationale and evidence scope |
| 1 | [01-water.tex](sections/01-water.tex) | Physical water management in Fischer–Tropsch catalysis |
| 2 | [02-cyclic-oxides.tex](sections/02-cyclic-oxides.tex) | Steam compatibility and recovery of selective oxygen delivery |
| 3 | [03-polymer.tex](sections/03-polymer.tex) | Fresh catalyst demand during polymer ethenolysis |
| 4 | [04-silver.tex](sections/04-silver.tex) | Ni-dependent useful output on promoted Ag |
| Shortlist | [05-shortlist.tex](sections/05-shortlist.tex) | Six reserves and withdrawn claims |

## Build

From this directory, with TeX Live, pdfLaTeX, BibTeX and the packages loaded in `main.tex`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Without latexmk:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The selected bibliography in [references.bib](references.bib) is self-contained. Building does not require the local literature library, network access, or copied source publications. The compiled `main.pdf` is retained; auxiliary build files are ignored.

## Evidence and reviews

[Evidence notes](evidence/) record exact primary-source locations, access limits, checked calculations and design decisions for each stage. [The water-output calculation](evidence/check_water_output.py) can be rerun with Python using its accompanying source-series data. Notes document what was checked; they do not imply that unpublished data or every source supplement was available.

[Review records](reviews/) contain the independent stage and manuscript reviews and corrections. [process.md](reviews/process.md) records the current stage status and findings disposition. These supporting records are separate from the scientific narrative.
