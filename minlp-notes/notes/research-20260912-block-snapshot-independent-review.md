# Independent review of the full-vector snapshot prototype

Date: 2026-09-12. Reviewer: `/root/noisy_solver_review`, separate from the
implementation author. Status: passed in the stated model and tested
numerical scope. No implementation change was required. The practical result
remains modest: greedy selection reproduces the same schedules, and the
shared-block Liu relaxation supplies tighter bounds in both saved probes.

The reviewed source is
[block_snapshot_design.py](../code/research_20260912/block_snapshot_design.py),
SHA-256 `85c328d8cab52989a308c90e54008ecc211ecb0ad1bd5b3db39b90f6ea6193ba`.
The [independent checker](../code/research_20260912/review_block_snapshot_design.py)
and [report](../code/research_20260912/results/block-snapshot-independent-review.json)
retain test counts, errors, source and artifact hashes, reconstructed bounds,
package versions and cap checks. This review concerns the implementation and
the [saved numerical probes](research-20260912-block-snapshot-probe.md).
The separate block approximation theorem and its novelty assessment are not
replaced by these tests. No new literature was identified during this review.

The covariance orientation is correct, including for nonnormal transitions.
The stationary latent covariance is `I`, the observation-noise covariance is
`I`, and the innovation covariance is `Q=I-AA^T`. Thus, for `t>s`, the lower
observation-covariance block is `A^(t-s)` and the upper block is its transpose.
Using `I-A^T A` for the innovations would generally define a different
stationary model. The reviewer constructs independent loadings of each
process innovation into all later states, sums their covariance contributions,
and adds independent observation noise. These calculations agree with the
implemented covariance. They include randomly generated nonsymmetric
transitions and the two saved coupled, nonnormal transitions.

Local factors also preserve the required block ordering. The implementation
stores history ages from nearest to oldest. It orders the covariance columns
and the sensitivity blocks the same way. The reviewer uses chronological
history order and an independently generated covariance, then forms the full
selected-subset residual transformation and conditional block covariance.
This verifies

```text
beta = R_tH (R_HH)^(-1),
D = R_tt-beta R_Ht,
w = (F_t-beta F_H)^T D^(-1)(F_t-beta F_H).
```

In particular, conditioning changes the sensitivity as well as the error
variance. The transformed residual covariance checks include correlations
between overlapping windows; they do not assume that different local
residuals are independent. Full history reproduces true marginal information.
Stationarity permits caching the regression and conditional covariance by
history ages, while the adjusted sensitivity remains time dependent.

With one unknown parameter, information is scalar and positive. Maximizing
`log J` is therefore equivalent to maximizing `J`. The implementation can
maximize the sum of local increments by one discrete exact-count dynamic
program, without a fractional information mixture. Its state tracks time,
the number selected, and the recent calendar mask. The predecessor arrays
recover a size-`k` schedule. The reviewer independently uses tuples of recent
calendar indices in place of masks. Both recurrences agree with exhaustive
enumeration on the tiny cases, and the independent recurrence reconstructs
both saved application optima for the surrogate problem.

The uniform-bound specialization is consistent with the separately reviewed
full-block theorem. This model is already noise-whitened, has `Pbar=rmin=1`,
and the stated transition norm cap is `rho`. Therefore the gain bound is
`kappa=1/2`, with no channel-count multiplier. The reviewer recomputes the
gain-refined constant as the direct geometric tail plus one half of the
remaining unrefined row bound. Independence and complete history correctly
give zero. The theoretical statements require an actual contraction bound;
the implementation's norm check and the numerical certificates remain
subject to floating-point tolerances.

For `delta<1`, the data-information inequality gives the implemented
prior-aware transfer:

```text
J_true(S) <= prior + (J_local(S)-prior)/(1-delta).
```

Consequently the completed global surrogate maximum yields a true-design
upper bound. The code also uses the true full-selection information, which
is an upper bound under the fixed Gaussian mean/covariance model even though
the full selection exceeds the count limit. It reports the minimum. Every
reported lower bound is the true marginal score of a feasible schedule.
When `delta>=1` no spectral transfer is used. The checker verifies the
reported arithmetic, the selected arc sum, and containment of the enumerated
true optimum on the small instances.

The shared-block Liu implementation uses the correct common visit variable
for every channel at a time. Let `D` repeat `z_t/a` over the block's channels,
`S=R-aI`, and `f` be the time-major sensitivity vector. Its symmetric positive
definite solve gives

```text
v = [I+sqrt(D) S sqrt(D)]^(-1) sqrt(D) f,
J = prior + [sqrt(D)f]^T v,
V = f-S sqrt(D)v.
```

The gradient with respect to the common block visit is the sum of that
block's channel derivatives, `sum_j V_tj^2/(aJ)`. The reviewer compares this
against a separate nonsymmetric resolvent solve, checks binary equality with
the true selected covariance, and differentiates block visits numerically.
At a tangent point, the sum of the `k` largest block gradient entries is the
exact linear maximum over `0<=z<=1, sum z=k`. Thus each saved tangent is an
upper bound independently of the continuous optimizer's success flag.
The checker reconstructs the saved tangent points, gradients, prices and
bounds, and separately verifies the fractional objective and rounded
schedule. Fractional values are not used as feasible discrete objectives.

The sensitivity and provenance checks use a different numerical method from
the author's analytic derivative and complex-step comparison. The reviewer
forms the three-species kinetic generator and its derivative with respect to
`log(k1)`. Matrix exponentials recover the concentrations, and the Fréchet
derivative of the matrix exponential recovers the parameter sensitivities.
After multiplying by the saved channel profiles, the sensitivities agree
within `3.54e-16`. Time grids, channel grids, profiles, mean spectra,
transition matrices and innovation covariances also reconstruct from the
stated formulas. The artifact source hashes match the reviewed source, and
both saved probe records are marked complete with one-thread BLAS settings.

The inputs remain a stylized kinetic spectrum and noise model. They contain
no measured spectral or residual-covariance data. Selecting a time acquires
all channels. Increasing the channel count adds measurements at unchanged
per-channel noise; the information values across dimensions are therefore
not normalized measurements of improved design quality.

The bounded independent run completed in about 0.37 seconds with one BLAS
thread, Python 3.13.11, NumPy 2.5.3 and SciPy 1.18.1. The report includes:

| Check | Count |
| --- | ---: |
| Independent covariance constructions in the tiny sweep | 32 |
| Local information comparisons | 193 |
| Normalized residual spectrum comparisons | 184 |
| Exhaustive and independent-DP comparisons | 32 |
| Bounded snapshot solver runs | 33 |
| Shared-block Liu binary identities | 67 |
| Block-gradient finite-difference checks | 56 |
| Binary tangent comparisons | 67 |
| Bounded continuous solver runs | 14 |
| Independent greedy candidate evaluations on saved probes | 328 |
| Single-exchange neighbors of saved schedules | 256 |

These include empty and full counts, a singleton, zero transition and zero
information, complete history, negative transition entries and nonnormal
matrices. Maximum covariance and local-information differences were
`2.22e-16` and `1.78e-15`; the greatest derivative discrepancy was
`2.64e-10`. The saved validation artifact's four window cases were also
reconstructed, with their true optima independently enumerated.

Both saved application schedules select indices `0,...,7`, corresponding to
times `0.5,...,4.0`. An independent greedy construction selects those same
times, and none of the 128 single-exchange neighbors per case improves its
true information. Both independent dynamic programs visit 5,279 states,
confirming the state-count observation at fixed calendar width and count.

| Channels | Feasible true information | DP transferred upper | Liu upper |
| --- | ---: | ---: | ---: |
| 4 | 0.261018588612 | 0.262857957533 | 0.261652900714 |
| 16 | 1.545705598245 | 1.556958717772 | 1.548885734152 |

The information gaps reported by the source note reconstruct. The Liu upper
bound is tighter in both examples, and the dynamic program does not improve
the greedy schedule. These application cases were not exhaustively enumerated
over true information, so global optimality of the common schedules remains
unproved. The useful demonstrated capability is the correct block
implementation and the state count's independence from the block dimension.
It does not establish superior application performance or novelty.

Cap behavior is consistent with the documented numerical scope. Mocked
covariance allocation proves that snapshot memory refusal and an already
expired initial deadline occur before covariance construction, with null
bound fields. An injected interruption during the DP retains only the true
baseline bounds and no surrogate optimum or transferred certificate. An
interrupted Liu solve retains its true baseline bounds. Array-workspace
preflights and checks between numerical operations are not process memory
limits or hard wall-clock limits. Some comparator preflight errors propagate
to the probe's exception wrapper, which records them before atomic JSON
replacement. No cap or exception occurred in the saved probes.

Ordinary floating-point factorizations, eigenvalues, optimizer tolerances and
DP comparisons qualify all these results. This review found no incorrect
reported bound or covariance/sensitivity calculation in the tested domain.
It provides neither interval validation nor an exact rational certificate.
No MIP or new large benchmark was run, and the saved local timings were not
treated as statistically controlled comparisons.

Reproduce the independent review from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/review_block_snapshot_design.py
```
