# Polynomially varying local constraint normals in fixed follower blocks

Date: 2026-09-05. Status: reviewed and integrated into
[the response-semantics result](../results/bilevel-compressed-response-infimum-semantics.md).
This extends the exact infimum and attainment-decision conclusions of
[the response-semantics theorem](../results/bilevel-compressed-response-infimum-semantics.md).
It does not restore unconditional attainment.

Use the fixed-dimensional positive-definite quadratic block model from
[the block theorem](../results/bilevel-fixed-block-response-algorithm.md),
but now allow every local constraint matrix to depend polynomially on the
leader:

```
P_b(x)={y: E_b(x)y=e_b(x), G_b(x)y<=h_b(x)}.
```

Keep a compact leader domain, polynomial coordinate bounds ensuring uniform
boundedness, fixed block dimension `d`, fixed leader/resource/aggregate
dimensions, positive-definite local `Q_b(x)`, and the same explicit
polynomial degree/bit representation. Shared resource matrices may also
vary polynomially. Row counts in all local matrices remain unrestricted.

**Candidate corollary.** Optimistic and pessimistic feasibility, finite
infimum computation, and attainment decision are polynomial in rational
input bit length. An optimizer can be returned when one exists, together
with a worst-case follower response under the pessimistic convention.
Output uses one polynomial-size common algebraic field. The pessimistic
upper constraints apply to every global follower optimum, as explicitly
defined in the response-semantics theorem.

## Replacement for the constant equality-basis step

At fixed compressed coordinates `v=(x,w,lambda,mu)`, the local quadratic
response is still unique when feasible. Its stationarity problem has
polynomial positive-definite matrix `Q_b(x)` and polynomial effective
linear coefficient `q_b(v)` exactly as in the earlier block proof.

Instead of choosing a single constant row basis of `E_b`, enumerate every
pair `(I,J)` where `I` is a subset of equality rows, `J` a subset of
inequality rows, and `|I|+|J|<=d_b`. There are polynomially many pairs for
fixed `d`, even when their row counts grow. Include the empty pair.
Put

```
V_(I,J)(x)=[(E_b(x))_I; (G_b(x))_J],
M_(I,J)(x)=[Q_b(x)  V_(I,J)(x)^T;
             V_(I,J)(x)     0].
```

Use a branch only where `Delta_(I,J)(x)=det M_(I,J)(x)` is nonzero.
For positive-definite `Q_b(x)`, this is equivalent to row independence of
`V_(I,J)(x)`, by the same nullspace argument as in the original block
proof. Cramer's rule solves its KKT equations rationally. As before, use
`Delta^2` as a positive denominator, multiplying all Cramer numerators by
`Delta`. This denominator is now positive only on the branch's declared
validity region, which is sufficient for every clearing operation.

A branch is valid when `Delta^2>0`, the candidate satisfies **all** original
local equality and inequality rows, and the multipliers belonging to `J`
are nonnegative. No condition that `I` span all equality rows is needed for
soundness: multipliers on omitted equality and inequality rows can be set
to zero, yielding sufficient KKT conditions for the local strictly convex
quadratic program. Hence every valid branch returns its unique minimizer.

For completeness, at any fixed `x` with a feasible local polytope choose
`I` to be a basis of the full equality row space at that leader. The
polyhedral normal-cone representation of the negative local minimizer gradient,
followed by conic support reduction modulo that equality row space,
provides active inequality rows `J` independent together with `I` and
`|I|+|J|<=d_b`. This pair is enumerated and has nonzero KKT determinant.
Its branch is valid and returns the minimizer. Rank changes of `E_b(x)`
cause no missing cases because all possible bases, including the empty
one, were enumerated.

## Global regimes and bit complexity

Collect every determinant and cleared branch-feasibility polynomial from
all blocks. The KKT matrices have size at most `2d`; their entries have
polynomial degree in the fixed-dimensional leader/compressed variables.
Determinants and numerators therefore have polynomial degree and expanded
bit length. There are polynomially many branches and tests for fixed `d`.

Realizable sign conditions of this family in the fixed-dimensional
compressed space can be enumerated in polynomial bit time. Within each
condition, determinant nonvanishing and all branch-validity tests are
fixed. Discard a condition if any block has no valid branch; otherwise
choose its first valid branch. Uniqueness of the local quadratic response
makes overlapping branches agree, so this selection is lossless.

The selected squared determinants have positive product on that regime.
Clearing this common denominator gives a polynomial-size fixed-dimensional
formula for all follower KKT points. Pointwise polyhedral KKT necessity
still covers every global follower minimizer. Comparing all compressed
KKT values therefore gives the exact globally optimal reaction graph.

All quantifier formulas for optimistic and pessimistic values, infima,
and attainment now apply unchanged. Uniform box boundedness on compact
`C` bounds all upper values. At each fixed feasible leader the follower
argmin set is compact, so a pessimistic worst response exists there. The
reaction graph need not be closed as the leader varies; hence the result
retains an attainment test and does not promise an optimizer when the
infimum is unattained.

The previous local-fixed-normal theorem's proof of unconditional
optimistic attainment remains valid only in that narrower setting. The
one-dimensional example `xz=0` from the response-semantics theorem already
shows why this distinction cannot be removed.

## Contribution scope

The extra mathematical step is enumeration of all possible equality bases
and independent active inequality subsets while testing determinant
nonvanishing on each leader regime. This is an elementary extension of
the previously credited parametric active-set construction, not a separate
claim of a new local-QP algorithm. Its use here removes an artificial
constant-normal restriction from the exact global bilevel infimum theorem
while retaining an explicit failure-of-attainment distinction.

A small exact check in
[check_response_boundaries.py](../code/bilevel_response/check_response_boundaries.py)
exercises a changing equality rank: the local problem minimizes
`z^2/2-z` over `[0,1]` with `xz=0`. The equality-active KKT determinant is
`-x^2`; its squared denominator vanishes at `x=0`, where that branch must
be discarded and the empty equality subset instead yields `z=1`. The same
script checks that the quartic pessimistic example has a nonglobal KKT
point at `z=1/2`, which the global value comparison must exclude. These
exact examples support the boundary handling; they do not replace the
independent proof audit.
