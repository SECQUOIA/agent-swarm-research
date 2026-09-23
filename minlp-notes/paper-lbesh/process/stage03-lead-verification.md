# Stage 3 lead verification

Working directory: `code/minlp_solver_lab`. These are targeted local checks; no project-wide or CI checks were run.

1. `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python -m unittest lbesh_research.test_instances_independent lbesh_research.tests.test_conic lbesh_research.test_independent_conic -v`

   Fourteen actual tests passed (three independent instance checks and eleven conic checks). The command exited with status 1 because the third module path was incorrect: it needs `.tests.`. The fifteenth reported test was a loader error, not a scientific test failure. The affected module was rerun correctly below; the already passing modules were not repeated.

2. `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 lbesh_research/conic_reference_env/.venv/bin/python -m unittest lbesh_research.test_conic_reference lbesh_research.test_conic_reference_independent -v`

   Six tests passed, with no skips. They cover independently enumerated assignments, positive-weight and zero-weight closures, singular-domain rejection, unsupported trigonometric rows, five pilot roots checked against independently implemented perspective atoms, and fractional scalar perspectives.

3. `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 LBESH_RUN_SOLVER_REVIEW=1 .venv/bin/python -m unittest lbesh_research.tests.test_independent_conic -v`

   Eleven tests passed, with no skips. They cover conditional objectives, indicator references, empty branches at zero weight, original-space witnesses for expanded PSD quadratics, global norm/reciprocal/maximum rows, infeasible outcomes without stale witnesses, invalid convex bounds and reciprocal domains, shifted-square fractional hulls, unsupported SOS, and small indefinite Hessians.

In total, 31 distinct scientific tests passed. The initial invocation error was corrected. These fresh formulation checks do not add observations to the frozen benchmark cohort.

The lead also searched online for `"extended supporting hyperplane" "generalized disjunctive" 2026` and `"radial" "perspective cuts" "disjunctive"`. These searches did not reveal an additional directly relevant primary result beyond the reviewed literature; that negative search is not evidence of priority. The local full text of Kelley, Kazachkov and Ralphs, *Parametric Disjunctive Cuts for Sequences of Mixed Integer Linear Optimization Problems* (2025), was inspected: it concerns transferable MILP disjunctive certificates across perturbed problems, not the radial-versus-point policy studied here. No novelty claim or manuscript citation was added on that basis.
