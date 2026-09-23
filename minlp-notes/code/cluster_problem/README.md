# Cluster-problem illustration: node counts at nondegenerate and degenerate constrained minima

Supports `results/cluster-free-branch-and-bound-constrained-minima.md`.

```
conda run -n minlp-notes python code/cluster_problem/count_boxes.py
```

A minimal spatial branch-and-bound (bisection of the widest side, best-bound
selection, incumbent fixed at the optimal value, fathoming at absolute
tolerance `eps`) with the same generic second-order relaxation of the nonlinear
constraint in both examples (`g - alpha * sum (x_i - l_i)(u_i - x_i)`,
`alpha = 1`; error `<= n alpha w^2/4`), convex objectives kept exact, node
problems solved with cvxpy (Clarabel, with SCS as fallback).

This is an uncertified numerical illustration. The script uses numerical
primal objective values as estimates of relaxation optima, accepts
`optimal_inaccurate` and `infeasible_inaccurate` statuses, and does not
validate dual lower bounds or infeasibility certificates. Its node counts
therefore depend on solver accuracy and are not rigorous branch-and-bound
certificates. The recorded run includes an accuracy warning.

Recorded run (2026-09-22, about 10 minutes):

| `eps` | A: nodes | A: max open | B: nodes | B: max open | `eps^(-1/4)` |
|---|---|---|---|---|---|
| 6.3e-2 | 7 | 2 | 18 | 6 | 2.0 |
| 1.6e-2 | 10 | 3 | 26 | 6 | 2.8 |
| 3.9e-3 | 17 | 6 | 41 | 8 | 4.0 |
| 9.8e-4 | 20 | 6 | 59 | 11 | 5.7 |
| 2.4e-4 | 23 | 6 | 87 | 17 | 8.0 |
| 6.1e-5 | 29 | 6 | 124 | 21 | 11.3 |
| 1.5e-5 | 32 | 6 | 179 | 31 | 16.0 |
| 3.8e-6 | 35 | 6 | 253 | 48 | 22.6 |
| 9.5e-7 | 41 | 6 | 362 | 65 | 32.0 |

Example A (`min x_1^2 + x_2^2` s.t. `x_1 x_2 >= 1` on `[0.5, 2]^2`; LICQ,
strict complementarity, second-order sufficiency on the critical cone only):
the number of open boxes is at most 6 and the recorded node counts are
consistent with `log(1/eps)` growth (roughly three to seven additional nodes
per quartering of `eps`, the depth needed to
reach width `sqrt(eps)`). Example B (`min x_2 - x_1` s.t.
`x_2 >= x_1 + (x_1 - 1)^4` on `[0, 2] x [0, 3]`; second-order sufficiency
fails, quartic growth along the critical direction): the recorded counts
are consistent with `eps^{-1/4}` growth (at the smallest tolerance, nodes
about `11 eps^{-1/4}` and open boxes about `2 eps^{-1/4}`). These finite
runs do not establish asymptotic rates or the constants of the theorem.
The theorem bounds comparable-size boxes locally; the heap can contain
multiple sizes, so its maximum size is a different quantity.
`run.log` holds the last run.

The corrected nearby-point counterexample in Section 3 of the result note
has a separate exact polynomial-identity check, requiring SymPy:

```
python code/cluster_problem/check_counterexample.py
```
