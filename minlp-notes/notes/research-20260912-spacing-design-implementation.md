The isolated compact spacing producer closes the requested first case's
**surrogate hull** gap to `1.45e-7` in 3.24 seconds. It stores 610 calendar
masks, compared with 8,192 unrestricted masks at the same memory width. Its
true-evaluated feasible incumbent is `16.27631933797835`. The producer does
not report a transferred true upper bound; the independent minimum-gap
certifier consumes its saved data and hull matrix separately.

The implementation is
[`noisy_markov_spacing_design.py`](../code/research_20260912/noisy_markov_spacing_design.py).
It imports the reviewed log-determinant and simplex-weight refinement helpers
without changing the reviewed solver core. `SpacingCalendarOracle` generates
only masks whose set bits are separated by at least g. Its information window
is L; its state width is `max(L,min(g−1,n−1))`, so a short information window
cannot silently discard the sampling cooldown. Skip and choose transitions
use compact mask indices. Choose transitions are disabled until the minimum
gap is met. Local information uses genuine selected-history covariance
conditioning and the corresponding adjusted sensitivity.

The dynamic program adds an exact-count layer and recovers a complete path.
A count-capacity check prunes states that cannot supply enough remaining
spaced samples. All recovered paths and incumbents are checked for both exact
cardinality and minimum gap. The seed is evenly spaced and is checked as well;
the constructor rejects counts above `ceil(n/g)`. No unrestricted `2^L` array
is allocated, and the workspace preflight precedes covariance allocation.
The estimate includes compact arc matrices, predecessor/action arrays, two
value layers, covariance workspaces, and corrective workspaces. It is not an
operating-system RSS limit, since interpreter and library memory are additional.

`produce_spacing_hull` repeatedly prices log-determinant tangents and refines
the mixture over generated paths. Each completed pricing round records its
surrogate value and upper bound, true-evaluated incumbent, visited-state count,
and time. A time or iteration cap preserves completed numerical certificates.
The output deliberately leaves `true_upper_bound` and `true_gap` null; a
surrogate upper bound must not be interpreted as a true-likelihood bound
without the separate covariance approximation argument.

The first case uses the early-peak kinetics sensitivities from the
[smooth probe](research-20260912-noisy-markov-kinetics-probe.md): A0=1,
k1=0.7, k2=0.2, parameters `log(A0),log(k1),log(k2)`, and a fixed horizon 12.
There are n=96 candidate times `12*(j+1)/96`, k=32 selections, and minimum gap
g=2. Thus candidate spacing is 0.125 and the minimum physical sampling gap is
0.25 model time units. The latent AR coefficient is `sqrt(0.4)` rather than
0.4: its two-step correlation matches the earlier n=48 grid's one-step
correlation up to floating-point representation. This preserves the specified
physical covariance scale across that grid refinement. The selected count
still doubles relative to the n=48 probe, so this is not a same-budget
comparison. The latent and nugget variances remain 0.00125 each and the prior
is `0.01 I`. The covariance is stylized, not measured noise from a published
experiment.

At information memory L=13, the state width is also 13. The compact mask count
is 610; the count-layer upper bound is 1,932,480 states. Each pricing call
actually visits 510,939 states after prefix and count-capacity restrictions.
The workspace estimate is 16,656,904 bytes, or 15.89 MiB, within the 256 MiB
workspace limit. Six completed pricing rounds give:

| Round | Surrogate mixture value | Surrogate upper bound | True feasible value | Elapsed seconds |
|---:|---:|---:|---:|---:|
| 1 | 16.155084486 | 16.292801212 | 16.272714116 | 1.007 |
| 2 | 16.272892220 | 16.277638276 | 16.276168590 | 1.502 |
| 3 | 16.276318901 | 16.276605198 | 16.276319338 | 1.948 |
| 4 | 16.276456864 | 16.276545730 | 16.276319338 | 2.380 |
| 5 | 16.276470651 | 16.276477925 | 16.276319338 | 2.802 |
| 6 | 16.276470689 | 16.276470833 | 16.276319338 | 3.238 |

The final surrogate upper bound is `16.276470833445167`; the feasible mixture
value is `16.27647068886335`. The final mixture has three positive path weights,
so hull closure does not establish a discrete surrogate optimum. Subtracting
the true incumbent from this surrogate bound would also mix two different
objectives and is not a valid true gap.

The [first-case artifact](../code/research_20260912/results/noisy-markov-spacing-kinetics-probe.json)
contains the full input matrices, `minimum_gap`, L, selected indices and times,
mixture information, individual path matrices and weights, tangent witness,
and complete pricing history. Its schema includes the fields needed by the
separate `certify_spacing_design.py` implementation. Source SHA-256 is
`64a0b7679850c239a46d6b2f1387701d61fe7438e46736eb2f52ddee2eb36d98`.

The [validation report](../code/research_20260912/results/noisy-markov-spacing-design-validation.json)
passes eight small exhaustive cases. They include L=0, `L<g−1`, g=1, gaps
reaching the horizon, full history, and k=0. Information sums are compared with
independently assembled conditional-residual matrices, with maximum absolute
entry discrepancy `1.78e-15`. Linear prices, including indefinite gradients,
match exhaustive subset prices within `8.89e-16`. Generated surrogate bounds
enclose the enumerated discrete surrogate optima. Oversized workspace refusal
occurs without inventing an unevaluated lower bound. Independent oracle review
and gap-aware exact certification are separate from these numerical checks.

Reproduce from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_spacing_design.py validate
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_spacing_design.py first-case
```

The first-case invocation has a thirty-second cap and no solver parallelism;
the commands set BLAS to one thread. The observed run did not reach its cap.
The spacing graph and count dynamic program are classical constructions.
This single constrained case establishes a usable producer and compact state
representation, not priority, broad scalability, or a global true optimum.
