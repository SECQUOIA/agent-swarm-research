# Independent review of the compact minimum-gap numerical producer

The compact calendar oracle and numerical hull producer pass this independent
review. No incorrect feasible selection, local information matrix, or numerical
surrogate upper bound was found. No production code was changed.

The reviewed source is
[`noisy_markov_spacing_design.py`](../code/research_20260912/noisy_markov_spacing_design.py),
SHA-256 `64a0b7679850c239a46d6b2f1387701d61fe7438e46736eb2f52ddee2eb36d98`.
The author was not involved in constructing the reference implementation or
choosing these checks. The numerical producer does not supply a global bound
for the true likelihood: both `true_upper_bound` and `true_gap` remain null.
The separate exact spacing certificate is outside this review's scope.

## Code and mathematical audit

For information window length \(L\), minimum calendar gap \(g\), and horizon
\(n\), the producer retains
\[
 w=\max\{\min(L,n-1),\min(g-1,n-1)\}
\]
previous bits. This retains the cooldown when the information window is
shorter than \(g-1\). Mask generation constructs only bit sets whose positions
are at least \(g\) apart. Shifting a valid mask preserves this condition. A
choose arc is allowed exactly when the previous \(g-1\) positions are empty.
Thus every complete path satisfies the minimum gap, and every feasible
calendar subset has a unique path. The count layer imposes exactly \(k\)
selections.

At stage \(t\), let \(a\) be the age of the most recent retained selection,
and let `wait` be \(\max(0,g-a)\), or zero if cooldown has expired. The earliest
remaining feasible selection is \(t+\text{wait}\), so the maximum remaining
count is
\[
 \max\left(0,\left\lceil\frac{n-t-\text{wait}}{g}\right\rceil\right).
\]
The implemented pruning rule uses this quantity and therefore removes only
states that cannot reach the required count. It does not assume nonnegative
arc scores.

For a choose arc, only selected predecessors within the information window
enter the conditional regression. Its matrix is the outer product of the
adjusted mean sensitivity divided by the conditional variance. Summing these
matrices with the prior gives the stated finite-window surrogate information.
The prefix-mask restriction correctly excludes bits corresponding to times
before the calendar starts. The special cases \(L=0\), \(g=1\), \(k=0\),
\(g\ge n\), and \(L\ge n-1\) follow the same transitions. Full history
reproduces the true information on every feasible subset.

The fully corrective producer retains nonnegative weights summing to one and
feasible exact-count support paths. Each tangent upper bound uses a positive
definite reference matrix and a complete linear pricing solve. The true
incumbent is evaluated with the selected dense covariance. Closing the
surrogate hull gap is reported as `surrogate_hull_optimal_tolerance`; this does
not claim integer optimality or close a true-likelihood bound.

The memory preflight runs before the seed objective or covariance allocation.
The reported estimate accounts for the principal arc, predecessor, action,
value, and covariance arrays and includes workspace allowances. It is an
allocation estimate, not a certified process RSS limit. Deadline checks are
cooperative checks around Python work and linear algebra calls; they cannot
interrupt an individual NumPy call. Time or correction failure preserves an
already available feasible incumbent and mixture. A refused memory preflight
returns no incumbent. These distinctions are represented in the returned
status and null fields.

## Independent checks

The review script is
[`review_noisy_markov_spacing_producer.py`](../code/research_20260912/review_noisy_markov_spacing_producer.py).
It forms explicit triangular conditional matrices using independently
constructed covariance entries and dense inverses. Its separate dynamic
program stores tuples of calendar indices and the most recent selection,
without using production masks, transitions, or remaining-capacity pruning.
For small problems, exhaustive subset enumeration checks the pricing optimum
and the surrogate objective bounds directly.

The saved report is
[`noisy-markov-spacing-producer-independent-review.json`](../code/research_20260912/results/noisy-markov-spacing-producer-independent-review.json).

| Check | Count |
| --- | ---: |
| Compact masks against unrestricted enumeration | 195 |
| Dense conditional information matrices | 4,933 |
| Exhaustive linear prices, including negative and nonsymmetric gradients | 1,005 |
| Producer outputs, including saved and interrupted results | 34 |
| Feasible support paths and information matrices | 57 |
| Independently priced tangent witnesses | 31 |
| Rejected malformed inputs | 27 |
| Memory, time, iteration, and correction failure checks | 6 |

There were 121 small model configurations with horizons up to nine,
positive and negative correlations, independent-noise cases, zero latent
variance, several variance ratios, a non-diagonal positive definite prior,
and every relevant count boundary. The largest absolute difference in an
information check was \(5.7\times10^{-14}\); the largest exhaustive pricing
difference was \(1.2\times10^{-13}\). Malformed-input checks include invalid
window or gap values, impossible counts, duplicate and out-of-range indices,
boolean indices, minimum-gap violations, and invalid resource limits.

The saved
[`noisy-markov-spacing-kinetics-probe.json`](../code/research_20260912/results/noisy-markov-spacing-kinetics-probe.json)
was also audited. Its source hash matches the reviewed producer, and the
review report additionally records hashes of imported source files and the
saved result. All six support paths have 32 observations separated by at
least two grid intervals. The mixture, incumbent, and tangent witness replay
against the independent covariance and tuple-state reference. The reported
surrogate hull value is `16.27647068886335`, its upper bound is
`16.276470833445167`, and the true feasible objective is
`16.27631933797835`. The author recorded 3.238 seconds and six pricing rounds.
This is one stylized kinetics case, not evidence of a general runtime ranking
or measured noise covariance.

Run the bounded review with:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 \
python code/research_20260912/review_noisy_markov_spacing_producer.py
```

The saved run took 5.26 seconds under Python 3.13.11, NumPy 2.5.3, and SciPy
1.18.1. These floating-point checks complement the code audit; they do not
replace exact outward bounds from the separate certificate implementation.
