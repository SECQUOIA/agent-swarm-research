**Independent review of certified MINLP driver integration.**

Reviewed 2026-09-13. No correctness blocker was found in the reviewed integration. This is a source review and targeted regression result, not a formal verification or a claim that all possible inputs have been tested. The exact-expression and discrete-proof kernels received separate reviews.

The reviewed file is [driver.py](../code/minlp_solver_lab/certify/driver.py), SHA-256 `cefb9d8278e2b7e942830964b7fac78994c647edb05cdf98f7c3d3f258911afb`. The review covered `prepare_model`, `build_certificate`, `check_certificate` and its internal helper, `vipr_compare`, and `_verify_given_cut`.

The source review traced fixed-value substitution and bounds, exact coefficient accumulation, nonlinear row shifts, signed objectives and constants, the epigraph extension, rational bound propagation, producer/checker model separation, supporting-point and residual-slope checks, LP regeneration, bijective VIPR variable naming, master identity, and final result reporting. Complete success requires discrete proof replay. A requested partial check reports `partial_ok` and `status="partial"` without exposing a certified bound. Failed external corroboration also prevents a complete success result.

The independent regression is [test_driver_independent_review.py](../code/minlp_solver_lab/certify/tests/test_driver_independent_review.py), SHA-256 `ca90b814b4e60edeeae5be9cd8db23e441ef49e1ca9b6778a024ae2ff361d547`. It checks the maximization problem

```
maximize  -(x-y)^2 + 3*x + 7
subject to 0 <= x <= 2, y fixed to 2, x^2 + 2*y <= 8.
```

The hand-constructed nonlinear row and epigraph cuts, together with a matching exact VIPR proof, establish the normalized lower bound `-13` and return the original maximization upper bound `13`. The value is attained at `x=2, y=2`. Increasing the row-cut intercept from `-8` to the invalid value `-7` is rejected at the cut-checking step, without exposing a certified bound. This exercises the combination of fixed substitution, nonlinear and affine objective terms, a nonzero constant, exact master identity, and objective-sign transfer in one complete check.

Reproduction command, run from the repository root after the driver hash above was recorded:

```sh
PYTHONPATH=code/minlp_solver_lab code/minlp_solver_lab/.venv/bin/python -m pytest -q code/minlp_solver_lab/certify/tests/test_driver_independent_review.py
```

Result: `1 passed in 0.63s`. The regression uses the in-repository exact proof replay and does not call an external solver or proof-checker binary.

Scope restrictions remain explicit. The checker interprets the loaded Pyomo expression tree, including prior Python/Pyomo construction rewrites. Domain checks use the declared variable box; missing domain restrictions are not inferred from nonlinear constraints. Cuts require finite supported symbolic derivatives; general subgradients and perspective recognition are unavailable. Unsupported LP names, active model components, multiple objectives, and unsupported nonlinear rows are refused. These restrictions can reduce coverage without invalidating accepted lower bounds. Full benchmark replay and its measurements are separate evidence.

The reviewer changed no core or paper files. The additions were the independent regression and this review record; the mathematical note was also aligned with the final expression semantics and supported-domain restrictions before this record was written.
