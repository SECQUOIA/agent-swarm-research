# Sparse indicator quadratic optimization

Read [paper.pdf](paper.pdf), or build the source [main.tex](main.tex).
Section sources are in `sections/`.
The author and date fields are intentionally blank. References identify the
specific versions used in the comparisons. `evidence/coverage.md` maps the
relevant repository results, and `evidence/sources.md` records inspected
primary sources and the limits of the novelty comparison.

From this directory, build only this manuscript:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The resulting PDF is `build/main.pdf`; `paper.pdf` is the checked distribution
copy. Build outputs are ignored by Git.
The build needs a standard TeX installation with `latexmk`, BibTeX, and
the packages named in `main.tex`. No repository-wide verification is needed.

Run the exact finite checks with:

```sh
python3 -B checks/check_enumeration.py
python3 -B checks/check_limits.py
python3 -B checks/check_extensions.py
python3 -B checks/check_spectral.py
```

The first checker covers the near-optimal count and certified enumeration,
including tight atomic counts, noisy-constant optimizer recovery, and a
support optimal only at one parameter. The second independently assembles
the hardness and message quadratics from residual rows, solves every support
in small instances, and checks the pruning estimates, star inverses, exposed
face, and normalized projected-row distinction for every order of small stars.
The third checks atomic higher moments and both VC and affine-rank tails by
complete finite-noise enumeration, and verifies open/closed endpoint and
interval discrepancy bounds. All use exact rational arithmetic and the Python
standard library.

The fourth checker tests `checks/spectral_reference.py`, a reference of the
main spectral algorithm. Its optimization oracle uses the supplied tree
decomposition and projected bag tables. It then reoptimizes the selected
support, enumerates near-optimal supports, and constructs each message directly
with the same noise vector. It returns noisy quadratic coefficients, optimizers,
and an additive certificate for the original objective. Inputs must satisfy
the documented rational-data, spectral-bound, and decomposition preconditions;
all numerical inputs are `fractions.Fraction` values. The implementation uses
the valid message-specific coordinate bound instead of its common upper bound
used to state the theorem's work estimate.

Independent grid enumeration and Cramer's-rule support solves check small
instances, fixed indicators, nonzero edge factors, empty/repeated bags, finite
boundary probes, and exact tie-only labels. The earlier enumeration checker
uses an exhaustive approximate oracle; the spectral reference uses bag DP.
These exact finite checks supplement the proofs; they do not establish the
asymptotic theorems, full-box completeness, novelty, or a practical speedup.

The supporting appendices give all fixed moments, algebraic region and labeled
subdivision consequences, sharper scalar and planar geometric bounds,
finite-grid discrepancy transfer, and direct recursive algorithms under strict
diagonal dominance. The manuscript distinguishes all active support labels,
necessary formulas, connected winning regions, and CAD subdivision cells.
The geometric and CAD theorems are proved or derived from cited primary results;
the finite scripts do not implement CAD or complete recursive SDD algorithms,
and do not computationally verify the analytic coarea argument. Actual commands,
diagnostic counts, and limits of validation are in `evidence/validation.md`.
