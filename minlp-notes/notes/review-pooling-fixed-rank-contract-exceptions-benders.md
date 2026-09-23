# Independent second audit: fixed affine quality rank

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS.** I checked the complete vector extension in
[the candidate](pooling-fixed-rank-contract-exceptions-algorithm.md),
including chart coverage, all local vector equations, denominator
clearing, singular and lower-dimensional cases, and exact optimization.
This review builds on the independently checked
[scalar exception proof](review-pooling-bounded-contract-exceptions-benders.md).

## Affine reduction and actual quality balance

A rational affine basis of the source-quality vectors has polynomial
encoding length. A positive-demand exact product outside their affine
hull is infeasible because every physical positive blend belongs to
that hull. Zero demand forces all incoming nonnegative flows to zero;
its exact homogeneous quality equation is then independent of the
specified product vector, so replacement by any hull vector is safe.
Incompatible positive arc lower bounds are still rejected by the flow
rows. At affine rank zero the whole model is an ordinary LP with known
active-blend qualities.

Writing an original quality coordinate as an affine function of basis
coordinates converts its mass to that affine function's constant times
throughput plus its linear part applied to basis-quality mass. Hence
all original exceptional-output quality inequalities remain valid,
including arbitrary many original quality coordinates. They add rows,
not core variables.

The vector global equations recover the physical pool balances
coordinate by coordinate exactly as in the scalar proof. Their degree
is at most two. Nonnegative flows handle zero throughput without
division. At positive throughput the reconstructed quality lies in
the convex hull of actual feeds, hence in the chosen coordinate box.
Although the box may contain points outside that hull, the balance
equations exclude them whenever the pool is active. Inactive pools may
use a source vector in the box. The core dimension is at most `t+5s`.

## Chart coverage and local vector equations

For any quality vector unequal to all source vectors, each polynomial
`sum_h k^(h-1)(C_ih-q_h)` is nonzero and has at most `t-1` real roots.
The union over sources excludes at most `|I|(t-1)` candidate integers.
Thus the stated family of `|I|(t-1)+1` directions contains a chart on
which every scaling factor is nonzero. This includes `t=1`, when a
single direction suffices. Each omitted full source vector is rational
and is handled by an original fixed-vector-quality LP. Repeated source
vectors and overlapping charts do not affect coverage.

The chart directions have polynomial bit length for fixed rank. Every
scaling factor and every further coefficient used for its sign
partition is affine in the rank-dimensional quality vector. A
polynomial-size affine arrangement has polynomially many realizable
sign cells in fixed dimension. Zero signs for the extra coefficients
and lower-dimensional intersections with the quality box must be
retained; the draft does so. Only zero scaling factors are excluded
from an individual chart.

The projected scalar equation gives the constant incidence matrix.
The outlet-total interval has the scalar two-inlet encoding when the
projected source qualities differ. Equal projected qualities require
the parameter-only total-flow test instead; they need not mean equal
full source vectors.

The additional basis-coordinate equations are therefore essential. I
independently expanded their coefficients. Put `c_i=beta*C_i` and
`bproj=beta*B`. Then

```
a_h=C_1h*c_2-C_2h*c_1
    +(C_2h-C_1h)*(beta*q)+q_h*(c_1-c_2),

f_h=b*gamma_1*[B_h*c_2-C_2h*bproj
               +(C_2h-B_h)*(beta*q)+q_h*(bproj-c_2)].
```

Thus `a_h` is affine and `f_h` is quadratic. Multiplying the original
coordinate equation by the nonzero `gamma_1*gamma_2` is reversible.
Where `a_h=0`, the exact remaining requirement is `f_h=0`. Where it is
nonzero, putting `f_h/a_h` in both the lower and upper candidate lists
imposes equality on the selected arc. All coordinate equations can
use that same arc because the projected node equation determines the
other arc. Conflicting coordinate equalities are detected by candidate
consistency rows. This works also when projected source qualities
coincide.

For a single inlet the additional equation after multiplication by
its nonzero scaling factor is exact. With no bypass inlet every vector
quality equation remains a pure parameter condition. No original
quality information is replaced by its scalar projection alone.

## Polynomial cuts, degree, and bit length

Boundary removal shifts prescribed transformed flow out of both node
bounds and preserves all derived boundary capacity or equality rows.
The same accounting applies when one selected two-inlet arc is a
retained boundary arc. Residual paths, cycles, and isolated nodes have
the previously checked connected-cut description.

Candidate lists may now be polynomial rather than constant in size,
but a connected cut uses at most two arc lists. Enumerating every
selected pair, and every lower/upper consistency pair on one arc, is
still polynomial. For each resulting row, multiply by only its one or
two selected denominators. Their nonzero signs are fixed by the chart
cell, so the inequality direction can be preserved exactly, for
example by multiplying by the sign-adjusted positive product.

Each denominator is affine, each numerator has degree at most two,
and a node sum is affine in quality and boundary coordinates. This
gives total degree at most three for these cut and consistency rows;
the draft's conservative degree-four bound is valid. Boundary rows and
the physical/global equations also have fixed degree. Identically zero
denominators are never cleared: they belong to the separately treated
`a_h=0` case. No product over an unbounded collection of arc
denominators is introduced.

All coefficients have polynomial rational encoding length. Direction
coefficients, fixed projected-quality differences, constant-degree
products, and polynomial-length node sums preserve this bound. The
number of charts, cells, cuts, and candidate combinations is polynomial
for fixed rank and exception count.

## Exact optimization and lifting

The scalar attained-value argument applies with fixed core dimension
`t+5s`; adding one value coordinate remains fixed-dimensional.
Sign cells keep their strict and equality conditions. The union over
all valid charts and all full-source-vector LPs covers exactly the
original attainable-value set, including singular and lower-dimensional
feasible sets. The compact original model has an attained maximum.
Sampling from an actual cell attaining that value avoids any unsound
closure at vanishing denominators.

The value and core sample can be represented together in one real
algebraic field of polynomial degree and encoding length. Evaluate
each selected rational capacity in that field, recover a feasible
incidence flow there, and divide by the nonzero chart scalings. The
constant incidence matrix introduces no new algebraic extension.
Local contracts recover all remaining pool arcs, and the global vector
identities ensure every recovered flow has the correct physical pool
quality. Singular source-vector cases are original rational LPs.

The new checker described in the candidate supplies distinct evidence
for the vector equations: removing them creates false positives. Its
reported exact rational cut comparisons against numerical original LPs
support local equivalence, not full symbolic optimization. I did not
duplicate those tests. This review independently establishes the
additional algebraic, chart-coverage, and complexity obligations.

The result retains the fixed exception count, fixed affine rank,
bypass-degree-two, exact ordinary contracts, and redundant common pool
bound assumptions. It allows arbitrary original quality count, but
does not prove a general fixed-rank pooling algorithm or a quadratic-
field witness bound. Separate literature priority remains provisional.

### Redundancy certificate addendum

The common pool upper bound is redundant whenever it is at least the
minimum of total source upper throughput, the sum of pool-feed arc upper
capacities, and the sum of pool-outlet arc upper capacities. Nonnegative
flows and pool conservation prove each of these bounds separately.
This check uses no quality assumption and applies to the fixed-rank
extension unchanged. It does not introduce a new dense aggregate row.

The scalar audit's sharpened common-capacity redundancy certificate
also applies unchanged: use the minimum of total input-throughput
upper bounds, total allowed feed capacities, and total allowed outlet
capacities. Each separately bounds physical pool throughput.
