# Exact latent-separator certificates

Date: 2026-09-12. The [separator theory](research-20260912-latent-separator-design.md)
has passed [fresh mathematical review](research-20260912-latent-separator-independent-review.md).
The exact implementation passed a
[separate fresh review](research-20260912-latent-separator-certificate-independent-review.md).
All 3,693 assertions passed, including independent rational conditional
inverses, exhaustive tiny bounds, malformed inputs and two replay routes for
all five saved certificates. No implementation correction was needed. These
certificates apply to the original selected-covariance objective, without a
finite-history error correction.

The [certifier](../code/research_20260912/certify_latent_separator.py) accepts
an arbitrary positive definite reference and an arbitrary nuisance matrix from
the numerical producer. It independently validates the incumbent and recomputes
every quantity needed for its global bound. Neither convergence of the producer
nor accuracy of its stored objective and price is a certificate assumption.
JSON decimals define exact rational sensitivity data; this does not certify
uncertainty in the physical model or roundoff in generating those sensitivities.

## Certificate construction

With the block partition and latent anchors in the theory note, let `H` be the
conditional latent mean loading, `D` the block diagonal residual covariance,
and `K_A` the anchor covariance. For any `W` positive definite and any `G`,

```text
log det J(S) <= -log det W - p + tr(W J0)
             + tr(W G^T K_A^-1 G)
             + sum_blocks tr[W (F_Sb+H_Sb G)^T D_SbSb^-1 (F_Sb+H_Sb G)].
```

The inequality follows by evaluating the variational Schur quadratic at `G`,
then applying the log-determinant tangent with weight `W`. The implementation
symmetrizes and rounds the proposed Schur reference to an exact rational matrix
`N`, verifies positive definiteness, and sets `W=N^-1`. It rounds `G` on the
same grid; no optimality equation for `G` is required. All physical covariance
parameters and anchor loadings remain exact.

The anchor prior quadratic uses the scalar Markov precision formula. Local
conditional innovation coefficients come from exact scalar bridge filtering.
A depth-first enumeration retains only the current ancestors' exact filter
states. Prepared integer intervals are reused across blocks with the same
conditional covariance. The reviewed
[integer interval scorer](research-20260912-integer-interval-scores.md)
rounds every innovation score upward. Adding those scores bounds each complete
local pattern. An integer dynamic program first selects the best pattern for
each local count and then enforces the exact global cardinality.

The feasible lower bound uses the original full selected scalar filter and
a rational determinant/logarithm enclosure. The reference and coefficient grids
are `10^8` and `10^12`; the feature grid is `10^18`, the score grid is `10^8`,
and final log bounds are rounded outward on `10^12`. Invalid inputs, a reference
that fails the exact SPD check, insufficient variance-grid resolution, or an
exceeded pattern cap cause explicit rejection. The certificate has no deadline;
its recorded runtime is additional to design generation.

## Saved results

All cases use the same fixed physical covariance and 16 observations described
in the [grid benchmark](research-20260912-fixed-physical-grid-benchmark.md).
The 48-point certificate uses the separator's own incumbent. At 96 and 192
points, the saved shared greedy/exchange incumbent is better and is re-evaluated
exactly. The serialized fractions, selected schedule, rounded witnesses, integer
prices, input hashes and dependency hashes are retained in every artifact.

| Candidates | Block size | Exact feasible lower bound | Exact global upper bound | Exact log gap | Certificate seconds |
|---:|---:|---:|---:|---:|---:|
| 48 | 8 | 14.925507606504 | 15.005243683880 | 0.079736077376 | 0.047 |
| 96 | 12 | 14.945662679078 | 15.051419395187 | 0.105756716109 | 0.872 |
| 96 | 16 | 14.945662679078 | 15.025970711361 | 0.080308032283 | 16.147 |
| 192 | 12 | 14.953046919008 | 15.139311234872 | 0.186264315864 | 1.238 |
| 192 | 16 | 14.953046919008 | 15.110331327215 | 0.157284408207 | 20.587 |

Artifacts:
[48, b=8](../code/research_20260912/results/latent-separator-n48-b8-certificate.json),
[96, b=12](../code/research_20260912/results/latent-separator-n96-b12-certificate.json),
[96, b=16](../code/research_20260912/results/latent-separator-n96-b16-certificate.json),
[192, b=12](../code/research_20260912/results/latent-separator-n192-b12-certificate.json),
and [192, b=16](../code/research_20260912/results/latent-separator-n192-b16-certificate.json).

Adding the numerical generation and charged shared setup/greedy times gives
accounted totals of about 2.720 and 24.295 seconds for the 96-point blocks of
12 and 16; the corresponding 192-point totals are 5.511 and 38.023 seconds.
These sum separate saved measurements, not newly measured pipeline runs.
In particular, the 192-point `b=16` numerical solve fits its 30-second budget,
but generation plus exact certification exceeds 30 seconds. Certifying all
tested block sizes costs more than any single row and is not charged as one
preselected algorithm configuration.

The method improves the recorded 192-point upper bound over the tested dense
OA and unfinished calendar runs. It misses the 0.01 log-gap target. At 96
points, the refined calendar diagnostic gives a tighter numerical upper bound;
its numerical gap is about 0.03710. Dense MIP bounds in that benchmark are
solver-numerical, whereas the separator bounds above have rational witnesses.
There is no claim that every dense formulation or branching strategy is worse.

## Reproduction

From the repository root, reproduce the 48-point certificate with:

```sh
uv run --project code/research_20260912 python code/research_20260912/certify_latent_separator.py code/research_20260912/results/latent-separator-n48-probe.json /tmp/latent-separator-n48-certificate.json
```

For the 192-point `b=16` certificate and its saved shared incumbent:

```sh
uv run --project code/research_20260912 python code/research_20260912/certify_latent_separator.py code/research_20260912/results/latent-separator-n192-larger-blocks.json /tmp/latent-separator-n192-certificate.json --case 1 --selected 9 14 20 27 38 49 59 69 79 92 122 140 154 167 179 191
```

Use `--case 0` for `b=12`. The 96-point larger-block input uses the selection
`4 6 9 13 18 24 29 33 38 45 61 70 77 83 89 95`. The mathematical result fields
reproduce exactly; timing and optional incumbent-provenance metadata differ.

The certificate is a verification component for the specialized separator
relaxation. Exact arithmetic, Schur identities and block-pattern pricing are
established tools. The [priority audit](research-20260912-latent-separator-priority-audit.md)
restricts the remaining candidate contribution to the specialized hierarchy
and demonstrated strengthening/cost tradeoff.
