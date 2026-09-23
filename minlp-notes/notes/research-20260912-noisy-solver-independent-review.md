# Independent review of the noisy Markov design prototype

Date: 2026-09-12. Reviewer: fresh agent `/root/noisy_solver_review`, separate
from the implementation author and the scalar theorem reviewer. Status:
passed for the stated mathematical model and tested numerical scope after two
implementation issues were corrected. This review establishes neither
publication priority nor a general computational advantage.

The reviewed implementation is
[noisy_markov_design.py](../code/research_20260912/noisy_markov_design.py),
SHA-256
`b47931e8e7871c7ed98dafd09ed99020b821bfefb0e920a49238836afea38fb7`.
The [standalone verifier](../code/research_20260912/review_noisy_markov_solver.py)
and its [JSON report](../code/research_20260912/results/noisy-markov-solver-independent-review.json)
are retained. The report records source, verifier and benchmark hashes, package
versions, individual solve statuses, error residuals and failure-path checks.
The implementation source is checked for modification during each verifier
run. The reviewer did not edit the implementation.

The prototype handles stationary scalar covariance
`R_ij=P rho^|i-j|+r 1{i=j}`, fixed mean sensitivities, a positive-definite
information prior, and selection of exactly `k` calendar indices. It is
narrower than the time-varying and full-block mathematical extensions in the
[theorem note](research-20260912-noisy-markov-memory.md). The independent scalar
and block proof reviews remain separate evidence; this review checks the
implemented specialization and its numerical optimization certificates.

The original implementation underestimated memory by omitting dense covariance
and pricing workspaces, and computed true seed/full-selection objectives before
the memory guard. Thus a small configured memory limit did not prevent those
allocations. The author moved the preflight before objective evaluation and
included those workspaces in the estimate. A mock that fails on any objective
evaluation now verifies that an early refusal returns `memory_limit` with null
objective and bound fields. The estimate remains a planning guard, not an
operating-system memory limit, as the updated README states.

The original `CalendarOracle.information` silently accepted some invalid
subsets by turning them into a set. The author added shared validation to
true information, local information and residual-covariance evaluation.
Duplicate, negative, out-of-range and noninteger indices now fail clearly.
The same review also exercised invalid dense warm starts and covariance
splitting parameters. Root-phase numerical inconsistency guards were present
in the final reviewed source.

The conditional information calculation is correct. Bit zero denotes the
preceding calendar index, and a skip shifts a zero into the window. The
conditional regression uses the selected entries of the original covariance.
Both its variance and its sensitivity are adjusted:

```text
b = R_tH (R_HH)^(-1),
d = R_tt - b R_Ht,
g = F_t - b F_H,
W = g^T g / d.
```

The subtraction in `g` is necessary when conditioning actual observations.
The verifier forms an explicit unit lower-triangular residual map on each
selected subset, obtains `Q=A^T D^(-1) A`, and independently evaluates
`prior+F_S^T Q F_S`. It uses dense inverses for this small reference
calculation, rather than copying the production accumulation of arc matrices.
It also checks information for cardinalities other than the oracle's priced
count. The implementation deliberately recomputes such information; entries
in the precomputed arc table that cannot belong to a size-`k` path may be zero.

Exact-count pricing is correct. A dynamic-programming state records the
number already selected and the recent calendar mask. The recurrence retains
the greatest accumulated linear score reaching that state. The skip test
removes states with too few remaining calendar positions to reach `k`, and
the terminal layer requires count `k`. Information from the fixed prior is
excluded from every arc score and added separately to tangents. The
independent reference uses tuples of recent selected calendar indices, not
masks or the production predecessor arrays. Enumeration and that separate
recurrence agree with the returned maximum and selected path. Tests include
indefinite gradient matrices, hence negative arc scores, as well as zero
information and tied paths.

The hull certificate has the correct direction. For any positive-definite
matrix `M`, not necessarily the exact hull optimizer, concavity gives

```text
logdet J <= logdet M - p + tr(M^(-1) J).
```

Maximizing the final linear term over all count-feasible paths therefore gives
a valid upper bound for the surrogate hull and every discrete surrogate
design. A feasible convex combination supplies a lower value for the hull
optimization; it does not supply a feasible discrete-design objective. The
implementation keeps those roles separate. Every true lower bound comes from
reevaluating a size-`k` subset using the original marginal covariance. SLSQP
only improves feasible mixture weights. Its success is unnecessary for the
validity of a completed pricing certificate.

The uniform spectral correction agrees with the reviewed scalar theorem. The
verifier recomputes the gain-refined constant using the alternative expression
`direct_tail+gain*(unrefined_row_sum-direct_tail)`. It checks the actual
normalized residual eigenvalues against this constant. Independence, zero
latent variance and complete calendar history return an exact surrogate and
zero correction.

When `delta<1`, the data-information inequality gives

```text
J_true(S) <= prior + (J_surrogate(S)-prior)/(1-delta).
```

This proves both the blanket shift `U-p log(1-delta)` and the implemented
prior-aware tangent. At `N=prior+(M-prior)/(1-delta)`, the latter is

```text
logdet N - p + tr(N^(-1) prior)
  + max_path sum_arc tr(N^(-1) W_arc)/(1-delta).
```

Optimizing `M` for the uncorrected hull does not invalidate this tangent.
A single prior-aware tangent need not outperform every previously available
blanket-shift bound, so the implementation correctly takes their minimum
together with the true full-selection upper bound. When `delta>=1`, the
spectral transfer is not used. The verifier reconstructs each saved tangent,
independently solves its linear pricing problem and checks that the reported
true upper bound is exactly the minimum of the available completed
certificates. Thus the larger saved cases are checked without assuming that
their unknown discrete optimum equals a feasible objective.

The dense comparator is consistent with the same noisy covariance. It uses
`a=split_fraction*lambda_min(R)`, `S=R-a I`, `D=diag(z)/a`, and

```text
V = (I+S D)^(-1) F,
J(z) = prior + F^T D V,
d logdet J(z)/d z_i = V_i J(z)^(-1) V_i^T/a.
```

For `0<split_fraction<1`, the binary information equals the selected marginal
information. Its concavity supports the upper tangent cuts. Independent
checks cover splitting fractions 0.01, 0.5, 0.99 and 0.999999. Finite
differences and tangent inequalities agree with the implemented gradient.
The root LP phase preserves true lower bounds, and its fractional relaxation
values are recorded separately. A run with a root phase and zero integer
rounds retains precisely its initial true lower bound. True-valued warm
starts and the transition from continuous to binary variables passed small
enumerated comparisons. Gurobi uses one thread.

The final bounded verification run completed in about 2.1 seconds with one
BLAS thread, Python 3.13.11, NumPy 2.5.3 and SciPy 1.18.1. The checks were:

| Check | Count |
| --- | ---: |
| Independent subset information factorizations | 1,136 |
| Residual spectral comparisons | 860 |
| Exact-count prices against enumeration and tuple-state DP | 160 |
| Dense binary information identities | 704 |
| Dense gradient finite-difference directions | 48 |
| Dense tangent inequalities | 384 |
| Hull solves checked against enumerated discrete optima | 40 |
| Dense solves checked against enumerated discrete optima | 32 |
| Feasible fractional points checked against root bounds | 80 |
| Invalid input rejection checks | 23 |
| Saved benchmark hull results independently reconstructed | 6 |

The greatest absolute information-factorization discrepancy was
`3.55e-15`; the greatest pricing discrepancy was `1.07e-14`; the greatest
gradient directional discrepancy was `8.76e-10`. These residuals quantify
agreement on tested instances and are not rigorous error bounds.

Failure-path checks include zero and one optimization round, a deadline
already exhausted before pricing, a memory refusal, one SLSQP iteration,
zero integer rounds after root refinement, and injected deadlines during
pricing and correction. The tests verify that a later pricing interruption
preserves an earlier completed upper certificate and that interrupted
correction preserves feasible weights. A memory refusal returns no invented
feasible objective. No tested cap status is misrepresented as a discrete
optimality result. `pricing_rounds` counts the main hull iterations; the
optional final prior-aware pricing step is additional.

The six saved hull records use `n=12,24,48`, `k=n/3`, `rho=0.4`, unit
latent/noise variances, and `L=4,6`. Their stored matrices, mixtures, selected
subsets, surrogate tangent maxima and prior-aware maxima all reconstructed.
The benchmark artifact hash at review was
`f259d211c490ae19673ef740c610482015e44c956c3db61be75807331ff7dc87`.
The twelve-candidate discrete optimum was also independently enumerated.
Saved dense incumbents were reevaluated for every size. For larger saved dense
runs, solver bounds cannot be independently reconstructed from the JSON:
the OA cut systems and solver proof logs are not retained. The fresh small
dense comparisons provide separate implementation evidence.

The strengthened dense comparison materially changes the practical reading.
With splitting fraction 0.99, up to 200 root cuts and the disclosed best
hull-generated MIP start, it closes the 12- and 24-candidate cases in about
0.022 and 0.032 seconds. At 48 candidates it reaches a true logdet gap
`0.0246235` in approximately five seconds. The `L=6` hull result has corrected
true gap `0.0226885`, while its surrogate hull gap is about `1.25e-9`.
Hull closure therefore does not close the true design problem in that case.
The warm-start generation time is excluded from the strengthened dense
solver's five-second cap and is disclosed in the implementation README.
One seed and these nested generic instances do not establish broad superiority,
application value, or a publishable algorithmic advance.

Remaining limits are numerical and operational. The bounds use ordinary
floating-point solves, eigenvalues, SLSQP and Gurobi tolerances, without
outward rounding or interval validation. Highly ill-conditioned priors or
information matrices may impair correction or bound accuracy; a small
additional probe with prior scales down to `1e-12` caused hull correction to
stall rather than provide an effective bound. Time limits are soft across
an individual numerical operation and preprocessing, and memory limits are
workspace estimates. Unanticipated numerical-library or solver exceptions
can still propagate instead of becoming a structured result. These limits
should remain visible when reporting results or extending the prototype.

Reproduce the independent review from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/review_noisy_markov_solver.py
```
