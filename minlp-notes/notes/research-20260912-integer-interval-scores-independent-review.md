# Independent review of integer interval arc scores

Date: 2026-09-12. Status: accepted after one input-validation correction.
The final component has no remaining defect found in this bounded review.
Its contract is an upper bound on each local quadratic information score; a
complete design certificate still needs a valid tangent, spectral correction,
feasible incumbent, complete pricing, and directed logarithm bounds.

Reviewed artifacts:

- [Component](../code/research_20260912/integer_interval_scores.py).
- [Author tests and benchmark](../code/research_20260912/verify_integer_interval_scores.py).
- [Author proof and performance note](research-20260912-integer-interval-scores.md).
- [Independent verifier](../code/research_20260912/review_integer_interval_scores.py).
- [Independent report](../code/research_20260912/results/integer-interval-scores-independent-review.json).

The reviewed component SHA-256 is
`b558f1b03db3f195be8fd0fbab8741396dd75264ccbef2f3a65d98908a763c1d`.
The independent reviewer did not edit the component or author test file.

## Contract and proof

For rational features `F`, a symmetric rational matrix `H`, rational local
regression coefficients `b`, and rational variance `d>0`, define

```text
g = F_t - sum_j b_j F_(t-age_j),
q = g^T H g / d.
```

The component returns an integer `U` such that `U/score_grid >= q`. Positive
semidefiniteness of `H` is unnecessary for this contract. All divisions used
to initialize intervals are exact rational divisions followed by mathematical
floor or ceiling. Subsequent arc calculations use Python integers, so there
is no fixed-width overflow or floating-point rounding in those calculations.

Write `Gf` for the feature grid and `Gc` for the coefficient grid. The feature
intervals contain `Gf F_ij`. Coefficient and weight intervals contain `Gc b_j`
and `Gc H_ij`. Therefore the interval formed by subtracting the interval
products from `Gc` times the feature interval contains

```text
Gf Gc g_i.
```

The product of two intervals is enclosed by the smallest and largest of the
four endpoint products, including negative and zero-crossing intervals. The
square of an interval has lower endpoint zero when the interval includes
zero; otherwise its lower endpoint is the smaller endpoint square. Its upper
endpoint is the larger endpoint square. These facts justify every interval
operation in the adjusted features and quadratic calculation.

Using symmetry, the exact quadratic decomposes into diagonal terms plus
twice the lower-triangular cross terms. Summing each interval upper endpoint
therefore gives an integer `Qup` satisfying

```text
Qup >= Gf^2 Gc^3 g^T H g.
```

The repeated appearance of a feature in several terms can make this sum
loose, but cannot invalidate it. In particular, signed off-diagonal weights
and negative diagonal weights are correctly handled by the same interval
product operation.

Let `D=floor(Gc d)>0`. If `g^T H g` is nonnegative, replacing its numerator by
the larger nonnegative integer bound and its variance by the smaller positive
number `D/Gc` preserves an upper bound. If the quadratic is negative, zero is
already an upper bound. Consequently

```text
q <= max(0,Qup) / (Gf^2 Gc^2 D).
```

This is exactly the denominator and nonnegative clamp used in the component.
Finally, multiplying by the positive integer score grid and taking an upward
integer ceiling proves the contract. The clamp is essential when `H` is
indefinite: dividing a negative upper numerator by a lower positive variance
would not, by itself, preserve an upper bound.

A positive variance with `floor(Gc d)=0` is rejected. This is an explicit
precision limit; increasing the coefficient grid can resolve it. No implicit
fallback changes the calculation. An arbitrary ordering of distinct positive
ages is valid for `prepare`, provided the coefficients have the matching
order. The stationary convenience method requires decreasing ages because it
constructs chronologically ordered conditioning data.

## Malformed-pattern correction

The original public `IntegerPattern` dataclass could be constructed with
invalid internal fields. `upper` checked its type and grid compatibility, but
did not check positive variance, matching coefficient lengths, or ordered
interval endpoints. For example, with unit grids, `F=(1,2)`, `H=1`, target
one, age one, and coefficient one, replacing a prepared pattern's
`variance_lower` and `score_denominator` by `-1` caused the original method to
return `-1`. The valid positive-variance score for that example is `1`.

The author added one-time dataclass construction checks during this review.
The final version requires:

- Immutable tuples of distinct positive integer ages and matching coefficients.
- Immutable coefficient intervals with exactly two ordered integer endpoints.
- Positive integer variance lower bound, coefficient grid, and denominator.
- Rejection of Boolean values where integers are required.

The existing per-arc checks continue to enforce compatible scorer grids and
valid target/history indices. This prevents the reported malformed cases
without repeating all structural checks on every arc. Ordinary use through
`prepare` was mathematically sound before this correction; the change closes
the public constructor boundary.

## Independent verification

The separate verifier passed:

- 2,025 interval-product checks against all integer points in the tested
  intervals, and 45 square-interval checks including zero-crossing intervals.
- 1,950 exact arc comparisons using independent dense symbolic matrix
  multiplication, including 981 negative exact quadratic scores. These use
  varied feature, coefficient, and score grids, arbitrary signed regression
  coefficients, and symmetric matrices that can be indefinite.
- Explicit cancellation cases where outward feature rounding makes the
  adjusted-feature interval straddle zero.
- 60 stationary-history checks using dense rational covariance inversion,
  including negative and zero correlation, zero latent variance, empty
  histories, and incomplete histories.
- 27 malformed-input rejections covering the constructor correction, invalid
  targets, incompatible prepared grids, bad dimensions, asymmetric weights,
  forbidden inexact numbers, and variance grid refusal.

For the saved `n=96`, `k=32`, `L=13`, minimum-gap-two instance, the reviewer
recomputed all 377 local conditional patterns using dense covariance
inversion rather than the author's scalar Kalman routine. A separate
reachability and pricing implementation represented history by tuples of
calendar indices rather than bit masks. It visited 753,275 states and checked
all 31,900 reachable arc scores against their exact rational ceilings.

Every interval score was at least the corresponding exact rational ceiling.
Exactly 418 arc scores increased, each by one unit on the `10^8` score grid.
The independently priced maxima were

```text
original rational arc ceilings: 299934500,
integer interval upper scores:  299934501.
```

Thus substituting the interval scores into this same design certificate
increases its global objective upper bound by exactly `1/100000000`. The
looser generic path-increase estimate is `k` times the largest individual
arc increase, or `32/100000000` here. Neither statement relies on the two
maximizing paths being the same.

The saved instance used for this replay has certificate SHA-256
`a9e2801335365776edd538e7c74c3d7017c5a9889d53b9a32985feca0d654388`.
The independent report records the full source, verifier, and input hashes.
Its approximately 28-second runtime includes the separate exact rational
checks and is not a measurement of the fast component alone.

## Scope of the performance evidence

The author's saved benchmark reports about 0.29 seconds for interval arc
evaluation versus 33 seconds for exact rational arc evaluation on this
instance. That benchmark predates the one-time constructor hardening, while
the independent full-arc replay above uses the final hardened source. The arc
arithmetic itself is unchanged. This is useful component-level evidence;
end-to-end speed after integration should be measured separately, including
conditional preparation, pricing, and the other certificate calculations.

The method is ordinary outward interval arithmetic applied to the expensive
rational arc calculation. This review makes no novelty claim for that
arithmetic. The useful result is a checked implementation that can replace
these exact rational arc evaluations while preserving the direction of every
certificate bound, with a measured negligible bound increase on the saved
instance.

Reproduce from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_integer_interval_scores.py
```
