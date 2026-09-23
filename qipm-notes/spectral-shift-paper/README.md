# The Quantum Cost of Unit-Normalized Spectral Shifting

This directory contains an anonymous, standalone research manuscript. Its
main output is `main.pdf`; `submission-source.zip` contains the portable
submission sources. The paper proves query bounds for applying a coherent
unit-normalized complement conversion circuit. It does not claim bounds on
classical phase computation, finite-precision synthesis, or an entire LP solver.

## Build the paper

With a standard TeX distribution containing pdfLaTeX, BibTeX, Latin Modern,
AMS packages, mathtools, booktabs, microtype, geometry, natbib, graphicx, and
hyperref, run:

```sh
make
```

The required figure PDF is included, so this build needs no Python packages
and no network. The generated `main.bbl` is also included for submission
systems that do not run BibTeX. To build directly using it, run pdfLaTeX on
`main.tex` twice. The Makefile otherwise refreshes the bibliography and
resolves cross-references automatically. `make clean` removes ordinary build
outputs but retains the supplied bibliography and figures.

## Reproduce the figures

Use Python 3.12 with NumPy, SciPy, and Matplotlib:

```sh
make figures PYTHON=python3
make
```

Individual commands (also usable from a different working directory with
an appropriate script path) are:

```sh
python3 scripts/query_overview.py
python3 scripts/joint_accuracy_diagnostics.py
```

`query_overview.py` writes `figures/query-overview.pdf`, a PNG preview, and a
CSV of thresholds. It uses the shared stationary-equation solver from
`joint_accuracy_diagnostics.py`. The figure shows exact proved exponent
ranges; numerical values only place the thresholds on its horizontal axis.
In particular, it does not label a degree-six witness error as the exact
even threshold F3.

`joint_accuracy_diagnostics.py` writes threshold/asymptotic and pinned-kernel
CSV data, a PDF, and a PNG under `figures/stage2-diagnostics/`. These are
supplementary diagnostics and are not required for the manuscript build.
They use floating-point arithmetic. Neither script certifies positivity or
contractivity from a mesh; the continuous-domain proofs are in the paper.
No random seed is needed because these computations are deterministic.

Validated versions: Python 3.12.14, NumPy 2.5.2, SciPy 1.18.0, Matplotlib
3.11.1; pdfTeX 1.40.25 and BibTeX 0.99d (TeX Live 2023/Debian). The scripts
use standard APIs and do not require these exact versions.

In the development workspace, all scripts and builds use the `qipm` conda
environment:

```sh
conda run -n qipm --live-stream make figures
conda run -n qipm --live-stream make
conda run -n qipm --live-stream make submission
```

## Submission package

Run `make submission PYTHON=python3`. The archive includes the manuscript,
macros, sections, bibliography database, generated bibliography, required PDF
figure, scripts, this README, and Makefile. It excludes audit records, logs,
local literature, previews, and intermediate build products. Extract it into
an empty directory and run `make` to build independently of the repository.

The theorem proofs are self-contained apart from explicitly cited standard
implementation and approximation results. The repository's `audit/` records
the development and source-coverage checks; it is not needed to read or build
the paper and is not part of the submission archive.
