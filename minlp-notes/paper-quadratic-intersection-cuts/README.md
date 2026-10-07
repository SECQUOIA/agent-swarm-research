# Limits and Guarantees for Quadratic Intersection Cuts

The manuscript develops the intersection-cut topic from the September and
October research notes. It includes the unrestricted corner benchmark,
bilinear determinant families, depth and conditioning guarantees, contact and
closure obstructions, homogeneous minors, successive cutting rounds, and the
retained computational evidence. The manuscript has no author line.

The main text explains the results and their relation to prior work. Six
appendices give technical proofs, rational witnesses, computer-assisted
certificate specifications, and experimental protocols. No optimization
experiment was rerun for this manuscript.

The [final verification record](verification/FINAL.md) lists the targeted
checks and delivery hashes. The [literature audit](evidence/literature-audit.md)
records the prior-work comparisons, inspected source versions, and access
limits.

## Files

- `paper.pdf`: compiled manuscript.
- `main.tex`, `macros.tex`, `sections/`, `appendices/`, `references.bib`:
  complete LaTeX sources.
- `delivery/quadratic-intersection-cuts-source.zip`: portable submission
  sources, including the compiled bibliography.
- `delivery/quadratic-intersection-cuts-companion.tar.gz`: retained certificate
  data, compact experimental records, original code, and a manifest checker.
- `companion/`: the unpacked electronic companion.
- `evidence/`: coverage, mathematical audits, literature review, independent
  manuscript reviews, and corrections. These working records are separate
  from the submission sources.
- `verification/`: targeted document checks and the final verification record.

## Build

From this directory, with a standard TeX Live installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The source archive preserves the same relative paths and also supplies
`main.bbl`. It needs no research-note file, literature folder, solver, or
machine-specific path to build.

Check the source graph, labels, and citations with:

```sh
python3 verification/check_document.py
```

The companion's manifest checker reads files and saved records. It does not
run a solver, regenerate certificates, or repeat computational experiments.
See its README for the distinction between complete saved certificates and
results whose retained evidence consists of exact-check receipts or numerical
records. Original provenance files may contain historical machine paths;
the manuscript and submission sources use relative paths.
