# Independent review of refined-pair certificate integration

**Accepted.** The optional refined-pair mode correctly implements the [reviewed scalar formulas](research-20260912-pair-refinements-independent-review.md), and the resulting delta is used consistently throughout the certificate. The default mode preserves the earlier arithmetic. The saved 96-candidate refined certificate replays with certified logdet gap **0.009725584617148928**, rounded for display.

This bounded review examined the new `refined_pairs=False` keyword in [noisy_markov_spacing_bound.py](../code/research_20260912/noisy_markov_spacing_bound.py) and [certify_spacing_design.py](../code/research_20260912/certify_spacing_design.py), its CLI flag, and the [new artifact](../code/research_20260912/results/noisy-markov-spacing-kinetics-refined-certificate.json). The reviewer authored the preceding mathematical review but did not author or modify these implementations.

The [checker](../code/research_20260912/review_refined_spacing_integration.py) and [results](../code/research_20260912/results/refined-spacing-integration-independent-review.json) retain the evidence and source hashes. Reviewed hashes are:

| File | SHA-256 |
|---|---|
| `noisy_markov_spacing_bound.py` | `a8bdac20548764c11bdd29b476c4a37722af088aa63af0b0e29b46d5d0b08371` |
| `certify_spacing_design.py` | `19341e7ba06816d12eefdb67299481fdacd9aaaa55c67df85ef17aaf5aa07a17` |
| `integer_interval_scores.py` | `b558f1b03db3f195be8fd0fbab8741396dd75264ccbef2f3a65d98908a763c1d` |

## Formula and integration checks

In refined mode, the helper uses the far coefficient \(P\) and near coefficient \(P\kappa(1-\kappa)\), with \(\kappa=P/(P+r)\). It retains the original spacing progression, row-pricing recurrence, and local innovation floor. Negative correlation is handled through its magnitude. Its stationary scalar API is consistent with the stronger near bound's assumptions.

The keyword defaults to `False`. The original far coefficient and near coefficient are unchanged in that mode; introducing a named near coefficient only changes expression organization under exact rational arithmetic. Nonboolean values are rejected, including in cases that would otherwise return an exact zero bound.

The certifier forwards the flag to the helper. It uses the returned delta in both

\[
N=\operatorname{round}\left[J_0+\frac{\operatorname{sym}(M)-J_0}{1-\delta}\right],
\qquad H=\frac{N^{-1}}{1-\delta}.
\]

Thus the change affects both the tangent reference and the linear arc prices. The existing positive-definiteness check on \(N\), rejection of \(\delta\ge1\), lower-bound calculation, and exact objective assembly remain intact. `pair_majorant` records the selected mode. The CLI's `--refined-pairs` switch reaches the same path and can be combined with `--integer-grid`.

## Independent checks

The helper reference uses explicit enumeration of separated distance sets, together with the previously reviewed dense conditional calculations. Small certificate references form rational covariance matrices, compute local conditionals independently, and enumerate every feasible design. For integer interval scores, this review reuses the separately accepted scoring component but supplies its matrix \(H\), coefficients, and variances independently of the certifier's mask implementation.

| Check | Count |
|---|---:|
| Helper/formula comparisons in both modes | 264 |
| Exact normalized-covariance spectral sandwich matrices | 2,320 |
| Small exact certificates | 85 |
| Exhaustively enumerated design bounds and prices | 340 |
| Implicit-default versus explicit-`False` certificate equalities | 42 |
| Nonboolean-mode rejections across helper and certifier | 18 |
| CLI modes with decimal input and provenance checks | 2 |
| Saved 96-candidate integer artifact replays | 2 |

The suite includes zero latent variance, zero correlation, negative correlation, one candidate, zero memory, complete history, minimum gaps larger than the horizon, empty schedules, and cooldown longer than the information window. Exact and integer-interval scoring are both exercised, including a coarse interval grid and asymmetric tangent sources.

One additional boundary case confirms that the flag changes the positive-relative-bound decision. For five candidates, \(P=r=1\), \(\rho=3/4\), \(g=L=1\), the original delta exceeds one and the default certifier rejects the request. Refined mode has delta \(9/11<1\), returns a certificate, and passes exhaustive comparison with every feasible size-two design.

## Saved artifact and preserved default behavior

The earlier [integer certificate](../code/research_20260912/results/noisy-markov-spacing-kinetics-integer-certificate.json) was regenerated through the default mode. Every common numerical and structural field matched exactly, including its tangent matrix, integer price, bounds, selections, and state counts. Its stored source hash identifies the earlier implementation; the new review retains the current source hashes. The added mode-description field does not change those numerical results.

The refined artifact was regenerated using `refined_pairs=True` and integer coefficient grid \(10^{12}\). Its exact data, tangent reference, integer price, bounds, and other deterministic fields matched. Its input-file, certifier, and interval-component hashes were verified. The tangent reference and the upper-bound assembly were also reconstructed independently from the saved delta and source matrix.

| Quantity | Original integer mode | Refined mode |
|---|---:|---:|
| Delta | 0.003795597732542757 | 0.003186913253976541 |
| Integer price on the \(10^8\) score grid | 299934501 | 299934459 |
| Certified logdet gap, displayed | 0.011557655731135803 | 0.009725584617148928 |

The original rational certificate's gap was 0.011557645731135803; the distinction of \(10^{-8}\) from the original integer mode is the previously reviewed outward interval-price increase. The refined artifact retains the same exact problem data, incumbent, and lower bound as that original rational certificate.

The bounded replay used the accepted integer pricing implementation for the large artifact. It did not repeat the earlier 31,900-arc dense rational replay. Correctness of that unchanged pricing/scoring machinery relies on the [certifier review](research-20260912-spacing-certificate-independent-review.md), its independent artifact replay, and the retained [integer-component review results](../code/research_20260912/results/integer-interval-scores-independent-review.json). The component hash matches the one reviewed there. Small exhaustive pricing checks in this review specifically verify the new delta's propagation into that machinery.

The refined replay took about 1.10 seconds on this run. This is certificate regeneration time, excluding numerical optimization, and is not an end-to-end solver comparison. No defect was found within the integration scope.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
  code/research_20260912/review_refined_spacing_integration.py
```
