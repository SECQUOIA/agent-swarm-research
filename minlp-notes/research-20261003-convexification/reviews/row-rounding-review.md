# Independent row elimination and rounding review

The reviewed primitive is `solver/row_certificate.py`. Its mathematical
contract is correct. If original source sides satisfy
`h_r(v) + d_r v <= b_r`, nonnegative multipliers and a support inequality
`a v + sum_r lambda_r h_r(v) >= beta` imply
`(a - sum_r lambda_r d_r) v >= beta - sum_r lambda_r b_r`.
The directions of both inequalities and both subtraction signs were checked
independently of the producer's replay routine.

For an exact coefficient vector `C`, the exported binary64 vector `Chat` has
error `e = Chat - C`. On a valid global box, `e v` is at least the sum of its
coordinatewise endpoint minima. Adding that lower bound to the exact right
side and rounding downward is valid. The implementation sums duplicate terms
and performs every intermediate operation in exact rational arithmetic.
It declines a nonzero rounding error on an unbounded coordinate, and allows
unbounded coordinates when their exported coefficient is exact. This is
needed for the original objective epigraph.

Five independent tests passed with:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/test_row_rounding_review.py
```

These tests derive the eliminated row directly and enumerate every box
corner to establish the exact worst rounding loss. They check both error
signs, negative endpoints, rational source coefficients, sharp downward
rounding, cancellation of terms of size `10^30`, an unbounded objective
coordinate, and refusals for negative multipliers and unbounded rounding
errors. They do not infer validity from producer/checker agreement. The
implementation author's separate suite reports 62 boundary and binding tests.

This primitive treats supplied bounds, original sides, and the support
certificate identity as trusted inputs. The original-model saved-cut replay
must independently establish those premises. It certifies a supplied linear
row; it does not certify SCIP presolve, floating-point feasibility, or a
complete optimization result.

Reviewed SHA256:

| File | SHA256 |
| --- | --- |
| `solver/row_certificate.py` | `6917a78df65e0c7edc4dcf3fe695296fb6b9164c51d145f0b32f655fad6b2a9c` |
| `reviews/test_row_rounding_review.py` | `8910374e562bbcae358d9566d6ad800a22e7d12518646ffef35e2fe663b996e8` |

Only topic-specific checks were run. No prior frozen files, project-wide
verification, or CI results were changed or inspected.
