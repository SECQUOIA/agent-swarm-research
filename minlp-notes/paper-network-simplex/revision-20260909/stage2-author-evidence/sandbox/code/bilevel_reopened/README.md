# Bilevel continuation code

This directory contains algorithms and verification experiments supporting the
[continuation results](../../notes/bilevel-reopened-closeout.md). Proofs establish
the general theorems; finite checks and numerical comparisons provide additional
evidence. Independent reviewer programs are identified by their filenames and
the linked review records.

## Implemented algorithms

- `quadratic_solver.py`: exact rational verification of scalar-leader box-QP
  response paths, exact affine or tariff-objective optimization on those paths,
  and a complete aligned rank-one price sweep. General path discovery uses
  numerical proposals and may report explicit recovery failure; the aligned
  sweep and the exponential small-instance exhaustive oracle use exact arithmetic.
- `approximate_structure_checks.py`: exact proof-of-concept for screening dense
  follower statuses using a surrogate, followed by true-Hessian KKT recovery.
  It includes exact objective sandwiches and negative screening examples.
- `quadratic_benchmarks.py` and `quadratic_tariff_benchmarks.py`: reproducible
  synthetic experiments with saved JSON results. Timings depend on the machine
  and workload. See the [algorithm note](../../notes/bilevel-reopened-quadratic-algorithm.md)
  for the API, numerical-proposal limits, model assumptions, and source attribution.

The general fixed-dimensional algebraic algorithms in the theorem documents are
not implemented by these prototypes. In particular, the near-optimal robustness
checks are diagnostics, not a complete quantifier-elimination solver.

## Verification

The existing environment used for the experiments is
`/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`; the numerical programs use
NumPy/SciPy, and some independent symbolic checks use SymPy. Pure rational
checkers use Python's standard library. From the repository root, examples are:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_reopened/quadratic_review_checks.py
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_reopened/screening_review_checks.py
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_reopened/nearoptimal_second_review.py
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_reopened/nonlinear_aggregate_review.py
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_reopened/response_constraints_review.py
```

The [closeout](../../notes/bilevel-reopened-closeout.md) links the independent
reviews and distinguishes author diagnostics, independent checks, exact
certificates, and numerical solver comparisons. Passing a numerical comparison
does not certify arbitrary instances or establish publication priority.
