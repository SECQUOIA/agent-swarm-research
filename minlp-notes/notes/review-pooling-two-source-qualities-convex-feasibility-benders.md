# Independent audit: two source qualities and arbitrary bypass topology

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS, including the stronger source-interval theorem.** I
independently checked the full final draft in
[the candidate](pooling-two-source-qualities-convex-feasibility.md).
The reviewed scope includes arbitrary input supply intervals, positive
individual feed lower bounds, a restrictive nonnegative common pool
upper bound, and the optional outlet resource inequalities with
nonnegative right-hand sides. Product demands and qualities remain
exact, and individual pool-outlet and common pool lower bounds remain
zero. The conclusion is polynomial-bit exact feasibility and rational
physical witness recovery, without a bypass topology restriction.

## Signed output identity and convexity

Normalizing two distinct scalar source qualities to zero and one is
an invertible rational affine change of quality. Positive-demand
products outside their interval are impossible. Zero-demand product
quality rows are homogeneous and impose no extra mass condition once
incoming nonnegative flows vanish. One source quality and unusable
pools reduce to the original fixed-quality LP after preserving all
node and incident-arc bounds.

On `0<q<1`, multiplying class-zero bypass flows by `-q` and class-one
flows by `1-q` is invertible. The class-zero interval order reverses;
the class-one order does not. This correctly converts all individual
bypass and fixed-source feed bounds into affine inequalities without
any bound on node degree.

For one product, let `z_0,z_1` denote its total bypass flow from the
two classes. Its physical equations give `b*B=q*v+z_1` and
`b=v+z_0+z_1`. Consequently

```
b*(B-1)=-(1-q)*v-z_0,
W_0=-q*z_0=q*b*(B-1)+q*(1-q)*v.
```

This independently proves the key identity for arbitrary numbers of
inlets, including an empty class or no bypass inlets. Since `q*(1-q)>0`,
the two-sided transformed inequality is exactly `0<=v<=U`, not a
relaxation. An absent outlet has `U=0` and is forced to zero. Original
nonnegative bypass flows additionally imply `v<=b` automatically.

Introducing one shared variable `r>=q^2` is sound for every outlet
simultaneously. Each coefficient `U` is nonnegative, so replacing
`U*q*(1-q)` by `U*(q-r)` tightens the upper bound. Every original
point is represented by `r=q^2`; every represented point satisfying
`q^2-r<=0` is physically feasible. The bound `r<=1` loses no original
point. This is an exact existential convex formulation.

The common pool upper bound follows by summing the same identity over
all products. It can be restrictive: the identical substitution with
its nonnegative upper bound preserves both directions of equivalence.
More generally, multiplying by any rational coefficients `alpha_j`
and summing proves the optional resource-row extension. The signs of
the `alpha_j` do not matter. The needed sign is the nonnegative right-
hand side `U`, which controls the direction of the `r` substitution.

## Exact-source global balances

With fixed input supplies, the total mass and class-one quantity checks
are necessary. Recovering each feed and outlet from its exact node
contract makes their total mass difference equal to the checked global
mass difference. Summing the transformed output quality equations and
using the checked total class-one quantity gives the actual pool
quality balance. Hence the local transformed system has not dropped
global constraints. At zero pool throughput, nonnegativity forces all
pool arcs to vanish; no division by throughput is used.

## Arbitrary source intervals: independent balance reconstruction

Exact product demands and qualities determine the two consumed source
class totals `A_0=sum b*(1-B)` and `A_1=sum b*B`. This does not fix
the individual input consumptions and therefore permits arbitrary
input supply intervals.

Keep `t_i=gamma_i*A_i` and `h_i=gamma_i*y_i`. Their interval constraints
are affine because each class's scaling sign is fixed on the interior.
The same applies to positive feed lower bounds; a missing feed means
`h_i=0`. The scaled input equation
`t_i=h_i+sum_j w_ij` is equivalent to actual input conservation after
division by the nonzero scaling factor.

Dividing the two class-total equations recovers exactly the consumed
totals `A_0,A_1`. Thus total input consumption equals total product
demand. Summing recovered input and output mass equations gives actual
pool mass balance. Independently,

```
sum_i t_i=-q*A_0+(1-q)*A_1
         =sum_j b_j*(B_j-q)=sum_ij w_ij.
```

Summing scaled input conservation therefore gives `sum_i h_i=0`.
Since `h_i=-q*y_i` in class zero and `(1-q)*y_i` in class one, this
is exactly `sum_class_one y_i=q*sum_all y_i`, the normalized physical
pool quality balance. All recovered intake and bypass bounds are
preserved. Output nonnegativity and capacities follow from the same
output identity as before. No unverified class resource or global
quality equation remains.

These extra variables and equations increase the polytope size only
polynomially. Finite supply/feed/bypass bounds and `0<=q<=1` give
finite bounds on `t,h,w`. The only nonlinear test remains
`F=q^2-r<=0` over a rational compact polytope, with rank-one positive
semidefinite Hessian.

## Singular endpoints, exact QP, and rational witnesses

The algorithm uses original physical LPs at `q=0,1`, retaining all
actual supply intervals, capacities, resource rows, and both pool
balances. Singular transformed equations are never accepted as
endpoint witnesses.

The auxiliary LP maximizing a margin below both `q` and `1-q`
determines whether the linear polytope has an interior-quality point.
If its optimum is positive, a rational optimal LP point supplies such
a point with polynomial encoding length. It need not yet satisfy the
quadratic inequality.

The exact convex-QP primitive used next is applicable in arbitrary
dimension. I checked the primary Kozlov–Tarasov–Khachiyan paper,
[1980 full text, printed pages 1320–1321](https://www.mathnet.ru/php/getFT.phtml?jrnid=zvmmf&option_lang=eng&paperid=5189&what=fullt).
It explicitly treats exact optimum values and attaining points with
polynomial binary complexity; its active-system determinant argument
also supplies rational encoding bounds. Rational input rows can be
cleared to integer rows with polynomial bit length. This invocation
does not rely on a generic exact-SOCP feasibility theorem.

For the resulting exact minimum `m`, the three cases are exhaustive.
If `m>0`, feasibility fails. If `m=0`, two minimizers with different
quality coordinates would have midpoint value
`-(q_1-q_2)^2/4<0`, a contradiction. Thus all minimizers share the
same quality coordinate. An interior minimizer is a witness; an
endpoint minimizer rules out any interior point with `F<=0`.

If `m=-rho<0`, the proposed rational combination with the previously
found interior point stays in the polytope and has interior quality.
The bounds on `q,r` imply `F(p)<=1`, so the chosen
`lambda=rho/[2*(rho+1)]` gives `F<=-rho/2<0`. All numbers involved
have polynomial rational encoding. This argument handles arbitrarily
small margins and degenerate feasible sets without numerical tolerance
assumptions.

Dividing the rational transformed witness by the nonzero rational
class factors recovers polynomial-bit original flows. Sums used in
local recovery preserve polynomial bit length. If the recovered pool
is inactive, its reported quality can be reassigned to an allowed
feed quality, because all incident pool flows are zero. Endpoint
solutions are rational original LP witnesses. The theorem therefore
does prove rational physical witness existence and construction.

## Scope and verification evidence

With arbitrary many conserved attributes but only two distinct full
source-quality vectors, an affine-line coordinate reduces every
positive-demand product equation exactly. Products outside that line
must be rejected; zero-demand semantics are unchanged. This is a
restriction on all source vectors, not merely on the two sources that
happen to feed the pool. The seven-source-quality hardness construction
therefore presents no contradiction.

Positive outlet or common pool lower bounds have the opposite
curvature and are not covered by this proof. For variable source
consumption, standard procurement costs are no longer constant and
the argument does not optimize them. Arbitrary arc-cost optimization
is likewise not established.

The author's original-network checks support the fixed-source mapping
and the need to preserve outlet lower bounds. They are numerical QP
and global pooling comparisons, not exact certificates or tests of
every arbitrary-supply case. I did not duplicate those runs. This
audit independently verifies the general source-interval proof,
capacity strengthening, strict-interior decision, and bit-complexity
claims. Priority for the pooling specialization remains subject to
the separate literature assessment.
