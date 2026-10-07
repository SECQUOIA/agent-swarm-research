# Stage 2 lead verification

Working directory: `code/minlp_solver_lab`.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PATH=/workspace/local-home/miniconda3/envs/solvers/bin:$PATH .venv/bin/python -m unittest lbesh.tests.test_publication_contracts lbesh.tests.test_independent_solver_review -v
```

Passed: all 25 tests, no skips. Adding the installed Ipopt executable to PATH exercised the real reduced-NLP/exponential analytic checks that skipped during the earlier readiness assessment. Tests cover the known log(2) optimum across all eight separator/formulation/tree combinations, original nonlinear objectives and maximization, fixed/rounded integer variables, logic, inactive/constant alternatives, bound orientation, invalid candidates, callback/nonfinite failures, unsupported structures, and no-NLP linear regressions. A deliberate inconsistent-bound fixture emitted Pyomo's expected warning; all assertions passed.

This verifies selected behavior of the existing frozen implementation. It is not proof that floating-point solvers satisfy every exact-arithmetic theorem assumption. No research source was changed, no full benchmark was rerun, and no project-wide check or CI inspection occurred.

Source inspection separately confirmed that the internal absolute primal tolerance and objective-gap rule differ from the independent benchmark classification formulas. The mathematical author has been asked to keep those roles explicit.
