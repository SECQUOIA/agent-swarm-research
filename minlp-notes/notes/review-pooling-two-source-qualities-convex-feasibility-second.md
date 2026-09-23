# Independent audit: two source qualities and arbitrary bypass topology

Date: 2026-09-05. Reviewer: `pooling_all_two_review`.
Verdict: PASS for the stated feasibility theorem and polynomial-encoding
rational original witness. No mathematical defect found.

Candidate: [two source qualities](pooling-two-source-qualities-convex-feasibility.md).

## Physical equivalence

Normalize the two source values in increasing order to zero and one.
The exact global mass and normalized quality totals are necessary. A
positive-demand product outside the normalized interval is infeasible;
a zero-demand product contributes no flow or quality mass. One source
value and an unusable pool reduce to the stated original LP cases.

For `0<q<1`, the scaling factors are `-q` for class zero and `1-q` for
class one. Both have fixed nonzero sign. Therefore every bypass interval
and every input's bypass-total interval transforms to an affine interval,
with order reversed for class zero. This does not rely on bounded source
degree. Missing feed arcs mean a zero intake residual and must retain
that equality; positive feed lower bounds remain legitimate.

At output `j`, writing `W_1=R-W_0` gives

```
s=-W_0/q+(R-W_0)/(1-q)
 =R/(1-q)-W_0/[q(1-q)].
```

Since `R=b(B-q)` and `v=b-s`, this is exactly
`W_0=q b(B-1)+q(1-q)v`. Thus a zero-lower-bound outlet interval
`0<=v<=U` is equivalent to the proposed affine lower bound and concave
quadratic upper bound on `W_0`. The same identity holds with any number
of inlets from either class, including no inlets from a class or no
bypass at all. An absent outlet is correctly represented by `U=0`.

Recovering all local feeds and outlets gives nonnegative flows satisfying
their original bounds. Summing local exact output quality equations and
subtracting the exact global quality total restores the actual pool
quality balance. The exact global mass total similarly restores pool
mass conservation. These identities apply to every transformed feasible
assignment, so arbitrary bypass cycles or branching introduce no hidden
aggregate condition. At zero throughput all nonnegative pool arcs vanish.

## Convex formulation and the shared auxiliary coordinate

For each output, its upper bound is

```
W_0 <= q b(B-1)+U(q-q^2).
```

Replacing `q^2` by a common `r` in the affine rows and requiring `r>=q^2`
is exact for feasibility. Setting `r=q^2` extends every original point.
Conversely increasing `r` decreases every right-hand side because all
`U>=0`, so every lifted feasible point satisfies every original upper
bound. No output requires its own quadratic variable. When `U=0`, the
row is independent of `r` and the argument remains valid.

The rational polytope `P` is bounded: `q,r` lie in `[0,1]` and transformed
bypass bounds give finite bounds on every `w`. Minimizing `F=q^2-r`
over `P` is a convex quadratic program with rank-one positive semidefinite
Hessian. This is a polynomial algorithm in the full number of arc
variables; fixed-dimensional elimination is not being used here.

## Exact strict-interior handling

The original physical LPs at `q=0,1` are necessary because the scaling
is singular there. The affine transformed limits cannot substitute for
these LPs. The candidate correctly uses them separately.

The margin LP detects whether `P` itself contains any quality in `(0,1)`
and supplies a polynomial-bit rational point `p` there. If the minimum
of `F` is positive, the lifted model is infeasible. If it is zero,
all minimizers have the same `q`: for two different quality coordinates,
the midpoint's objective is the average objective minus one quarter
of their squared difference. Such a midpoint would have negative
objective, contradicting a zero minimum. Hence inspecting the rational
optimizer's quality decides interior feasibility in this case.

If the minimum is `-rho<0`, the convex combination with coefficient
`lambda=rho/[2(rho+1)]` has interior quality because `0<lambda<1` and
`p` is interior. Since `F(p)<=1`, convexity gives the stated upper bound
`-rho/2<0`. The coefficient and resulting point have polynomial rational
encoding. This argument works even if every minimizing quality is an
endpoint; no assumed numerical interior margin is needed.

Concrete edge cases confirm why the distinctions are needed. On
`P={0<=q<=1,r=0}`, the minimum is zero at endpoint zero, although `P`
has interior-quality points: the interior branch must reject. On
`P={1/2<=q<=1,r=2q-1}`, the minimum is zero only at endpoint one and
must also reject. On `P={0<=q<=1,r=(4/5)q-4/25,0<=r<=1}`, the unique
zero minimum is at the rational interior quality `2/5` and must accept.
The proof handles all three exactly.

## Exact convex QP and rational witnesses

I opened the original full article by Kozlov, Tarasov, and Khachiyan,
[*The polynomial solvability of convex quadratic programming*](https://www.mathnet.ru/eng/zvmmf5189),
1980. Printed page 1320 defines exact solution to include the exact
optimal value and an attaining point and states polynomial running time
in binary input length. Printed page 1321 derives rational optimizer
coordinates from active KKT linear systems and determinant bounds,
and explicitly bounds the numerator and denominator of the optimal
value. The primary text therefore supports the primitive needed here,
including exact sign comparison and polynomial-size rational solutions.
Clearing rational input denominators incurs only polynomial bit growth.

After the interior procedure, division by `q` or `1-q` recovers rational
bypass flows of polynomial encoding length. Rational addition recovers
feeds and outlets. A small numerical value of a denominator does not
invalidate this bit bound: it is still a nonzero rational number with
polynomial numerator/denominator encoding. Physical feasibility follows
from the exact identities already checked. Endpoint LP witnesses are
rational as well.

## Scope and remaining evidence

The vector-quality extension is correct when source vectors take only
two distinct values: all active mixtures lie on their affine line;
positive exact products outside it are rejected, and all coordinates
reduce to its scalar parameter. This is a two-distinct-vector assumption,
not merely affine rank one with many distinct source values.

Exact source supplies and exact product demand/quality contracts are
essential to the balance elimination. Zero outlet lower bounds are
essential to the common convex epigraph direction: a positive lower
bound yields an inequality of the opposite curvature. The theorem
does not impose a restrictive common pool capacity or optimize arbitrary
individual arc costs. Standard node economics is constant under the
exact throughput contracts.

This is an independent proof and primary-primitive audit. The author's
original-model numerical comparisons will provide separate evidence;
they are not needed to justify the exact algebra or bit complexity.
The novelty of this precise physical subclass remains subject to its
separate bounded literature assessment.

## Addendum: restrictive common pool upper capacity is covered

The common-capacity exclusion in the initial candidate is unnecessary.
Sum the exact output identity over all products and write `T=sum_j v_j`:

```
sum_j W_0j = q sum_j b_j(B_j-1)+q(1-q)T.
```

For `0<q<1`, the upper bound `T<=U_pool`, with `U_pool>=0`, is exactly
equivalent to the concave quadratic upper inequality

```
sum_j W_0j <= q sum_j b_j(B_j-1)+U_pool(q-q^2).
```

Replace `q^2` by the same shared `r`. Because its coefficient is
`-U_pool<=0`, requiring `r>=q^2` strengthens this row in the same
direction as every local outlet upper bound. An original point extends
with `r=q^2`; conversely every lifted point satisfies the original pool
capacity. The endpoint original LPs retain the common bound directly.
Thus arbitrary finite nonnegative common pool upper capacity is covered
without any new variable, quadratic condition, or change to the exact
interior procedure. The common lower bound remains zero.

The same identity also handles a rational upper resource row
`sum_j alpha_j v_j<=U` whenever `U>=0`: multiply each output identity
by its specified coefficient and sum. This gives another linear row
in `(q,r,w)` with coefficient `-U` on `r`. The coefficients `alpha_j`
need not share a sign for this algebra, although ordinary upper resource
bounds usually have nonnegative coefficients. This observation does
not cover arbitrary mixed input/bypass resource rows or positive lower
outlet requirements. It can be retained as an optional extension rather
than broadening the core physical theorem unnecessarily.

## New extension proposed for independent review: variable input supplies

The input exact-contract assumption also appears removable for feasibility.
Keep every product's exact demand `b_j` and exact normalized quality `B_j`,
but permit each input's actual consumed amount `A_i` to lie in its given
rational interval. Global conservation fixes the total consumed amounts
of the two source classes, irrespective of their division among inputs:

```
A_1_total=sum_j b_j B_j,
A_0_total=sum_j b_j(1-B_j).
```

For an interior quality, let `gamma_i=-q` or `1-q` according to its class.
In addition to scaled bypass flows, retain scaled actual source throughput
`t_i=gamma_i A_i` and scaled pool intake `h_i=gamma_i y_i`. Supply intervals
give affine bounds on `t_i`; feed-arc intervals give affine bounds on `h_i`.
Use `h_i=0` for a missing feed arc. Each input's conservation becomes

```
t_i=h_i+sum_j w_ij.
```

Impose the two affine class-total equations

```
sum_(i in I_0) t_i=-q A_0_total,
sum_(i in I_1) t_i=(1-q) A_1_total.
```

All product equations, individual outlet bounds, and the optional common
pool upper bound use precisely the existing convex formulation. Summing
input conservation and product equations gives

```
sum_i h_i
 = -q A_0_total+(1-q) A_1_total-sum_j b_j(B_j-q)
 = 0.
```

After division by each nonzero `gamma_i`, this says
`sum_i C_i y_i=q sum_i y_i`, the actual pool quality equation. The class
totals also give total actual source consumption `sum_j b_j`; subtracting
all bypass flows gives pool mass conservation. Hence no new nonlinear
aggregate equation is required. Conversely any original feasible network
has those class totals, so scaling supplies all these rows.

All new variables have finite affine bounds from their physical intervals
or incident capacities. Thus the rational polytope remains compact and
the same rank-one convex QP and strict-interior procedure apply. Rational
recovery divides `t_i,h_i,w_ij` by nonzero rational scalings. Endpoint
qualities still use the complete original fixed-quality LPs.

This extension has been sent to the author and root for a separate
independent check; it is not covered by the PASS verdict for the original
candidate at the top of this review. If accepted, the resulting theorem
would require exact product demand/quality but allow arbitrary rational
input supply intervals and positive feed lower bounds. With variable
input consumption, arbitrary standard input costs cease to be constant;
the extension claims feasibility only. Costs uniform within each source
quality class remain constant by the fixed class totals.
