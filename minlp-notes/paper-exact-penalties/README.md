# Exact norm penalties

`main.tex` is the manuscript source and `main.pdf` is the compiled manuscript.
The author field is intentionally blank. The bibliography identifies the
versions used, including the December 15, 2025 Lefebvre–Schmidt manuscript.

Build from this directory with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python3 verification/check_lower_bound.py
python3 verification/check_upper_bound.py
python3 verification/check_calibration_perturbation.py
```

`verification/check_lower_bound.py` evaluates exact envelopes on the stated projected
interval endpoints, optimized dual formulas, multiplier-independent balanced
witnesses, accuracy thresholds, strict points, and encoding counts. The
projection itself is established by the manuscript proof. The script also
checks exponent arithmetic for the fractional-power example and the
completed-square identity for the source example's continuous branch. It uses
only Python's standard library. Finite checks support arithmetic and indexing;
the manuscript proofs establish the quantified claims. These are targeted
local checks, not project-wide verification or CI results.

`evidence/coverage.md` maps the repository's penalty developments to the
manuscript and identifies related work with a different scope.

The upper-bound check uses SymPy (validated with version 1.14.0). It checks
the adjugate stationarity and numerator identities in a singular-Hessian
example, the degree counts, and a regularized family with no unperturbed
Slater point and divergent multipliers. It also checks valid and invalid candidates for a two-coordinate
reciprocal graph, including saturation of a smaller residual coordinate. These checks do not validate general quantifier
elimination or the cited algebraic radius and height bounds. The manuscript
proves the reduction to those bounds.

`verification/check_calibration_perturbation.py` uses only the Python standard
library. It independently enumerates balanced mixtures for small calibration
instances and their fixed-zero-multiplier thresholds, checks centered and
endpoint grids against rational box boundaries (including finer cases with
upper bounds below one), and tests the atomic grid correction, deterministic
margins, continuous and finite-grid tail identities, and infinite-threshold
witnesses at the zero atom of a concrete rational grid. Its finite examples do not prove complexity
reductions or the general geometric and Gaussian statements.
