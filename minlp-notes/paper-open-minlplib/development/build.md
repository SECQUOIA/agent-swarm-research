# Building the paper and the supplement

Run in `paper-open-minlplib/`:

```bash
make
```

This builds `build/main.pdf` (the paper) and `build/supplement.pdf` (the
supplementary material) with all references resolved, in both directions.
`make clean` removes the generated files (`latexmk -C`).

## What the command does

- Each document reads the other's `.aux` file through xr-hyper
  (`\externaldocument` in `main.tex` and `supplement.tex`), so `\cref`
  works across the two PDFs. `make` runs `latexmk main.tex supplement.tex`
  twice. The first pass writes both `.aux` files; in the second, latexmk
  reruns each document whose inputs changed. No document prints a page
  number of the other, so two passes suffice. A plain `latexmk` builds both
  documents too (`latexmkrc` lists them), but only one pass.
- `latexmkrc`: pdflatex, all output in `build/`. BibTeX runs separately
  for each document; both use `references.bib` with style `plainnat`.
- Links from one PDF to the other are relative (`supplement.pdf` and
  `main.pdf` in the same folder). They only work while the two files keep
  these names; the printed references do not depend on them.

## How the two documents are set up

- `preamble.tex` loads the packages (xr-hyper before hyperref) and
  `macros.tex`; both documents input it.
- `main.tex`: sections 00-11, bibliography, `\appendix`, then
  `A-semantics.tex` and `G-proofs-split.tex` (printed as Appendices A and
  B).
- `supplement.tex`: title "Supplementary material for: ...", a one-line
  note on S numbers, a table of contents, then `B0-families` (with B1-B9 as
  S1.1-S1.9), `C-points`, `D-literature`, `E-audit`, `F-eg-rounding`,
  `H-solvers`, `I-reproduction`, `J-displays` (Sections S1-S8), and its own
  bibliography.
- Supplement numbers carry the prefix S: Section S3, Theorem S3.2 (theorem
  environments are numbered within sections), equation (S4), Table S5,
  Figure S1. `\cref` prints the same forms in the main paper.
- Three small fixes for the cross-document setup, each commented where it
  is made:
  - `preamble.tex` redefines `\cref@getref`, because xr-hyper appends the
    other PDF's file name to imported cleveref records ("Section
    S3supplement.pdf"). Do not use `\cpageref` across documents.
  - `supplement.tex` resets its section, equation, table and figure
    counters by `part` (set to 99), so that cleveref never joins numbers of
    the two documents into one range ("Sections 1 to S2") and lists the
    paper's objects first in a mixed `\cref` list.
  - `supplement.tex` starts the counter of the `rotating` package at 100,
    because each sideways table writes a label `RF<n>` and the two
    documents' labels would otherwise clash.

## Checks after a build

```bash
grep -a 'undefined\|multiply defined' build/main.log build/supplement.log
grep -a 'LaTeX Warning: TODO\|archive DOI' build/main.log build/supplement.log
pdftotext build/main.pdf - | grep -c '??'
pdftotext build/supplement.pdf - | grep -c '??'
```

The first and the last two commands should print nothing or 0 (after
`make`; a single `latexmk` pass from a clean `build/` leaves the paper's
references to the supplement undefined).

## Float check

LaTeX gives no warning when a sideways table runs off the page, and
`pdftotext` does not reliably extract rotated captions (round-1 review: Table 2
and Table S42 were clipped without a warning). After every build:

```bash
python3 development/check_floats.py
```

It renders every page of both PDFs at 40 dpi, reports each page with ink
closer than 10 mm to an edge of the paper, and checks that `pdftotext` of the
main PDF contains all 31 closure names; it exits with status 1 otherwise. Then
render and inspect by eye every page with a sideways table or a longtable
(main: Tables 1 and 2; supplement: the sideways tables of S1, S4 and S6, and
the longtables), for example with

```bash
pdftoppm -r 40 -f <page> -l <page> -png build/supplement.pdf /tmp/page
```

Fix any clipping in the generator of the table (`data/make_tables.py`,
`make_campaign_table.py`, `make_points_table.py`), never in the generated file.
