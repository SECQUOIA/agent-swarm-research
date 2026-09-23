# Designing surface transport under uncertain kinetics

This folder contains the completed LaTeX manuscript and reproducible numerical evidence for the repository's uncertainty and measurement paper. It has undergone staged independent review and a separate five-reviewer whole-manuscript audit. The [review ledger](reviews/README.md) records coordinator decisions and accepted snapshots; the [final adjudication](reviews/final/round-01/adjudication.md) records the whole-manuscript findings.

The paper proves sharp predetermined mobility moment laws, generic-fold orders, an exact local placement profile, the exact-observation mean, and the finite-precision crossover. The previously open supercritical coefficient and intermediate-resolution limit are resolved through attained whole-line variational problems. No elementary formula or uniqueness is asserted for those minimizing densities. The physical interpretation uses fixed positive bulk diffusivity, constant affinity, nonzero mean flow, and the explicit assumptions in the manuscript.

## Build the paper

From this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

The entry point is [main.tex](main.tex), and the built paper is [main.pdf](main.pdf). TeX Live with pdfLaTeX, latexmk, BibTeX, and the packages in `preamble.tex` is required. All figure PDFs and generated table rows are included, so compiling LaTeX does not require numerical optimization. The recorded build uses latexmk 4.83 and pdfTeX 3.141592653-2.6-1.40.25 (TeX Live 2023/Debian).

## Reproduce numerical evidence

From this directory, inside the parent repository:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python numerics/reproduce.py
```

The script resolves paths from its own location, so it can also run from the repository root as `python paper-uncertain-mobility/numerics/reproduce.py`. It requires NumPy, SciPy, and Matplotlib. Exact versions for the stored computation are in `data/numerical-evidence.json`; the build record also records them. No package installation is performed by the script. The imports from the parent repository are `scripts/check_robust_design.py` (tridiagonal solver and explicit observed trial) and `scripts/check_risk_sensitive_design.py` (graded trial construction). These files are required to rerun the numerical driver, but not to compile or follow the paper's proofs.

To regenerate figures and table rows from stored data without rerunning solves:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python numerics/reproduce.py --plots
```

The driver writes `data/numerical-evidence.json`, `data/mean-table.tex`, `data/center-table.tex`, and the two PDF figures. Circle results evaluate trials, not finite-budget optima. Every sampled field has the same discrete mobility mass. The uncertain-center calculation minimizes a finite-domain, finite-volume, finite-quadrature objective; its tangent gap bounds that discrete objective only, with floating-point arithmetic. Separate spatial, parameter-quadrature, and domain checks are recorded. A deliberately underresolved quadrature example is retained. No numerical approximation to the new supercritical variational constant or full global crossover is presented as a proved value.

## Sources and audit records

- `sections/`: introduction, the six mathematical developments, numerical evidence, and discussion.
- `references.bib`: manually curated manuscript bibliography; distinct from the generated literature knowledge base.
- `figures/` and `data/`: generated artifacts with provenance in `numerics/reproduce.py`.
- [PLAN.md](PLAN.md), [claims-map.md](claims-map.md), and [notation.md](notation.md): scope, dependencies, and notation.
- `reviews/`: author handoffs, five independent reviews at each stage, adjudications, separate corrections, and acceptance manifests.
- [Stage 07 literature audit](reviews/stage-07/literature-audit.md): inspected primary sources, comparison scope, access limits, and current search record.

The paper includes every proof it needs; unpublished repository notes are historical leads, not mathematical prerequisites. No author identity, affiliation, journal submission, experimental validation, or publication status has been inferred. The blank LaTeX author field is intentional. The independent review and correction records are included with the manuscript.
