# Classical and Quantum Query Complexity of Scalar Newton Quantities

This directory contains a standalone LaTeX manuscript. The entry point is
`main.tex`; `main.pdf` is the compiled paper. `bibliography.bib` and the
included `main.bbl` supply the references. No file outside this directory
is needed to build the manuscript.

The results distinguish sparse entries, sampling-and-query access, and
coherent block access. Query and ideal-arithmetic bounds do not include
unprovided input-loading or bit-complexity guarantees. The paper states
which lower bounds match and which parameter regimes remain unmatched.

From this directory, use the repository's `qipm` environment:

```sh
conda run -n qipm --live-stream make
conda run -n qipm --live-stream make check
conda run -n qipm --live-stream make package
```

Alternatively, the checks can use the absolute environment interpreter:

```sh
make check PYTHON=/home/sgusev/miniconda3/envs/qipm/bin/python
```

A clean rebuild is `conda run -n qipm --live-stream make -B`. The LaTeX
build requires `pdflatex`, `bibtex`, and the standard packages listed in
`main.tex`. The independent identity diagnostics use Python with NumPy
and SciPy, already provided by `qipm`. No dependency installation is part
of the build. Outside this repository, equivalent installed tools suffice;
`PYTHON` can select the appropriate Python interpreter.

The five checks exercise residual polynomials and scalar variance,
cyclic clock identities, lower-bound witness identities, temporal and
reuse identities, and structured cone/core/preconditioner identities.
They are reproducible numerical diagnostics, not substitutes for the
proofs. They use fixed random seeds where applicable and do not benchmark
claimed asymptotic query lower bounds.

`make package` creates `scalar-newton-submission.zip`, containing the
manuscript source, bibliography and compiled bibliography, PDF, build
instructions, and diagnostics. Regenerate it after changing the paper.
The source has no author identity or journal-specific formatting; supply
the authorship and administrative information required by the chosen
submission venue.

The separate `audit/` directory records source coverage, literature
checks, author reports, independent review findings, and corrections.
It is excluded from the submission package. These internal reviews are
not external peer review.
