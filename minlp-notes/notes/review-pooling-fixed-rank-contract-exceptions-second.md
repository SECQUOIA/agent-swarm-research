# Independent audit: fixed affine rank and bounded contract exceptions

Date: 2026-09-05. Reviewer: `pooling_all_two_review`.
Verdict: PASS for the stated fixed-rank, fixed-exception theorem.
This restores my separate audit after an accidental filename collision;
[benders' independent audit](review-pooling-fixed-rank-contract-exceptions-benders.md)
is preserved separately.

Candidate: [fixed affine rank extension](pooling-fixed-rank-contract-exceptions-algorithm.md).

## Coordinate reduction and physical balances

A rational affine basis of the source vectors is computable with polynomial
bit complexity. Positive-demand exact product vectors must belong to this
affine hull. Zero-demand products have all flows zero, so their nominal
quality can be ignored or replaced by a vector in the hull. Rank zero
reduces to an LP. Original exceptional-output quality inequalities retain
the affine offset times throughput and the linear basis-quality mass;
the offset must not be discarded for variable throughput.

In basis dimension `t`, exceptional arcs and scalar transformed bypass
coordinates give the stated core bound `t+5s`. The total mass equation
and all `t` global quality equations restore actual pool conservation
coordinate by coordinate. This is the scalar argument with no omitted
vector balance. At positive throughput the core quality vector is a
convex combination of allowed feed vectors. A coordinate box containing
that hull suffices; imposing the hull separately is unnecessary. At zero
throughput the quality is immaterial.

## Coverage by projection directions

If `q` equals a source vector, the entire original fixed-vector model
is a rational LP. Otherwise every polynomial
`(1,k,...,k^(t-1)) dot (C_i-q)` is nonzero and has at most `t-1` roots.
The union of forbidden integers over the sources has size at most
`|I|(t-1)`. The proposed family of one more direction therefore covers
every remaining quality vector. Its count and bit encoding are polynomial
for fixed `t`. Charts may overlap without affecting exact feasibility.

Within a chart, every scaling `gamma_i` is nonzero. Its sign and the
signs of additional affine functions can be partitioned by an arrangement
in fixed dimension. Lower-dimensional zero strata must be included;
the candidate does include them.

## Additional coordinate equations and degree bounds

At a two-inlet ordinary product, projected quality gives `w_1+w_2=R`.
For every basis coordinate, substituting `w_2=R-w_1` into its original
quality equation and multiplying by `gamma_1 gamma_2` gives

```
a_h w_1=f_h,
a_h=(C_1h-q_h)gamma_2-(C_2h-q_h)gamma_1,
f_h=gamma_1[b(B_h-q_h)gamma_2-(C_2h-q_h)R].
```

The quadratic terms cancel in `a_h`, leaving an affine polynomial. The
bracket in `f_h` is also affine because `R=b beta dot (B-q)`, leaving
degree at most two after multiplication by `gamma_1`. At a zero of
`a_h`, keep the exact parameter equation `f_h=0`; elsewhere it is an
exact arc bound with quadratic numerator and affine denominator. This
also handles distinct source vectors with equal scalar projections.
Discarding those remaining coordinate equations would be incorrect.

The one-inlet case becomes a pure quadratic parameter equality; the
zero-inlet case retains the full vector equation. Flow bounds from the
projected two-inlet equation remain quadratic candidates when projected
source values differ and pure parameter conditions when they agree.

After deleting exceptions, a connected path or cycle cut crosses at
most two internal edges. Even polynomial-size candidate lists therefore
give polynomially many combinations. Each cut clears at most two
selected affine denominators, whose signs are fixed on its chart stratum.
This gives constant-degree polynomial rows, including linear boundary
terms. No product over all network denominators is required.

## Complexity, attainment, and witness field

There are polynomially many charts and affine sign strata for fixed
rank. Each uses fixed core dimension and bounded-degree polynomial rows.
The scalar attained-value argument carries over with all open and
lower-dimensional cells plus source-vector LPs. It does not take closures
of transformed cells. Compactness of the original physical model supplies
attainment of the global optimum.

Sample core coordinates in one polynomial-degree real algebraic field.
Evaluated rational capacities belong to that field. Incidence-flow
recovery adds no algebraic extension; original flows are obtained by
division by the nonzero scalings. Polynomial bounds on the common field
and coefficient lengths are preserved. No quadratic-degree witness
claim follows or is made.

## Independent algebra checks and scope

[My exact checker](../code/pooling_bypass_paths/check_fixed_rank_chart_algebra.py)
passed 45 symbolic residual identities and numerator/denominator degree
checks, covering repeated source vectors and equal projections. It also
passed 32 moment-curve coverage tests constructed to forbid all earlier
directions. These tests independently support the new local algebra and
coverage lemma; they are not an implementation of full algebraic global
optimization. The author's original-flow tests provide separate evidence
and include false positives when additional quality equations are removed.

The common-capacity certificate can use the minimum of total source upper
throughput, total feed capacities, and total outlet capacities, independently
of quality rank. This is a redundancy check, not a new dense aggregate row.
Fixed exception count, fixed affine rank, exact ordinary contracts, and
bypass degree two remain hypotheses of this audited theorem. Source
priority is separately qualified.
