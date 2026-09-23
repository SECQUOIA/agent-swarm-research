# Quadratic Aggregation: Certificates, Finite Descriptions, and Approximation

The standalone manuscript is `main.tex`. Its complete mathematical proofs
and references require no repository notes or external data. The final build
and source archive can be regenerated with the commands below.

Author names, affiliations, acknowledgments, and funding information were
not provided and are intentionally left for the authors to supply before
submission. No journal-specific template or permanent repository DOI is assumed.

## Build the paper and formal account

Install a LaTeX distribution with pdfLaTeX, BibTeX, latexmk, AMS packages,
Latin Modern, natbib, geometry, graphicx, microtype, xurl, and hyperref. Then run
from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/final main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/final formal-supplement.tex
```

The outputs are `build/final/main.pdf` and
`build/final/formal-supplement.pdf`. The generated `.bbl` files provide
complete typeset bibliographies. All five shorter `formal-*.tex` wrappers
can also be built with the same command. The supplied figure PDF allows
paper compilation without Python plotting dependencies.

## Reproduce the checks

The exact example scripts require Python 3 and its standard library:

```sh
python3 supplement/check_examples.py
python3 supplement/check_infinite_aggregation.py
python3 supplement/check_approximation.py
python3 supplement/check_four_aggregation.py
python3 supplement/check_three_dimensional_span.py
```

See [supplement/README.md](supplement/README.md) for the scope of each check
and the optional NumPy/Matplotlib command to regenerate the figure. These
scripts do not replace the general proofs.

See [FORMAL-VERIFICATION.md](FORMAL-VERIFICATION.md) for the exact Lean
coverage and [the portable project's instructions](supplement/lean/README.md)
for dependency installation and `python3 verify.py`. Lean is optional for
building or reading the paper. Its source package is self-contained apart
from explicitly pinned public dependencies.

## Create the submission source archive

After both final builds, run:

```sh
python3 package_submission.py
```

This creates `dist/quadratic-aggregation-source.zip`, a sorted source
manifest with SHA256 hashes, and convenient `paper.pdf` and
`formal-supplement.pdf` copies. The archive includes the main paper, all
LaTeX sections and wrappers, bibliography and generated `.bbl` files,
figure PDF, reproducibility scripts, and portable Lean sources. Successful
portable Lean verification logs and its manifest, when present, are included
as verification evidence. Downloaded `.lake` dependencies, caches, historical
review/process records, and third-party literature PDFs are excluded.
The archive itself does not need the surrounding repository.

`PROCESS.md` and `process/` record the development and independent review
workflow for this repository. They are not part of the submission source
archive and are not claims of external journal peer review.
