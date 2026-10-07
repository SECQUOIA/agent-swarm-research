# The Cost of Following the Central Path

Standalone LaTeX research manuscript. The paper studies
central paths and shortest accurate routes in specified barrier Hessian
metrics, finite bounded-movement sequences, barrier dependence, and the
additional cost of a feasible primal–dual completion.

- `main.pdf`: compiled manuscript.
- `main.tex`, `macros.tex`, `sections/`, `bibliography.bib`: complete manuscript sources.
- `figures/`: vector PDF figures used by the manuscript.
- `scripts/`: exact certificate, numerical diagnostics, and figure generation.
- `data/dyadic-lengths.csv`: numerical values underlying the three-length figure.
- `audit/`: development provenance, literature review, and independent review reports;
  these files are not manuscript build inputs.

## Build

From this directory, with a TeX distribution providing PDFLaTeX, BibTeX,
latexmk, and the packages listed in `macros.tex`:

```sh
make
```

Equivalently:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The included figures allow the PDF to build without Python. Copying this
folder is sufficient: the manuscript has no build dependency on other
repository folders or on local literature files. `make clean` removes
auxiliary TeX files and retains the PDF.

In the development repository, run tools in its required environment:

```sh
conda run -n qipm --live-stream make
```

## Reproduce certificates, diagnostics, and figures

Use Python 3 with NumPy, SciPy, and Matplotlib already available. The
rational certificate itself uses only the Python standard library.
There is no package installation or network access in these commands.

```sh
python scripts/verify_scalar_certificate.py
python scripts/verify_standard_geometry.py
python scripts/verify_barrier_dependence.py
python scripts/verify_primal_dual_formulations.py
python scripts/make_figures.py
```

Alternatively run `make verify` or `make figures`, with `PYTHON` set to
the desired interpreter. The repository interpreter is
`/workspace/local-home/miniconda3/envs/qipm/bin/python`.

The scalar certificate verifies the appendix's finite rational
inequalities using exact `Fraction` arithmetic; its bounds accompany the
analytic proof. The other scripts are numerical diagnostics of identities,
inequalities and independently solved central equations. They do not
establish global mathematical claims by sampling. Seeds are fixed where
random samples are used.

`make_figures.py` constructs the dyadic exponents by exact rational
summation and integer flooring. It evaluates transformed coordinates
without rounding the physical coordinates to the boundary, checks this
formula against independent integration and finite differences, and
integrates central speed separately between activation thresholds.
The CSV reports the adaptive quadrature error estimate, not a rigorous
error enclosure. The plot distinguishes finite-start endpoint distance
from distance to an entire accurate target set. Rebuilding figures can
slightly change floating-point values across library versions; it does
not change the theorems.

## Scope

The proved resource is bounded starting-local-norm movement. A shorter
route does not by itself establish a faster arithmetic or oracle
algorithm. Novelty statements distinguish the exact comparisons and
explicit constructions from classical spectral calculus, Lorentz norm
inequalities, canonical barriers, and primal–dual gap-set geometry.
Primary sources are cited in the paper; no licensed literature originals
are redistributed here.
