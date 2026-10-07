# Objective Sublevels and Central-Path Hessian Conditioning

`main.pdf` is the reading copy; `main.tex` and `sections/` are the standalone anonymous manuscript. The paper studies the equality-reduced primal barrier Hessian in a fixed external metric, including equal-gap comparison across barriers, matching geometric conditioning laws, exact SDP spectra, and Newton-forcing consequences.

Build the paper with a TeX installation providing `latexmk`, `pdflatex`, BibTeX, and the packages listed in `main.tex`:

```sh
make
```

All figures and tables are already supplied. To regenerate the numerical evidence, use Python with NumPy, SciPy, and Matplotlib:

```sh
make reproduce PYTHON=/path/to/python
make
```

In the repository's configured environment, the exact command is:

```sh
make reproduce PYTHON=/workspace/local-home/miniconda3/envs/qipm/bin/python
```

Reproduction requires no network access, no downloaded literature, no parent-repository imports, and no additional optimization package. It verifies exact rational certificates for the frozen benchmark representations and records all accepted and rejected numerical points. See [repro/README.md](repro/README.md) for the data definition, numerical contracts, and provenance. The manifest records the versions and hashes used for the supplied artifacts; small numerical differences on another BLAS implementation can change a threshold-based stopping iteration.

`submission-source.zip` is the portable submission source bundle; internal development and review records remain in the repository.

`development/` contains internal authoring and independent-review records. It is not part of the submission manuscript or required for reproduction. Author names, affiliations, and journal-specific submission metadata should be supplied by the submitting authors.

The exact fractional SDP log-barrier spectrum in Section 7 is formalized in
Lean in [`../formal/QipmFormal/FractionalSDP/`](../formal/QipmFormal/FractionalSDP/).
The [verification report](../formal/FRACTIONAL_SDP.md) maps the unique center,
actual Hessian and Frobenius metric, complete spectra, and leading asymptotic
constants to the proofs. It also records coverage of every sufficiently small
gap and central parameter. This does not formalize the section's
singularity-degree, diameter, or arbitrary-barrier claims. The manuscript
includes the rational parametrization used in the formal proof.
