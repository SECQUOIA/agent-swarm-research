# Review of optional integer scoring in the spacing certifier

Date: 12 September 2026. Reviewer: `/root/spacing_bound_review`, which did
not author this integration or its scoring component. Verdict: accepted.
No author code was edited during this review.

The reviewed integration is
[certify_spacing_design.py](../code/research_20260912/certify_spacing_design.py),
SHA-256 `40ede634ef137af6a91b981fe6890427f48c8e108d7926f4c83d82fe04b4897c`.
This is a bounded extension of the
[earlier certifier review](research-20260912-spacing-certificate-independent-review.md).
The separately reviewed
[integer scoring component](research-20260912-integer-interval-scores-independent-review.md)
has SHA-256 `b558f1b03db3f195be8fd0fbab8741396dd75264ccbef2f3a65d98908a763c1d`.

The integration adds an optional positive integer `integer_grid` argument
and matching `--integer-grid` CLI option. With the argument omitted or set
to `None`, arc prices still use the earlier exact rational calculation.
With a positive grid, the component receives the same exact feature matrix,
the same corrected tangent weight `H=N^-1/(1-delta)`, and the same score
grid. Each distinct recent history is prepared from the existing exact local
coefficients and variance, in their matching chronological age order.
Subsequent arcs use that prepared pattern at their actual target time.

The component's accepted contract is an integer upper bound on the exact
arc price in the certifier's score units. The integration passes these integers
directly into the unchanged exact-count, minimum-gap pricing program.
Replacing each exact arc ceiling by a possibly larger integer preserves the
global objective upper bound. The spectral delta, reference matrix, feasible
incumbent, true incumbent information, and rational logarithm calculations
are unchanged. Coarse grids can weaken the upper bound; they do not change
its direction.

The option rejects zero, negative, Boolean, inexact, and noninteger grid
arguments. If a positive variance rounds down to zero on the requested grid,
the component's explicit refusal propagates to the caller. The integration
does not silently change arithmetic modes or return a certificate after that
failure. The CLI records the arithmetic mode, coefficient grid, feature grid,
component hash, and integration source hash.

## Independent integration checks

[The review script](../code/research_20260912/review_spacing_integer_integration.py)
passed the following checks, saved in
[its JSON report](../code/research_20260912/results/spacing-integer-integration-independent-review.json):

| Check | Number |
| --- | ---: |
| Small exact certificates | 90 |
| Certificates with coefficient grids `1`, `3`, or `10` | 54 |
| Default exact-rational certificates | 18 |
| Exhaustively priced feasible designs | 680 |
| Invalid integer-grid rejections | 7 |
| Zero rounded variance-floor rejection | 1 |
| CLI success and refusal checks | 2 |

These tests cover positive and negative correlations, zero memory, additional
cooldown memory, complete histories, singleton horizons, empty designs, and
large sampling gaps. The reference forms local conditionals by dense rational
covariance solves and feeds them to the independently accepted component.
It then enumerates feasible complete selections to check the integrated
integer maximum. This independently checks feature, tangent, coefficient,
age, variance, and score-grid forwarding as well as the pricing integration.
Exact dense true-information calculations and separate rational logarithm
enclosures check every tested objective upper bound.

The tests also verify that omitted and explicit `None` options return the
same mathematical results and metadata, apart from runtime. CLI checks
verify the recorded grids and file hashes, and confirm that a refused grid
does not create an output artifact.

## Composition with the large independent replays

The large exact certificate had already passed a dense rational and
tuple-history replay. The scoring component had separately checked all
31,900 reachable arcs and 377 conditional patterns on that same hashed
96-candidate problem, and independently priced both sets of arc weights.
This integration review reuses those accepted results rather than repeating
the expensive exact calculations.

The review compares the
[new integer certificate](../code/research_20260912/results/noisy-markov-spacing-kinetics-integer-certificate.json)
with the old exact certificate and both independent reports. All source and
input hashes match their respective reviewed versions. Problem data, delta,
tangent reference, incumbent, lower bound, grids other than the new integer
coefficient grid, and pricing-state metadata agree. The independently verified
integer maximum increases from `299934500` to `299934501`. The certificate's
exact objective upper bound and gap therefore increase by exactly
`1/100000000`, giving displayed gap `0.011557655731135803`.

The saved runs report about 1.087 seconds for the new complete certificate
and 36.609 seconds for the earlier rational version on this case. The review
did not repeat those timing runs. This is a comparison of two certificate
arithmetic implementations on one fixed instance, not a general solver
performance ranking or a novelty claim for interval arithmetic.

Reproduce the bounded integration checks from the project root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_spacing_integer_integration.py
```
