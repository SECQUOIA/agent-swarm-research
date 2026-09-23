# Independent review of the exact partial-observation trace certificate

Date: 2026-09-12. Status: accepted. This fresh review found no defect in the
certifier or the four saved certificates. It verifies correctness for the
fixed two-mode model implemented here, not publication priority or an exact
discrete optimum.

Artifacts:

- [Reviewed certifier](../code/research_20260912/certify_partial_trace.py).
- [Independent checker](../code/research_20260912/review_partial_trace_certificate.py).
- [Independent report](../code/research_20260912/results/partial-trace-certificate-independent-review.json).
- [Reviewed partial-observation theorem, including its normalized refinement](research-20260912-partial-observation-independent-review.md).
- [Previously accepted integer interval component](research-20260912-integer-interval-scores-independent-review.md).

The checked certifier SHA-256 is
`35b19e7ef5abad8cd1eedfbfeb0ab13a2519f6f7c3236d871314ebf9d2a688df`.
No author source file was edited by this reviewer.

## Exact model correspondence

The implementation fixes latent transition `A=diag(2/5,1/5)`, observation row
`h=(3/5,4/5)`, stationary latent covariance `P=vI`, and independent measurement
variance `v>0`. Thus its scalar observation covariance is exactly

```text
R_ij = v [(9/25)(2/5)^|i-j| + (16/25)(1/5)^|i-j| + 1{i=j}].
```

In particular, `v` is each component's scale; the unconditional scalar
observation variance is `2v`. The certificate does not support arbitrary
latent transitions or an independent second variance parameter. Its saved
problem data explicitly record the fixed transition and observation row.

Starting the filter at its first used time with covariance `vI` is correct
by stationarity, even when the local-history indices are negative. Over a gap
`g`, the conditional state covariance update is

```text
P_next^- = A^g P_current^+ (A^g)^T + v[I-A^g(A^g)^T].
```

The process covariance in this expression is exactly the sum of the omitted
calendar innovations. The conditional mean propagates by `A^g`. Updating
with the current residual and gain is the usual Gaussian conditioning
identity, carried out here with rational arithmetic.

For local coefficients, the filter is fed independent coordinate vectors as
deterministic observation responses. Its prediction at the target is then
the row of regression coefficients. A zero target response makes its
innovation the negative of that row, explaining the final sign reversal in
`local_pattern`. For true information, the responses are the rows of `F`, so
the innovation responses are `F_t-b F_history`. Summing their outer products
divided by their exact innovation variances gives

```text
J(S) = J0 + F_S^T R_SS^-1 F_S.
```

The independent checker verified these identities by directly inverting the
dense rational mixture covariance above, without using either filter helper.

## Spectral constant and square-root rounding

The model's one-step process covariance is
`Q=v diag(21/25,24/25)`. Therefore

```text
Q >= (1-gamma^2)P,  gamma=2/5,
h P h^T = v,       s=1,
kappa=s/(1+s)=1/2.
```

These are exactly the intrinsic hypotheses of the separately reviewed
normalized partial-observation theorem. Its constant becomes

```text
delta = gamma^(L+1)/(1-gamma)
        + sqrt(1/2) sum_(h=1)^L sum_(d=L+1-h)^L gamma^(h+2d).
```

The author's finite geometric expression equals this double sum. Its
coefficient is rounded upwards on the integer grid `G=10^12`:

```text
c = ceil(G sqrt(1/2))/G = 707106781187/1000000000000.
```

The integer square-root construction is correct. Taking `isqrt(G^2//2)`
gives the lower integer candidate, and testing `2 root^2 < G^2` determines
whether an increment is required. Since the near sum is nonnegative,
replacing `sqrt(1/2)` by `c` preserves the upper-bound direction.

The checker independently obtained the least valid integer numerator by
bisection on `2 m^2 >= G^2`, and evaluated the near term by the explicit
double sum. It checked both the normalized and original formulas, multiple
root grids, and the full-history override. If `L>=n-1`, every local history is
complete and the exact value `delta=0` is appropriate.

For all four saved `L=8` cases, the rational constant has decimal display
`0.0005838858411624957`. Its proof is independent of the chosen sensitivities,
cardinality, and positive variance scale.

## Objective bound and pricing

Let `J_L(S)=J0+sum W_(t,H)` denote the information from the local conditionals.
The spectral theorem implies

```text
J(S) <= J0 + [J_L(S)-J0]/(1-delta).
```

Because the supplied objective weight `W` is exactly checked to be positive
semidefinite, applying `tr(W ·)` preserves the inequality. The prior term is
therefore `tr(W J0)` without rescaling. The data terms use the scorer matrix
`H=W/(1-delta)`.

Every resulting arc upper score is valid by the previously reviewed integer
interval component. This review checks its new inputs and integration rather
than repeating its arithmetic test suite. In particular, local variances are
positive under this covariance, their grid lower bounds must remain positive,
and the weight symmetry and dimensions are established before construction.

The count/mask dynamic program covers every cardinality-`k` subset, including
empty and full selections. Its mask records the last `L` calendar decisions;
skipping a candidate still advances that mask. Removing a skip transition
only when too few remaining times could reach cardinality `k` is valid.
Every integer upper score is added with a positive sign. Hence

```text
upper = tr(W J0) + maximum_integer_path_score/score_grid
```

is a global upper bound. The lower bound is the exact weighted trace of the
true selected information. Both bounds, their difference, and the relative
gap are rational, so no logarithm enclosure or numerical solver tolerance is
needed. When the lower bound is zero, the relative gap is reported as absent
rather than dividing by zero. The absolute certificate remains meaningful.

## Independent results

The separate checker passed:

- 189 local conditional coefficient/variance identities using dense rational
  inversion at three different variance scales.
- 378 true selected-information identities against dense selected inverses.
- 200 exact delta/root-grid comparisons, including complete-history cases and
  coarse root grids.
- 321 small complete certificates, with all 1,071 applicable selected subsets
  explicitly checked against each reported upper bound.
- 27 malformed input/option rejections: invalid dimensions, non-PSD or
  asymmetric matrices, bad cardinalities/windows/selections, nonpositive or
  too-small variance, forbidden inexact numbers, and memory-cap refusal.

Small instances cover `n=1,...,6`, one to three parameters, zero/intermediate/
full cardinality, both spectral formulas, zero and truncated memory,
complete and overlong memory, singular priors, and zero objective weights.

The checker then verified all four saved certificates. For each, it rebuilt
the local conditional patterns by dense covariance inversion and ran a
separate dynamic program whose histories are tuples of calendar indices.
The recorded integer prices and priced selections agreed exactly. It also
recomputed the feasible lower information by inverting the 16-by-16 or
32-by-32 selected covariance and matched every rational bound field.

| Saved case | n | k | Integer price | Relative gap, decimal display |
|---|---:|---:|---:|---:|
| 0 | 48 | 16 | 194551540833 | 0.0005992333102508146 |
| 1 | 48 | 16 | 257032945882 | 0.0005973186929751917 |
| 2 | 96 | 32 | 386956489863 | 0.0006036037710669942 |
| 3 | 96 | 32 | 510465579710 | 0.0005992492410591934 |

All cases use `L=8` and score grid `10^8`. Each n=48 replay checked 10,495
arcs and 96,255 states; each n=96 replay checked 22,783 arcs and 452,607 states.
There are 256 local patterns per case. The input file hashes, indexed problem
data, fixed model identifiers, certifier hash, and interval-component hash
were checked against each saved artifact. The approximately six-second
independent review runtime includes the small tests and all four replays; it
is distinct from certificate construction time.

## Scope and reproduction

The exact rationals define the recorded decimal instances. Their ordinary
floating-point display fields are descriptive and are not separately rounded
outward. The fixed latent transition is per calendar step; changing the
candidate grid changes its interpretation in physical time unless that is
accounted for when defining a new instance.

The constructor's state cap and `L<=30` guard are conservative refusal rules,
not exact Python memory or bit-complexity limits. The filter and information
helpers are internal building blocks with narrower preconditions than the
top-level certifier, which checks the needed data and selected indices before
calling them. No unsupported direct helper call is used in these proofs.

Reproduce from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_partial_trace_certificate.py
```

The report identifies the checked source, component, verifier, and certificate
versions by SHA-256. This review does not assess novelty, benchmark fairness,
or performance relative to stronger competing approaches.
