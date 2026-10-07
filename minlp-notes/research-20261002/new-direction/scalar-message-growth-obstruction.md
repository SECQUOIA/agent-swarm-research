# Exponentially many scalar Bellman pieces at fixed growth and width

Date: 2026-10-02. This rules out enumerating complete scalar-separator
quadratic messages as the proposed next route. It is a representation
lower bound, not optimization hardness or a lower bound for factorized
certificates. The example itself has an immediate global certificate.

For `s_0=0` and `s_t,z_t in [0,1]`, define

```
F(s,z) = sum_(t=1)^m (s_t-s_(t-1)/2-z_t/2)^2
         +(1/8) sum_(t=1)^m z_t(1-z_t).
```

Every term is nonnegative. Its zero set `S` consists exactly of the
`2^m` points obtained by choosing binary `z` and following the stable
recurrence

```
s_t = s_(t-1)/2+z_t/2.
```

All resulting states lie in `[0,1]`. The terminal projection is

```
pi_(s_m)(S) = {j/2^m : j=0,...,2^m-1}.
```

## Uniform growth and curvature

For any feasible point, round each `z_t` to a nearest binary value `b_t`.
Let `s*` be the exact recurrence driven by `b`, put `e=z-b`, and let
`r_t=s_t-s_(t-1)/2-z_t/2`. The displacement `d=s-s*` obeys

```
d_t=d_(t-1)/2+r_t+e_t/2,          d_0=0.
```

The causal convolution with coefficients `1,1/2,1/4,...` has Euclidean
operator norm at most their sum, two. Therefore

```
||d|| <= 2||r||+||e||,
dist((s,z),S)^2 <= ||d||^2+||e||^2
                 <= 8||r||^2+3||e||^2.
```

Nearest-binary rounding gives `e_t^2<=z_t(1-z_t)`. Consequently

```
dist((s,z),S)^2 <= 24 F(s,z).
```

Thus `g=1/24` is valid independently of `m`. All Hessian diagonals are
positive: the `z_t` diagonal is `1/4`, an interior state diagonal is
`5/2`, and the terminal state diagonal is two. The valid common upper
coordinate curvature is `L=5/2`, giving `kappa<=60`.

The bags `{s_(t-1),s_t,z_t}`, with the fixed coordinate `s_0` omitted,
form a path decomposition. For `m>=2` the graph contains a triangle and
has treewidth exactly two. Consecutive triangles share only their state
articulation variable. Numerical coefficients and their encoding lengths
are bounded constants.

## The complete terminal message needs exponentially many pieces

Consider the exact terminal message

```
M(v)=min{F(s,z): s_m=v, all other coordinates in [0,1]},
       v in [0,1].
```

Every conditional domain is nonempty and compact. The preceding zero-set
description gives exactly `2^m` distinct zeros of `M`. Moreover,

```
M(v) >= (1/24) dist(v,pi_(s_m)(S))^2,
```

because coordinate distance cannot exceed full-vector distance. Hence
`M` is strictly positive away from those isolated zeros and vanishes on
no nontrivial interval.

Suppose a representation covers `[0,1]` by `K` intervals on each of
which `M` agrees with a quadratic polynomial. Each nondegenerate piece
uses a nonzero polynomial, since a zero polynomial would give a zero
interval. Such a piece contains at most two distinct zeros. A degenerate
singleton piece covers at most one. It follows that

```
K >= 2^(m-1).
```

The same counting argument applies to interval-restricted quadratic
pieces represented by their lower envelope: each active piece touching
a zero must itself vanish there, while an identically zero piece cannot
have a nontrivial validity interval. Subtracting a fixed terminal unary
quadratic from every message also changes nothing: add it back before
counting zeros. The obstruction therefore does not depend on a common
choice of where the terminal quadratic is allocated.

## Consequence for the research direction

Full scalar-message enumeration can be exponential even on a chain of
triangles with fixed `p=3`, `kappa<=60`, positive diagonal curvature,
and constant-size coefficients. The proposed polynomial full-message
closure target is therefore false under those assumptions.

The sum of residual squares and box-bound products already certifies
`F>=0`, and any binary recurrence provides an attaining point. This is
an easy optimization instance. Selective Bellman inequalities, shared
factorized descriptions, or other certificates may avoid constructing
the complete message. No lower bound for those mechanisms is proved.

The [independent review](scalar-message-growth-review.md) checks the
recurrence, growth constant, decomposition, and piece-count argument.
This closes the suggested full-message test; it does not resolve the
general unknown-growth arbitrary-optimal-set problem.

## Targeted verification

An inline `python3 -` check with exact rational arithmetic verified the
candidate-distance growth bound on 500 points for chains of lengths
one through five, all 510 binary zero points for lengths one through
eight, and their distinct terminal projections. The proof above covers
all lengths and points. No project-wide verification or CI check was
performed.
