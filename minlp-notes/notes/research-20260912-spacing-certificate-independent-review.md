# Independent review of the minimum-gap design certifier

Date: 12 September 2026. Reviewer: `/root/spacing_bound_review`, which did
not author the certifier. Verdict: accepted for its stated exact rational
model, subject to the positive relative-bound condition `delta<1`. The
numerical optimization producer is outside this review's scope.

Reviewed implementation:
[certify_spacing_design.py](../code/research_20260912/certify_spacing_design.py),
SHA-256 `b0bb6aa2cecd328a1e860cd8f4d7a132e9d0f85e55efe137b9c312c93ba49484`.
It imports the [accepted spacing bound](research-20260912-noisy-markov-spacing-independent-review.md)
and the already reviewed exact rational primitives. Their hashes are stored
in the [review result](../code/research_20260912/results/spacing-design-certificate-independent-review.json).
The reviewer made no edits to author code.

## Constraint and pricing review

The incumbent checks enforce exactly `k` distinct integer indices in the
horizon, then enforce each consecutive gap after sorting. The parameter
check `k<=ceil(n/g)` is the exact maximum possible cardinality. Invalid
incumbents are rejected before any certificate is returned.

At candidate time `t`, mask bit `a-1` records a previous selection at age
`a`. The retained width is

```text
max(L, min(g-1,n-1)).
```

The lower `L` bits alone determine the true local conditional. The lower
`min(g-1,width)` bits determine whether selection at `t` is forbidden. Thus
cooldown survives even when `L<g-1`, while irrelevant old observations do
not enter the information approximation. A gap exactly equal to `g` is
allowed. Clipping the cooldown width to `n-1` is valid because no two
candidate times differ by more than `n-1`.

The dynamic program starts with zero selected observations and an empty
history. Both skip and choose transitions shift the existing history by one
position; choose sets the new most recent bit. Each transition preserves the
gap condition. Merging paths with equal time, count, and retained mask is
valid: future feasibility depends only on cooldown, and future scores depend
only on the information history. The skip pruning uses an upper bound on
remaining capacity, so it cannot discard a feasible complete selection.
Only terminal states with exactly `k` selections enter the maximum.

Local regression coefficients are computed with chronological negative ages
and a fresh unconditional initial variance. Their sensitivities refer to the
actual past indices `t-age`. Reachable masks cannot refer before the start
of the horizon. The conditional cache can depend only on the recent mask
because the covariance is stationary; the score cache also includes `t`
because sensitivities vary with time.

Each exact rational arc price is rounded upward to an integer multiple of
`1/score_grid`. The terminal integer maximum is therefore a valid upper
bound on the exact linear pricing problem. The total excess on a fixed
nonempty path is strictly less than `k/score_grid`. The reported priced
selection is feasible and attains the reported integer maximum.

## Objective and artifact review

The certifier obtains the accepted spacing-dependent variance floor and
spectral delta, and rejects `delta>=1`. Let `W(S)` be the surrogate data
information. The accepted theorem gives

```text
J_true(S) <= J0 + W(S)/(1-delta).
```

The supplied information matrix is only a way to choose a tangent reference.
It is symmetrized, transformed using delta, rounded exactly to a rational
grid, and required to be positive definite. It need not represent an optimal
or even feasible hull mixture. For the resulting positive definite `N`,
monotonicity and concavity of log determinant give the upper bound

```text
logdet(N)-p+tr(N^-1 J0)
    + max_feasible_S tr[N^-1 W(S)/(1-delta)].
```

The exact integer pricing maximum bounds the last term from above. The
reviewed rational logarithm enclosure bounds `logdet(N)` from above. The
lower bound independently evaluates the incumbent's true selected covariance
information and encloses its log determinant from below. A negative final
gap raises an error instead of returning a certificate.

The artifact contains exact sensitivities, prior, covariance parameters,
cardinality, gap, window, tangent reference, selected incumbent, priced
selection, integer price, and rational bounds. These suffice to reconstruct
the stated mathematical certificate without trusting numerical solver
statuses. The CLI reads JSON decimal numbers as exact rational decimal data
and records the input file hash, selected case and hull indices, and source
hash. This interpretation certifies the recorded decimal problem; it does
not enclose a separate unknown physical or floating-point input model.

## Independent verification

[The independent script](../code/research_20260912/review_certify_spacing_design.py)
uses dense rational covariance matrices and exact elimination to compute
local regressions and true information. It enumerates all feasible subsets
and sums their rounded arc prices directly. It does not reproduce the
author's mask dynamic program or use the author's Kalman recursion as its
reference. A separate rational logarithm series from the earlier independent
review checks the objective inequalities.

All checks passed:

| Check | Number |
| --- | ---: |
| Exact certificates | 1,100 |
| Exhaustive feasible-subset true-objective comparisons | 5,909 |
| Exhaustive feasible-subset integer-price comparisons | 5,909 |
| Certificates needing additional cooldown memory | 465 |
| Empty-design certificates | 353 |
| Expected `delta>=1` rejections | 132 |
| Malformed-input rejections | 25 |
| State-cap boundary checks | 2 |
| CLI decimal interpretation and artifact replay | 1 |

The suite covers horizons `1,2,4,6,7`, positive and negative correlations,
strong correlation with small nugget, zero latent variance, `g=10^6`, zero
memory, windows exceeding the horizon, and every feasible cardinality in
its selected parameter grid. Additional cases cover one and three mean
parameters and asymmetric tangent sources. Coarse score and reference grids
exercise outward price rounding and reference rounding explicitly.

The CLI check writes actual decimal JSON numbers, chooses a nondefault case
and hull, and reconstructs exact input fractions from the emitted artifact.
It independently replays the price and objective bounds and verifies the
recorded file hashes and indices. Every tested visited-state count is at
most the reported state-count bound.

Reproduce from the project root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_certify_spacing_design.py
```

## State cap and implementation limits

The initial code reported `n*(k+1)*mask_count` while its visited-state counter
also included the initial state. For `k=0`, the counter is `n+1`, one above
that expression. The author corrected the bound before the reported suite
to `1+n*(k+1)*mask_count`. This affected accounting and the preflight cap,
not the objective or pricing mathematics.

The state-count cap bounds possible time/count/mask states, including the
initial state. It is not a bound on bytes or total process memory: paths,
input matrices, cached fractions, and integer numerator sizes also consume
memory. The cap is conservative because it counts many unreachable states.
The method can reject trivial small-cardinality problems when its
cardinality-independent delta is too large; such rejection returns no false
certificate.

One optional resource improvement remains: the exact separated-mask count
is evaluated before testing the cap. The count is at least `width+1`, from
the empty mask and singleton masks. An early check using this lower bound
would avoid unnecessary combinatorial counting for clearly oversized
horizons and windows. This does not affect the accepted objective bound.

No additional literature was identified during this implementation review.

## Independent replay of the 96-candidate kinetics artifact

The [saved kinetics certificate](../code/research_20260912/results/noisy-markov-spacing-kinetics-certificate.json)
also passed an independent mathematical replay. It has `n=96`, `p=3`,
`k=32`, `g=2`, and `L=13`, with certified logdet gap
`0.011557645731135803` when displayed as a float.

[The replay script](../code/research_20260912/review_spacing_certificate_artifact.py)
reads the artifact's exact problem data and tangent reference. Its pricing
algorithm uses a recursive suffix search with tuples of past calendar times,
including a separate spacing-based bound on the number of remaining choices.
It uses no bit masks. Local regressions use dense rational normal equations.
The incumbent's exact true information uses one dense rational elimination
with all sensitivity columns as right-hand sides.

The replay visited 507,872 cached suffix states and independently computed
31,900 arc prices. It reproduced the integer maximum `299934500` exactly
and verified that the artifact's priced selection attains it. It also
reproduced the spacing innovation floor using a dense local conditional,
verified the incumbent and upper objective bounds, and matched the exact
problem data to the hashed producer input.

The independent logarithm enclosure first rounds its range-reduced argument
outward on a `10^24` grid, then applies its separate rational series. This
keeps the computation bounded while preserving exact inequalities. The
saved [replay result](../code/research_20260912/results/spacing-design-kinetics-certificate-independent-replay.json)
contains hashes, exact incumbent logarithm bounds, and the reproduced gap.
The run took about 37.26 seconds, including 35.42 seconds through pricing.
These are single-run replay times, not a solver performance comparison.
