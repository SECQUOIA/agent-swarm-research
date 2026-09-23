# Independent review of the shared-scenario kinetic solver

Date: 2026-09-12. This review independently reconstructs both saved chemical
instances, including their individual reference bounds. The numerical
implementation is accepted after the two boundary corrections described
below. This review does not turn floating-point bounds into exact certificates;
the separate theorem and rational-certificate review owns that conclusion.

The checker is
[review_robust_solver.py](../code/research_20260912/review_robust_solver.py), with
[machine-readable evidence](../code/research_20260912/results/robust-solver-independent-review.json).
That evidence records the exact implementation and accepted-core hashes tested.
The final reviewed implementation hash is
`a26e91d75c603dd711336383b0b8ed6d611aba2cd8cfe9b185af329dfc832a35`.
The chemical artifacts retain their original generating source hash
`93cd7fbee09c78c696bced7cc70a14ab26f6eabe94e6f119dca32e498106de4b`.
Neither their saved schedules nor the accepted single-scenario core were
changed during this review.

## Findings and corrections

The original normalizer accepted finite positive entries whose sum could
overflow. Specifically, `probability([1e308,1e308])` returned `[0,0]`. For two
identical scalar scenarios with prior information 2 and selected observation
information 1, `tangent_price` then reported upper bound 0 although the optimum
is `log(3)`. The author corrected normalization by dividing by the largest
positive entry before summing. The independent regression checks the resulting
simplex and the actual `log(3)` tangent bound. This failure did not affect the
ordinary weights in the chemical artifacts.

The original greedy solver could retain a better evenly spaced seed while
completing exchanges at a different, worse path. Its status then incorrectly
called the returned seed a single-exchange local optimum. A seven-time,
three-scenario example returned seed `(0,3,6)` with score `-1.1913558697`, while
neighbor `(0,2,3)` scored `-0.9215037839`. The correction starts exchange search
from the better available incumbent and reports the completed exchange path
when declaring local optimality. The independent regression checks all
neighbors of the returned schedule. Both saved chemical greedy schedules were
already genuine local optima, so their interpretation is unchanged.

The 48-time hull run reports one unsuccessful SLSQP correction, with message
`Positive directional derivative for linesearch`. Its retained mixture is
feasible and the independent weighted tangent closes the numerical hull gap
to `2.16e-9`. Success of the optimizer is therefore unnecessary for this
reported bound. The 96-time run has no unsuccessful corrections.

## Independent reconstruction

The checker computes original information by Cholesky whitening, rebuilds
local conditional information directly from the covariance, and prices scalar
arcs with a separate dictionary dynamic program. It does not call the author's
pricing implementation to reconstruct saved upper witnesses. It checks:

- Every individual and shared support matrix, mixture weight, mixture matrix,
  selected score, and best retained path.
- All individual and shared tangent constants, gradients, prices, priced
  schedules, and minimum upper bounds, including the correction that leaves
  the prior unscaled.
- The common schedule and common mixture across scenarios. Cross-scenario
  blocks have no statistical interpretation and contribute nothing under the
  block-diagonal gradient.
- Individual-reference uncertainty in every standardized score and efficiency
  bound. Subtracting feasible reference lower bounds is a fixed-offset
  objective; it is not silently treated as exact scenario standardization.
- The analytic sensitivities against derivatives of the two-species matrix
  exponential, using the Frechet derivative rather than the author's mean
  formula. The largest discrepancy is `1.37e-14`. The same calculation confirms
  the stated rate-swap ambiguity when the initial concentration is unknown.

The largest discrepancy in reconstructed saved scenario scores is `6.65e-13`;
support matrices agree within `4.55e-13`, shared scalar prices within
`3.82e-14`, and shared upper bounds within `2.00e-13`.

Fresh exhaustive tests use three scenarios with different positive definite
priors, two parameters, eight candidate times, and all 56 size-three schedules.
They cover positive and negative AR coefficients and windows `0,2,5,7`.
Every combined price agrees with direct enumeration, full history agrees with
the true covariance, and all tested true upper bounds contain the exact
enumerated discrete optimum. Direct finite differences agree with mixture
gradients within `3.64e-10`.

An asymmetric scalar example has path information pairs `(4,1)` and `(1,2)`.
Its optimal mixture and dual scenario weights are `(1/4,3/4)`. Checking this
example distinguishes multiplier signs and unequal weights, while injected
unsuccessful optimizer results test clipped, absent, nonfinite, and extreme
finite multiplier proposals. Single-scenario cases with zero and full sample
counts also retain their exact feasible values and bounds.

## Saved comparisons and their limits

| Candidate times | Shared-hull schedule score | Completed greedy score | Shared numerical upper bound |
|---:|---:|---:|---:|
| 48 | -0.094278216 | **-0.089793800** | -0.081524745 |
| 96 | **-0.089226230** | -0.103905526 | -0.072858072 |

Scores use the saved fixed offsets. Independent greedy reconstruction returns
the exact saved paths, with 6 and 17 accepted exchanges and 4,233 and 39,441
objective evaluations. All 512 neighbors of the 48-time greedy incumbent and
all 2,048 neighbors of the 96-time incumbent have lower scores.

The generated hull incumbents themselves have improving exchange neighbors:
`+0.001819098` at 48 times and `+0.001262725` at 96 times. They should be called
generated feasible schedules, as the author does. Neither a completed local
optimum nor global discrete optimality follows from their closed hull gaps.

After reference uncertainty, the better retained schedule has a numerical
worst-scenario D-efficiency lower bound of 96.9355% at 48 times and 96.9529%
at 96 times. The central nominal schedules give 93.6938% and 96.1153%.
Combining the best feasible schedule with the common numerical upper bound
gives relative-to-optimum efficiency lower bounds of 99.6058% and 99.3363%.
These calculations support the stated mixed comparison; they do not establish
general superiority of one robust solver.

All scenario values, sensitivities, priors, and covariance parameters are
stipulated numerical inputs. The rate regimes are not measured uncertainty
limits. A finite scenario set does not cover intervening parameters, and
changing the grid while holding per-step correlation fixed changes the
physical correlation scale. These qualifications are correctly present in the
artifact metadata and author note. Literature and priority claims remain the
separate source audit's responsibility.

## Timing, caps, and reproduction

The recorded reference costs are 2.076 s and 9.980 s. Adding each solver's own
recorded cost gives 3.149 s and 13.635 s for reference plus shared-hull work,
and 2.576 s and 15.787 s for reference plus greedy work. The timing sums and
full-pipeline ordering check exactly. These are stored local measurements,
not independently recoverable historical wall-clock observations. The
independent checker's timings include caching and a different implementation
and are not competing benchmark measurements.

Both saved runs finish within their stated per-stage budgets. The cap is
cooperative: the implementation checks elapsed time between numerical
operations, and the memory cap compares an estimated array workspace with the
configured allowance. Neither is an operating-system resource limit. Immediate
deadline and memory refusal return no fabricated bound. An injected deadline
after a completed price retains its completed feasible and upper witnesses;
an iteration-limited result also retains valid numerical bounds.

Reproduce the independent review without modifying saved author artifacts:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python code/research_20260912/review_robust_solver.py
```
