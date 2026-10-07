# Targeted verification record

Verification is restricted to the joint-convexification continuation. No
project-wide checks or CI status/log inspection were performed. Research-agent
review is internal review, not journal peer review or formal verification.

## Combined component checks

From the repository root, with the recorded Python 3.13.11 experiment
environment:

```sh
PYTHONPATH=research-20261002-convexification:research-20261002-convexification/solver \
  code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261002-convexification/solver \
  research-20261002-convexification/theory \
  research-20261002-convexification/reviews/test_numerical_review.py \
  research-20261002-convexification/reviews/test_replay_review.py \
  research-20261002-convexification/reviews/test_source_model_review.py \
  research-20261002-convexification/experiments/test_cases.py
```

Result: **186 tests passed, with 53 subtests passed**, in 1.97 seconds.
This combines the previously separate arithmetic, theory, screening, native
sampling, importer, integration, independent review, and experiment-harness
checks. It does not collect tests from the frozen experiment source copies.

The first combined invocation supplied only the topic root in `PYTHONPATH`.
Collection failed for two tests that use standalone module imports
(`native_sampling` and `screening`). Adding the solver directory, as in their
component invocation conventions, resolved collection. No implementation
change was needed; the corrected command above completed successfully.

Before the campaign freeze, the experiment checker received one further
regression rejecting a nonfinite objective. The focused follow-up command was:

```sh
PYTHONPATH=research-20261002-convexification:research-20261002-convexification/solver \
  code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261002-convexification/experiments/test_cases.py
```

Result: **4 tests passed** in 0.67 seconds. Three were already included in the
combined run; this follow-up checks the changed harness and its new regression.

## Independent mathematical and source reviews

- [Numerical review](reviews/numerical-review.md): analytic interval and
  final-rounding checks, domain boundaries, screening norms, omitted proof
  cells, changed coefficients, and other forged-certificate cases. A
  generator/replay depth-budget mismatch was fixed and checked.
- [Star audit by full-space enumeration](theory/star-audit.md): 155 constrained
  stars compared with exact KKT face enumeration, 298 returned pieces checked,
  a mixed-curvature four-dimensional example, and seven rejected mutations.
- [Star audit over entire intervals](reviews/star-review.md): 88 cases,
  786 intervals, 7,063 exact alternative-rule comparisons, independent domain
  projection, and three rejected mutations.
- [Integration review](reviews/integration-review.md): source/native row
  equivalence, source domains under cancellation, auxiliary definitions,
  reformulation equivalence, actual inserted coefficients and scope, and
  original-model-bound replay. Concrete defects found during review were
  corrected before the experiment freeze.
- [Document review](reviews/document-review.md): mathematical hypotheses,
  correspondence between statements and implementation, attribution, and
  consistency with the retained computational evidence.

These reviews have different roles. Algebraic test instances do not replace
proofs; fresh-process replay shares some exact primitives with generation;
and numerical checks of SCIP incumbents and bounds do not certify a full solve.

## Experiment and document records

The [experiment protocol](experiments/protocol.md) records the selected models,
controls, budgets, ordering, and failure policy. The campaign retains frozen
sources, input models, raw records, and fresh-process replay results. Its
summary records the commands actually run and measured limitations.

The [document build instructions](document/README.md) and source reviews
record the LaTeX build and claim checks. The
[literature source manifest](literature/sources/MANIFEST.md) records source
versions, inspected passages, file hashes, retrieval limits, bibliography
checks, and local-link checks.
