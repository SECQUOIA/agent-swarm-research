# Exact design certificates with a minimum sampling gap

Date: 12 September 2026. Status: the bound and numerical producer passed fresh
independent review. Exact certificate integration and the larger saved certificate have also
passed [fresh review](research-20260912-spacing-certificate-independent-review.md).

The [spacing theorem](research-20260912-noisy-markov-spacing.md) tightens the
uniform local-history error bound by using the minimum sampling gap. The
[compact producer](research-20260912-spacing-design-implementation.md) stores
only feasible recent-history masks. Its
[fresh review](research-20260912-spacing-producer-independent-review.md) checks
local information, pricing, feasible mixtures, early exits and saved outputs.

`code/research_20260912/certify_spacing_design.py` independently recomputes
the objective certificate from the saved decimal model. It validates the
incumbent's cardinality and minimum gap, computes the exact spacing error
constant, and uses an arbitrary rational SPD reference in the prior-aware
logdet tangent. Exact local conditionals give nonnegative arc scores; upward
integer rounding and a longest-path calculation give a rigorous upper price.
The integer price includes the same sampling-gap constraint as the theorem.

The dynamic program retains `max(L,min(g-1,n-1))` history bits. Only the latest
`L` bits enter the information calculation. The additional bits, when needed,
prevent a new observation before the minimum gap expires. Empty designs,
one-observation horizons, and `L=0` still obey that constraint. The reported
state bound includes the initial state and all later layers. It is a count
bound, not a hard bound on Python process memory.

## First achieved constrained certificate

The first case uses the early-peak consecutive-reaction sensitivities described
in the [kinetics probe](research-20260912-noisy-markov-kinetics-probe.md), with
96 candidates on `(0,12]`, 32 selected observations, and a minimum gap of two
calendar positions. The saved latent correlation is the exact decimal
`0.6324555320336759`, chosen as a floating approximation to `sqrt(0.4)`.
This approximately preserves the physical latent correlation scale of the
48-candidate probe while refining the candidate grid. The selection budget
is different: 32 observations here versus 16 in that earlier probe.

| Quantity | Value |
|---|---:|
| Information window | 13 positions |
| Feasible history masks | 610 |
| Unrestricted 13-bit masks | 8,192 |
| Producer workspace estimate | 15.89 MiB |
| Producer time | 3.238 s |
| Numerical surrogate hull gap | 1.45e-7 |
| Exact certified true-objective gap, rounded upward | 0.01155765 |
| Exact certificate generation time | 36.609 s |

The exact gap concerns the saved rational covariance and sensitivity data.
The true selected logdet is approximately `16.27631934`; the certificate
bounds the optimum over every size-32 subset satisfying the gap. Closing the
surrogate hull gap does not establish an exact discrete optimum.

Independent replay checks all 31,900 arc prices with dense rational local
conditionals and a separate tuple-history recurrence. It reproduces integer
price `299934500` and verifies the exact incumbent and logarithm bounds.
The tiny suite separately checks 1,100 certificates and 5,909 exhaustive
subset comparisons.

The increased rational cost is material. The decimal correlation creates
long fractions in each local conditional and spectral correction. The
certificate remains correct, but it is substantially slower than the numerical
producer in this first implementation. The [outward integer-interval component](research-20260912-integer-interval-scores.md)
has passed fresh independent review. Its integrated mode reduces the full
certificate time to **1.087 seconds**, while increasing its exact upper bound
by only `1e-8`; the gap becomes `0.011557655731135803`. Both arithmetic modes
use identical problem data, reference, error constant and incumbent lower
bound. The [separate integration review](research-20260912-spacing-integer-integration-review.md)
has accepted the new branch and metadata after 90 small certificates, 680
exhaustive design comparisons, refusal checks and the large-artifact comparison.

Files in `code/research_20260912/results/`:

- `noisy-markov-spacing-kinetics-probe.json`: complete numerical input and witnesses.
- `noisy-markov-spacing-kinetics-certificate.json`: direct rational arc calculation.
- `noisy-markov-spacing-kinetics-integer-certificate.json`: outward integer-interval
  arc calculation, with its exact model, reference, price, selections and bounds.

Reproduce the exact certificate from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_spacing_design.py code/research_20260912/results/noisy-markov-spacing-kinetics-probe.json code/research_20260912/results/noisy-markov-spacing-kinetics-certificate.json
```

The numerical producer has no global true-upper-bound field; the exact
certificate supplies that separate result. These files preserve both the
practical gain from compact history states and the current arithmetic cost.

The fast mode is explicit so the earlier direct rational run remains reproducible:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_spacing_design.py code/research_20260912/results/noisy-markov-spacing-kinetics-probe.json code/research_20260912/results/noisy-markov-spacing-kinetics-integer-certificate.json --integer-grid 1000000000000
```

The interval grid controls rounding loss, and every rounded score remains an
upper bound. A variance whose lower grid endpoint is not positive is rejected;
the caller must use a finer grid. The source and grid settings are retained in
the certificate. The accepted component's full independent replay includes
all 31,900 saved arcs and reconstructs the one-unit integer-price increase.

## Refined stationary pair bound

The [freshly reviewed pair refinement](research-20260912-pair-refinements-independent-review.md)
removes an unnecessary far-pair regression factor and uses the first local
Kalman gain to tighten near pairs. The optional `--refined-pairs` mode applies
these formulas to the same stationary scalar model. Its implementation passed
[separate independent review](research-20260912-refined-spacing-integration-review.md),
including exact spectral checks, small exhaustive certificates, both CLI modes,
and exact replay of the original and refined artifacts.

On the saved 96-candidate problem, delta decreases from
`0.003795597732542757` to `0.003186913253976541`. Recomputing the tangent
reference and all prices gives an exact gap of `0.009725584617148928`,
about 15.85% below the previous integer-interval certificate. Certificate
generation took 1.088 seconds. The input, feasible incumbent and its lower
bound are unchanged. This improves the guarantee for that incumbent; it
does not demonstrate a better chosen schedule.

The new artifact is `noisy-markov-spacing-kinetics-refined-certificate.json`.
The earlier modes remain available for reproducing their saved results:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_spacing_design.py code/research_20260912/results/noisy-markov-spacing-kinetics-probe.json code/research_20260912/results/noisy-markov-spacing-kinetics-refined-certificate.json --integer-grid 1000000000000 --refined-pairs
```
