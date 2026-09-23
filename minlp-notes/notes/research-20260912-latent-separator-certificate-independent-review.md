# Independent review of exact latent-separator certificates

Date: 2026-09-12. The exact integration in
[certify_latent_separator.py](../code/research_20260912/certify_latent_separator.py)
is accepted for its stated stationary scalar model and cardinality constraint.
No change to the certifier was required. This review covers implementation and
the five saved exact certificates; the
[independent theory review](research-20260912-latent-separator-independent-review.md)
establishes the underlying bound. It makes no additional novelty claim.

The reviewed certifier has SHA-256
`239276bf6b71542af40441f928f39af502f615618761c44a1923d95679b6ff68`.
The separate
[review script](../code/research_20260912/review_latent_separator_certificate.py)
and [machine-readable report](../code/research_20260912/results/latent-separator-certificate-independent-review.json)
record 3,693 passing assertions, including both complete replay modes for all
five saved certificates. The full review took 78.743 seconds with BLAS thread
counts set to one. This is review time, separate from the certificates' recorded
generation times.

The expected small-case values come from independently constructed dense
rational covariance matrices. The reviewer forms `K_A`, computes
`H=K_:A K_A^-1`, and directly inverts selected submatrices of
`D=K+rI-H K_A H^T`. It does not use the producer's conditional-variance,
quadratic, information, or logarithm helpers to obtain expected results.
It uses the separately accepted `IntegerIntervalScores` component to check
the certifier's integration with that component, without repeating its entire
standalone review.

The implementation preserves the conditions needed by the accepted bound.
It symmetrizes and rounds the proposed reference, checks the resulting rational
`N` for positive definiteness, and computes `W=N^-1` exactly. The original
proposal need not be an optimal tangent. Rounded `G` is arbitrary and need not
satisfy a nuisance minimization equation. Direct anchor-covariance inversion
agrees with the sparse anchor-prior quadratic, and the parameter prior and
anchor prior each occur once. The adjusted sensitivities use `F+HG`, including
at anchor-time observations.

The exact bridge recursion agrees with dense conditional regression for every
tested pattern. Each depth-first entry has its predecessor available before
its score is accumulated; every nonempty local subset occurs exactly once.
The cached patterns depend on the block length and bounding-anchor geometry,
while evaluation uses the block's actual adjusted sensitivity rows. Summing
upward-rounded innovation scores gives an upper bound for a complete local
pattern. The count program then chooses exactly one pattern per block with
total cardinality `k`. The logarithm of the reference determinant is enclosed
upward, the feasible determinant is enclosed downward, and the final objective
rounding preserves those directions. No covariance truncation is present.

The finite checks cover the following distinct contracts:

- 156 exact bridge coefficient and variance comparisons, 156 outward arc
  integration checks, and 156 complete pattern scores checked against dense
  selected conditional inverses.
- 740 independent selected-information comparisons and 740 arbitrary-`G`
  trace-majorization checks over all subsets of the small instances.
- 52 complete cardinality support comparisons against exhaustive enumeration,
  304 local count maxima, 258 feasible true-objective upper-bound comparisons,
  and 52 incumbent lower bounds checked with independent rational logarithm
  enclosures.
- Positive, negative, zero, and near-unit signed correlation; zero latent
  variance; one candidate; singleton blocks; no anchors; empty selected blocks;
  unequal final blocks; and `k=0`, an interior cardinality, and `k=n`.
- Asymmetric proposed references before symmetrization; arbitrary signed
  nuisance entries; coarse and nondecimal reference, coefficient, feature,
  score, and log grids; and 52 exact JSON serialization/replay checks.
- Rejection of invalid dimensions, nonpositive-definite priors or rounded
  references, invalid covariance parameters, inexact floating API data,
  malformed selections and witnesses, invalid grids, insufficient variance
  resolution, and exceeded pattern caps. Oversized block proposals correctly
  clamp to the candidate count.

All five saved certificates reproduce every mathematical result field from
their original proposal files. They also reproduce from their own frozen
problem data, rounded reference, rounded nuisance matrix, and incumbent,
without needing the numerical producer. The n48 command-line invocation was
run separately and its mathematical payload matches the saved artifact.
All input, certifier, dependency, and optional incumbent-source hashes match.
For n96 and n192, the selected schedules match the saved shared greedy/exchange
incumbents, and the exact rational problem data match the benchmark.

The large incumbent objectives were additionally recomputed using an
independent exact tridiagonal solve based on the selected latent precision.
This calculation uses the identity
`R_SS^-1=r^-1 I-r^-2 (K_SS^-1+r^-1 I)^-1`, rather than the producer's
information-filter recursion. The same independent solver agrees with dense
selected covariance inversion in all 740 small subset checks. Dense rational
anchor-covariance inversion and independent rational logarithm enclosures also
verify the saved fixed terms and lower-bound directions.

| Candidates | Block size | Certified lower bound | Certified upper bound | Certified log gap |
|---:|---:|---:|---:|---:|
| 48 | 8 | 14.925507606504 | 15.005243683880 | 0.079736077376 |
| 96 | 12 | 14.945662679078 | 15.051419395187 | 0.105756716109 |
| 96 | 16 | 14.945662679078 | 15.025970711361 | 0.080308032283 |
| 192 | 12 | 14.953046919008 | 15.139311234872 | 0.186264315864 |
| 192 | 16 | 14.953046919008 | 15.110331327215 | 0.157284408207 |

The substantive claims and table in the
[author certificate note](research-20260912-latent-separator-certificates.md)
agree with the artifacts. Summing the saved generator wall time, benchmark
common setup, benchmark shared greedy time, and certificate time independently
gives 2.719978545 and 24.295445538 seconds for n96 with blocks 12 and 16;
the n192 totals are 5.510949291 and 38.022752706 seconds. These are sums of
separately measured runs. The n192 block-16 configuration therefore exceeds
30 seconds once certification is included. Charging every exploratory block
size would cost more than a single reported configuration.

At n192, both reviewed separator upper bounds improve on the recorded dense OA
and unfinished calendar bounds. At n96, the refined calendar diagnostic has
the smaller numerical upper bound, `14.989863478745855`, with its own reported
numerical gap `0.03709664527169387`. Those numerical comparison bounds are not
upgraded to rational certificates by this review. None of the five separator
certificates meets a 0.01 log-gap target.

The certificate applies to the exact rational data encoded by the JSON, with
`|rho|<1`, nonnegative latent variance, positive nugget variance, and a positive
definite parameter prior. Empty candidate or parameter matrices are rejected.
Zero latent variance or zero correlation uses no anchors. A grid that rounds
the reference out of positive definiteness or gives a zero variance floor is
rejected rather than certified. The computation has a pattern cap and no
deadline. These restrictions are explicit validity and resource conditions;
the certificate does not cover uncertainty in the physical model or establish
that the rounded sensitivities enclose the underlying continuous model.

Reproduce the review from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 code/research_20260912/.venv/bin/python code/research_20260912/review_latent_separator_certificate.py
```

No unresolved implementation or certificate issue remains within this scope.
