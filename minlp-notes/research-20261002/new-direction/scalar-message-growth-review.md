# Independent review of the scalar-message growth obstruction

Date: 2026-10-02. Reviewed
[scalar-message-growth-obstruction.md](scalar-message-growth-obstruction.md).
No substantive gap was found. No external search or additional agents were
used for this review.

The construction disproves polynomial closure for **complete, explicitly
listed interval-quadratic Bellman messages** under bounded width and global
quadratic growth. It does not disprove compact expression DAGs, selective
Bellman lower bounds, or factorized certificates.

## 1. Zero set and terminal projection

The objective is

```
F(s,z)=sum_(t=1)^m (s_t-s_(t-1)/2-z_t/2)^2
       +(1/8)sum_(t=1)^m z_t(1-z_t),
s_0=0,       s_t,z_t in [0,1].
```

All terms are nonnegative. Zero objective therefore requires and is
equivalent to binary `z_t=b_t` and the exact recurrence
`s_t=(s_(t-1)+b_t)/2`. These states are feasible. In particular,

```
s_m=sum_(i=1)^m b_i 2^(i-m-1).
```

The terminal values are exactly `j/2^m` for `j=0,...,2^m-1`, each attained
by a different binary string. The endpoint one is not a terminal zero.

## 2. Growth, curvature, and graph constants

Round each `z_t` to a nearest binary value `b_t`; ties can be resolved either
way. Set `e=z-b`, let `s*` follow the binary recurrence, and write
`r_t=s_t-s_(t-1)/2-z_t/2`. If `T` is the backward shift with zero initial
entry, then

```
(I-T/2)(s-s*)=r+e/2.
```

Its inverse is the finite sum of shifts with coefficients
`1,1/2,...,2^(-(m-1))`. Since each shift has Euclidean operator norm at
most one, the inverse has norm at most two. Consequently,

```
||s-s*|| <= 2||r||+||e||,
dist((s,z),S)^2 <= ||s-s*||^2+||e||^2
                 <= 8||r||^2+3||e||^2.
```

Nearest-binary rounding gives `e_t^2<=z_t(1-z_t)`. It follows that
`dist((s,z),S)^2<=24F(s,z)`, so `g=1/24` is a valid global constant.
No claim that this constant is sharp is needed.

The Hessian diagonal entries are:

- `5/2` for `s_t` with `t<m`;
- `2` for `s_m`;
- `1/4` for every `z_t`, including the negative contribution from its
  box-product term.

Thus all coordinate diagonals are positive, `L=5/2` is valid for every
`m`, and `kappa<=60`. For `m=1`, this `L` is merely conservative.

The bags `{s_(t-1),s_t,z_t}`, omitting the fixed `s_0`, form a path
decomposition: every interaction is covered and each state appears in
consecutive bags. For `m>=2` a triangle occurs, so treewidth is exactly two.
All coefficients have constant encoding length.

## 3. What the piece count proves

For each terminal value `v`, the conditional feasible set is nonempty and
compact, so the minimum defining `M(v)` is attained. The full growth bound
gives

```
M(v)>=(1/24)dist(v,{j/2^m:j=0,...,2^m-1})^2.
```

Together with the attainable zero states, this proves that `M` has exactly
`2^m` isolated zeros and no interval of zeros.

Suppose `K` intervals cover the terminal domain and on each interval `M`
agrees with a polynomial of degree at most two. A positive-length interval
cannot use the identically zero polynomial. Every remaining polynomial has
at most two distinct roots. A singleton interval covers at most one root,
including when its polynomial is identically zero. Counting the zeros thus
gives `2^m<=2K`, or `K>=2^(m-1)`. Overlaps, open versus closed endpoints,
and singleton pieces do not invalidate this bound, provided every domain
point is represented.

The same reasoning applies to an exact finite lower envelope of
interval-restricted quadratic pieces. At every zero, some eligible piece
attains zero. An identically zero piece with a positive-length validity
interval would force the nonnegative minimum to vanish on that interval,
which is impossible. Every other piece can account for at most two zeros.

Subtracting one fixed quadratic terminal potential also preserves the
bound: adding it back keeps every represented piece quadratic and restores
the zero-count argument.

The result does **not** bound the size of a recursive expression that
implicitly encodes exponentially many pieces. Nor does it force an
optimization algorithm to construct the full message. The original sum of
squares and box products is already a short exact lower-bound certificate,
and a binary recurrence supplies a matching feasible point.

## Verification record

This review checked the displayed identities, constants, graph structure,
and representation quantifiers directly. The main note records its targeted
exact-rational checks: 500 growth tests and all 510 binary zero states for
chain lengths one through eight. Those computations were not duplicated.
No project-wide verification or CI inspection was performed.
