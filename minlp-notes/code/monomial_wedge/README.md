# Wedge envelopes of two-variable monomials with real exponents: numerical check

Supports `results/monomial-wedge-envelopes-real-exponents.md`.

```
conda run -n minlp-notes python code/monomial_wedge/check_envelopes.py
```

For 26 exponent pairs covering the six regimes of Theorem 1, swapped mixed
signs, exact boundary cases `beta = 1`, and zero individual exponents, the script builds the chord function `phi`, the
ray function `H` and the corner interpolant `L`, checks their exactness
properties (rays, level curves, corners), and compares the predicted lower and
upper envelopes at random points of `conv(D)` with the LP envelopes of a dense
sample of graph points over `D` (about 4800 points). The pass conditions
separate signed validity discrepancies (`<= 1e-7` relative to `u`) from
two-sided finite-sample approximation error (`<= 2e-3` relative to `u`).
Sampled graph points must satisfy both predicted envelope inequalities.
Sampled points outside the predicted `conv(D)` must be LP-infeasible; solver
errors are reported rather than interpreted as infeasibility. A failed check
exits with a nonzero status.

Exact rational examples separately check the corrected degree-zero statement:
two-ray decompositions with either exponent sign, loose value bounds, empty
and singleton ratio intervals, the constant graph, and a sequence of hull
points approaching the excluded boundary point `(1, 1, 2)` for `f = x_2/x_1`
on ratios `[1, 2]`. These examples illustrate why the ordinary hull differs
from its closure. They do not prove the general set equality.

These are targeted mathematical sanity checks, not a proof or a solver
performance benchmark. LP agreement with a finite sample does not establish
exactness of an envelope.

Audit run (2026-09-22):

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python code/monomial_wedge/check_envelopes.py
git diff --check -- results/monomial-wedge-envelopes-real-exponents.md code/monomial_wedge/check_envelopes.py code/monomial_wedge/README.md
```

Both commands passed. The checker used NumPy 2.5.1 and SciPy 1.18.0; all 26
nonzero-degree cases and the exact degree-zero examples passed. The largest
reported signed discrepancy was `1.0e-15` relative to `u`, the largest
two-sided sampling discrepancy was `4.2e-4`, and no sampled point outside the
predicted domain was LP-feasible. These were targeted local checks; no
project-wide verification or CI checks were run.
