# Two source-quality vectors give exact convex pooling feasibility

Date: 2026-09-05. Status: verified theorem, including arbitrary source
supply intervals and restrictive common upper capacity. Two independent
full-scope audits passed: [first](../notes/review-pooling-two-source-qualities-convex-feasibility-benders.md)
and [second](../notes/review-pooling-two-source-qualities-source-intervals-independent.md).
The [earlier audit](../notes/review-pooling-two-source-qualities-convex-feasibility-second.md)
verifies the exact-source specialization and capacity strengthening.
The [primary-source comparison](../notes/pooling-two-source-qualities-convex-feasibility-novelty.md)
found no matching restricted theorem in the papers checked; this is not
exhaustive priority clearance.

**Theorem.** One-pool feasibility with at most two distinct complete
source-quality vectors is decidable in polynomial rational bit time,
with a polynomial-encoding rational original-flow witness. The bypass
graph, source count, product count, and quality-coordinate count are
unrestricted. Sources may have arbitrary finite rational supply intervals;
products have exact demands and exact qualities. Individual feed and
bypass arcs may have positive lower bounds. Pool-outlet and common pool
lower bounds are zero; their upper bounds may be restrictive. The result
concerns feasibility, not variable procurement or arbitrary arc-cost
optimization.

The proof first gives the exact-source specialization, then removes that
assumption in Section 6 without changing the single convex-QP primitive.

## 1. Physical class

Consider standard one-pool pooling with an arbitrary direct bypass graph,
arbitrarily many inputs, outputs, feed arcs and outlet arcs, and no
pool-to-pool arcs. Every input has an exact rational total supply `a_i`.
Every output has an exact rational demand `b_j` and exact scalar quality
`B_j`. There are at most two distinct rational input-quality values.
Every arc has finite rational upper and lower flow bounds, including
nonnegativity, except that every pool-outlet lower bound is zero.
The common pool lower bound is zero; an arbitrary rational nonnegative
common pool upper bound is allowed.
There are no other aggregate rows or economic requirements.

**Exact-source specialization.** Feasibility is decidable in polynomial rational
bit time. If feasible, the algorithm constructs an original rational
feasible flow of polynomial encoding length. No degree restriction on
the bypass graph or bound on the number of external nodes is needed.
Standard input costs and output revenues are constant on this class;
arbitrary arc-cost optimization is not claimed.

With one input-quality value, all active blends have that known value
and the model reduces to an LP. For two values, normalize them affinely
to zero and one. Let `I_0,I_1` be their source classes. Normalize product
qualities by the same affine map. Positive-demand qualities outside
`[0,1]` are infeasible. A zero-demand product's quality is immaterial.
An unusable pool is removed only after its incident zero-flow constraints
are checked; retain all external requirements and solve the resulting LP.

The necessary global constants are

```
sum_i a_i=sum_j b_j,
sum_(i in I_1) a_i=sum_j b_j B_j.                    (1)
```

Check (1) exactly. Individual missing pool arcs are represented by zero
capacity. An omitted common pool upper bound can be replaced by the minimum of
total source supply, total feed-arc capacities, and total outlet-arc
capacities. A restrictive explicitly supplied upper bound is retained.

## 2. Signed scaling with arbitrarily many bypass inlets

Handle `q=0` and `q=1` by the original fixed-quality physical LPs,
including all pool arcs and both pool balances. For the remaining
case `0<q<1`, define one signed variable for each bypass arc:

```
w_ij=-q z_ij             if i in I_0,
w_ij=(1-q) z_ij          if i in I_1.                 (2)
```

This change is invertible in the open interval. Original bypass bounds
become affine bounds in `q` on each `w`, with the appropriate reversed
order for class zero. Feed bounds remain affine as well: eliminate
`y_i=a_i-sum_j z_ij`, and multiply its bypass-total interval by the
source's factor in (2). This is an interval on `sum_j w_ij`, even when
the source has arbitrarily many bypass arcs. Positive inlet lower
bounds are permitted by this linear step.

For an output let

```
W_0j=sum_(i in I_0) w_ij,
W_1j=sum_(i in I_1) w_ij,
R_j(q)=b_j(B_j-q).
```

Its exact mass and quality imply

```
W_0j+W_1j=R_j(q).                                   (3)
```

The original total bypass flow is
`s_j=-W_0j/q+W_1j/(1-q)`. Eliminating `W_1j` using (3), and writing
`v_j=b_j-s_j`, gives the exact identity

```
W_0j=q b_j(B_j-1)+q(1-q) v_j.                       (4)
```

It holds for any number of bypass inlets, including an empty source
class at that output. If the outlet has upper capacity `U_j>=0` and
lower bound zero, (4) is exactly equivalent to

```
q b_j(B_j-1) <= W_0j
 <= q b_j(B_j-1)+U_j q(1-q).                        (5)
```

The upper bound is concave quadratic in `q`; the lower bound is affine.
For an absent outlet use `U_j=0`, which forces its flow to zero.
No summation over bypass paths and no connected-cut enumeration occurs.

A common throughput upper bound `T=sum_j v_j<=U_P`, with `U_P>=0`,
has the same form after summing (4):

```
sum_j W_0j <= q sum_j b_j(B_j-1)+U_P q(1-q).          (5a)
```

Thus restrictive pool capacity is included, without a path projection
or another aggregate variable.

Every input constraint, every original transformed arc bound, equation
(3), and the lower inequality in (5) is affine in the full variable set
`(q,w)`. The upper inequalities are the only nonlinear constraints.

Summing (3) and using (1) proves the actual pool quality balance after
local feed/outlet recovery, just as in the reviewed contracted model.
The mass constant gives actual pool conservation. At zero throughput,
nonnegativity forces all pool arcs to vanish. Thus no aggregate balance
is missing from the transformed model.

## 3. A single convex quadratic condition

Introduce one variable `r` and replace every upper inequality in (5) by

```
W_0j <= q b_j(B_j-1)+U_j(q-r).                       (6)
```

Use the identical replacement `U_P(q-r)` in the shared capacity row
(5a). Let `P` be the rational polyhedron comprising all these linear rows,
the preceding affine physical rows, and `0<=q<=1`, `0<=r<=1`. Original
finite capacities bound every `w`, so `P` is compact.

For a fixed interior `q`, the original transformed constraints are
feasible exactly when there is `(q,r,w) in P` satisfying

```
F(q,r,w)=q^2-r <= 0.                                (7)
```

Indeed, original feasibility gives `r=q^2`. Conversely `r>=q^2` makes
the right side of (6) no larger than its original concave upper bound,
because `U_j>=0`. Thus (6)--(7) imply (5). Restricting `r<=1` loses
no original point, since `0<=q<=1`.

The Hessian of `F` is positive semidefinite of rank one. Feasibility of
the closed model reduces to minimizing this rational convex quadratic
over a rational polytope. Exact convex quadratic programming is a
classical polynomial bit-time problem, with a polynomial-encoding
rational optimum. This is an invocation of convex QP, not a generic
claim about exact SOCP feasibility.

## 4. Exclude singular endpoint artifacts exactly

The original endpoint LPs were already handled separately. Their
transformed limits must not be accepted as substitutes, so require
`0<q<1` explicitly. The following procedure uses only rational LPs and
one exact convex QP.

First maximize `epsilon` over `P` with
`epsilon>=0`, `epsilon<=q`, and `epsilon<=1-q`. If this LP is infeasible
or its optimum is zero, `P` has no interior-quality point and this
branch is infeasible. Otherwise retain a polynomial-bit rational point
`p in P` with `0<q_p<1`.

Next minimize `F` over `P`, obtaining rational optimizer `x*` and exact
rational value `m`.

- If `m>0`, no feasible interior point exists.
- If `m=0`, every minimizer has the same quality coordinate `q*`.
  Otherwise the midpoint of two minimizers with different quality
  coordinates would have strictly smaller objective, since the only
  quadratic term is `q^2`. Thus the branch is feasible exactly when
  `0<q*<1`, and the rational optimizer is a witness.
- If `m=-rho<0`, combine `x*` with the retained interior point `p`.
  Since `F(p)<=1`, choose the rational
  `lambda=rho/[2(rho+1)]` and put
  `x=(1-lambda)x*+lambda p`. Then `0<q_x<1` and convexity gives
  `F(x)<=-rho+lambda(rho+1)=-rho/2<0`. This is a polynomial-bit
  rational witness.

The case distinction is exact even if feasible qualities occur only at
one rational interior value or if all closed minimizers lie at an
endpoint. It needs neither an assumed numerical margin nor an oracle
for strict convex feasibility.

Recover each original bypass flow from (2), then feeds and outlets from
their exact node contracts. All recovered values are rational, and every
division is by a nonzero rational number of polynomial encoding length.
Original bounds and all quality balances hold by Sections 2--3. At an
inactive pool the reported quality can be assigned arbitrarily to an
allowed feed value. Endpoint witnesses come from the original rational
LPs. This proves the constructive and bit-complexity claims for the specialization.

## 5. Scope, sources, and further checks

The same reduction applies to arbitrarily many conserved quality
coordinates if the input vectors take only two distinct values: use
their affine-line coordinate, reject incompatible positive-demand
product vectors, and retain homogeneous zero-demand semantics. The
statement restricts the number of distinct source vectors, not the
number of physical inputs or bypass arcs.

The same reasoning permits extra output-flow resource rows
`sum_j alpha_j v_j<=U` with rational coefficients and `U>=0`: multiply
(4) by the coefficients, sum, and use the same `U(q-r)` upper bound.
The coefficient signs do not affect that identity or the direction of
the replacement. This optional extension adds only linear rows to `P`.

Positive pool-outlet lower bounds would add the lower condition
`W_0j>=q b_j(B_j-1)+ell_j q(1-q)`. It has the opposite curvature and
is not covered by this convex formulation. A positive common pool
lower bound has the same issue. Unrestricted dense arc-cost optimization
is likewise not included.
The seven-quality constant-data hardness construction therefore does
not contradict this two-quality feasibility theorem.

The exact convex-QP primitive is due to Kozlov, Tarasov, and Khachiyan,
[*The polynomial solvability of convex quadratic programming*](https://www.mathnet.ru/eng/zvmmf5189),
1980, with a 1979 announcement. Polynomial-size rational witnesses also
follow from the standard rational quadratic-programming witness result;
the proof here uses the convex algorithm to construct them. The candidate contribution is the two-quality pooling reduction with arbitrary
bypass topology and source supply intervals, not convex-QP solvability.
The full-scope audits and bounded primary-source comparison are linked above.

## 6. Arbitrary source supply intervals

The exact-source-contract assumption can be removed. Retain exact
product demands and qualities, two distinct source-quality values,
zero pool-outlet lower bounds, arbitrary individual feed bounds, and
an arbitrary nonnegative common pool upper bound with lower bound zero.
Each input may now have an arbitrary finite rational supply interval.
This is still a feasibility and rational-witness theorem. Standard
production costs need not be constant in this stronger class, and no
economic optimization claim follows from the argument.

Write `A_i` for actual consumed input quantity and `y_i` for its actual
pool intake. Exact product contracts fix the total consumed quantities
of the two source classes:

```
A_0 = sum_j b_j(1-B_j),
A_1 = sum_j b_j B_j.                                 (8)
```

Indeed all original flows conserve total mass and the scalar quality,
so `sum_i A_i=sum_j b_j` and `sum_(i in I_1) A_i=sum_j b_j B_j`.
These are necessary constants determined by the products. The input
intervals themselves need not fix any individual `A_i`.

On `0<q<1`, keep each bypass scaling (2) and introduce

```
t_i=gamma_i A_i,  h_i=gamma_i y_i,
gamma_i=-q for class zero and 1-q for class one.      (9)
```

If the input supply interval is `[L_i,U_i]`, impose that `t_i` lies
between `gamma_i L_i` and `gamma_i U_i`, in the order fixed by its
class. Impose the corresponding interval on `h_i` from the actual
feed-arc bounds, including any positive lower bound. An absent feed
means `h_i=0`. These are affine rows. Replace the exact-source local
interval rows of Section 2 by

```
t_i=h_i+sum_j w_ij,                                  (10)
sum_(i in I_0) t_i=-q A_0,
sum_(i in I_1) t_i=(1-q) A_1.                        (11)
```

All these equations are linear in `(q,t,h,w)`, because `A_0,A_1` in
(8) are fixed product constants. Original bypass bounds, every output
row (3)--(6), and the common pool-capacity row remain unchanged.

The mapping is exact in both directions. Given an original feasible
flow with interior quality, (8)--(11) follow from conservation. In
the reverse direction divide by the nonzero class scalings to recover
`A_i,y_i,z_ij`. Their bounds and input conservation follow from
(9)--(10). Class sums (11) give actual total consumed supply
`A_0+A_1=sum_j b_j`, hence total recovered pool intake equals total
recovered pool outlet. Further,

```
sum_i t_i=-q A_0+(1-q) A_1
         =sum_j b_j(B_j-q)=sum_ij w_ij.
```

Summing (10) therefore gives `sum_i h_i=0`. By (9) this is

```
-q sum_(i in I_0) y_i+(1-q) sum_(i in I_1) y_i=0,
```

which is exactly the physical pool quality balance. At zero throughput
all recovered nonnegative pool arcs vanish as before. The output bound
identity (4) gives every outlet's actual nonnegative flow and upper cap.
Thus there is no missing class-level resource or hidden balance equation.

The expanded linear polytope has finitely bounded `t,h,w`, using finite
input and arc capacities and `0<=q<=1`. The sole nonlinear test is still
`q^2-r<=0`. Consequently Sections 3--4 give polynomial bit-time exact
feasibility and a polynomial-encoding rational original witness. For
`q=0,1`, solve the original physical LP with the actual supply intervals;
do not use the singular transformed equations.

At one source-quality value, use the ordinary fixed-quality LP directly.
The two-source-vector extension to arbitrarily many conserved attributes
also persists: all products must lie on the source affine line when
their demand is positive, and the scalar coordinate reduces every
conservation equation exactly.

Both full-scope independent audits explicitly passed the source-interval
extension and restrictive common upper capacity. These are part of the
theorem stated above.

## 7. Verification evidence

[The author checker](../code/pooling_bypass_paths/check_two_quality_convex_feasibility.py)
passed 160 original global pooling versus convex-QP decisions on arbitrary
dense bypass graphs: 148 were feasible. These include 64 cases with
nontrivial source supply intervals. Cases exercised endpoint LPs,
negative, zero, and positive QP minima, and infeasible interior linear
polytopes. They also include restrictive common pool upper bounds.
All optimization calls are numerical Gurobi solves; they are not exact
certificates for the full algorithm.

The explicit control uses two inputs of qualities zero and one, each
with exact supply one; two products have exact demands one and qualities
one and zero; only the high-quality input can bypass into the high-quality
product. Both pool outlets have cap one. Requiring pool flow at least
one half into the high-quality product makes the original model
infeasible. Removing that lower bound permits clean pool flow entirely
to the clean product and direct dirty flow to the dirty product. The
checker detects this change, confirming that positive outlet lower
bounds cannot simply be discarded.


The second full-scope reviewer also checked 240 exact rational networks,
including interior qualities `2^-80` and `1-2^-80`, zero-demand products,
positive shared auxiliary slack, and multiple conserved coordinates.
The checks covered 1,222 source equations, 913 product equations,
480 output resource rows, and 2,739 vector-quality equations. These exact
checks validate the scaling identities separately from numerical QP solves;
the general algorithmic guarantee follows from the proof.
