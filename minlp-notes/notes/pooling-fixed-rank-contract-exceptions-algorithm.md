# Candidate: contracted path pooling with fixed affine quality rank

Date: 2026-09-05. Status: full candidate proof. Two independent audits,
[benders_review](review-pooling-fixed-rank-contract-exceptions-benders.md) and
[pooling_all_two_review](review-pooling-fixed-rank-contract-exceptions-second.md),
report PASS for the stated fixed-rank, fixed-exception theorem.
This extends the separately reviewed scalar transformation.
Priority for the physical class is not established.

## 1. Statement and retained assumptions

Use the model in
[the scalar contract-exception note](pooling-bounded-contract-exceptions-algorithm.md):
one pool, a bypass graph of maximum degree two, arbitrarily many pool
feeds and outlets, finite rational individual arc bounds, and a fixed
number `s` of exceptional input/output nodes. Nonexceptional inputs have
exact total supplies. Nonexceptional outputs have exact demands and
exact conserved quality vectors. Exceptional nodes may have ordinary
interval requirements. Common pool-throughput bounds are redundant:
the lower bound is zero and the upper bound is certified by a valid
throughput bound, such as the minimum of total input-throughput upper
bounds, total pool-feed arc capacities, and total pool-outlet arc capacities. Standard input-cost/output-revenue profit is
the objective. A nonredundant common pool bound and unrestricted dense
individual arc costs remain outside the statement.

There may now be arbitrarily many quality coordinates. Assume the affine
rank `t` of the input-quality vectors is fixed. The candidate conclusion
is polynomial rational bit-time feasibility and exact standard economic
optimization, with an exact algebraic original optimizer. The polynomial
exponent may depend on `s,t`. No degree-two witness bound is claimed.

Compute a rational affine basis and use basis coordinates `C_i in Q^t`
for the input vectors. This is polynomial-bit rational linear algebra.
A positive-demand nonexceptional product vector must lie in this affine
hull; otherwise the instance is infeasible. Express every such product
as `B_j in Q^t`. A zero-demand product has zero incoming flows, so its
quality vector can be replaced by any vector in the hull. All original
exceptional-output quality inequalities remain as affine functions of
the basis quality mass and throughput.

For rank zero, every active blend has the same known quality vector.
The complete model is an LP after retaining compatible quality bounds.
Assume `t>=1` below. Remove an unusable pool only after forcing its
incident arcs to zero and checking those bounds; keep external contracts.

## 2. Fixed core and actual pool balances

Retain the same exceptional pool arcs and bypass arcs `H` as in the
scalar proof, and a vector `q in R^t` for pool quality. A coordinatewise
box spanned by allowed feed vectors is a valid compact search region.
Inactive pools can be assigned a source vector in that box.

Exceptional input throughput `A_i`, exceptional output throughput `D_j`,
and exceptional output basis-quality mass

```
M_j = q*v_j + sum_i C_i*z_ij
```

use only the core. Impose the total mass equation and the `t` coordinate
quality equations

```
sum_nonexception_inputs a_i + sum_exception_inputs A_i
 = sum_nonexception_outputs b_j + sum_exception_outputs D_j,

sum_nonexception_inputs C_i*a_i + sum_exception_inputs C_i*A_i
 = sum_nonexception_outputs B_j*b_j + sum_exception_outputs M_j. (1)
```

Eliminate ordinary feed and outlet flows by their exact node contracts.
At an ordinary output the remaining vector equation is

```
sum_i (C_i-q) z_ij = b_j(B_j-q).                       (2)
```

Exactly the scalar conservation proof, coordinate by coordinate, shows
that (1)--(2) and local flow rows imply actual pool mass and vector-quality
balances. At zero throughput all nonnegative pool arcs vanish. At positive
throughput `q` is the actual weighted average of the intake vectors.
Thus bounding `q` by the feed-coordinate box loses no feasible flow.

## 3. Polynomially many nonsingular projection charts

At every source vector `q=C_i` lying in the search box, solve the original
fixed-vector-quality LP, including all pool balances and economics.
These are at most `|I|` rational LPs.

For all other `q`, choose a direction from the following explicit family:

```
beta(k)=(1,k,...,k^(t-1)),
k=1,..., |I|*(t-1)+1.                                (3)
```

For fixed `q!=C_i`, the polynomial `beta(k)·(C_i-q)` is nonzero and has
at most `t-1` roots in `k`. The union of the forbidden values over all
inputs therefore cannot cover (3). Hence at least one direction has

```
gamma_i(q)=beta·(C_i-q) != 0   for every input i.       (4)
```

There are polynomially many directions because `t` is fixed, and their
rational encoding is polynomial. It is harmless that charts overlap.
For each chart retain only parameter points satisfying (4). Partition
further by signs of the affine coefficient functions used below. In
fixed dimension, the realizable sign conditions of polynomially many
affine functions have polynomial size; retain their lower-dimensional
cells as well. This is an ordinary hyperplane-arrangement operation.

Define signed flows `w_ij=gamma_i(q) z_ij`. On each chart this is invertible.
Add these transformed coordinates for retained bypass arcs and their
bilinear links. The core has at most `t+5s` coordinates.

## 4. Exact local reduction with vector qualities

Projected equation (2) gives the incidence node equation

```
sum_i w_ij=R_j(q),    R_j(q)=b_j beta·(B_j-q).          (5)
```

At an ordinary input its bypass-total interval becomes an interval
on outgoing `w`, with affine bounds in `q`. Original bypass bounds also
become affine arc bounds. The signs of all `gamma_i` fix their order.

At an ordinary output with two bypass inlets, label their vectors
`C_1,C_2`, projected constants `c_h=beta·C_h`, and transformed flows
`w_1,w_2`. Its outlet-flow bounds constrain total bypass `s_j` to a fixed
rational interval `[L_j,U_j]`.

If `c_1!=c_2`, precisely the scalar calculation gives

```
w_1 = gamma_1 [R_j-gamma_2*s_j]/(c_1-c_2).            (6)
```

Its two endpoint expressions are quadratic polynomials in `q`, and their
order is fixed by the signs of `gamma_1,gamma_2,c_1-c_2`. If `c_1=c_2`,
equation (5) instead fixes `gamma_1*s_j=R_j`; the flow bounds give pure
parameter conditions. No division by `c_1-c_2` occurs in that case.

The remaining coordinate equations in (2) must also be retained.
For each basis coordinate `h`, use `w_2=R_j-w_1` and multiply its equation
by `gamma_1 gamma_2`. The result is

```
a_h(q) w_1 = f_h(q),                                 (7)

a_h=(C_1h-q_h) gamma_2 - (C_2h-q_h) gamma_1,
f_h=gamma_1 [ b_j(B_jh-q_h) gamma_2
             -(C_2h-q_h) R_j ].
```

The quadratic terms in `a_h` cancel, so `a_h` is affine. Inside the
brackets in `f_h`, the quadratic terms also cancel because
`R_j=b_j beta·(B_j-q)`. Thus `f_h` has degree at most two. These equations
hold whether or not `c_1=c_2`.

Include every affine `a_h` in the chart's sign partition. Where `a_h=0`,
keep the pure parameter equality `f_h=0`. Otherwise equation (7) is
the lower and upper arc bound `w_1=f_h/a_h`. Its denominator has known
nonzero sign. All equations can be assigned to the same selected incident
arc. This gives rational bound candidates of numerator degree at most
two and denominator degree at most one. There are only polynomially many
candidates, even if redundant original quality rows are retained.

With a single bypass inlet, equation (5) fixes its transformed flow
`w=R_j`. Every additional coordinate of (2) becomes the pure parameter
equation `(C_ih-q_h)R_j=b_j(B_jh-q_h)gamma_i`, of degree at most two.
Its outlet interval gives an additional affine arc interval as in the
scalar proof. With zero bypass inlets, retain every equation
`b_j(B_j-q)=0` and require zero to satisfy the bypass-total interval.

Consequently the full ordinary-node system is an incidence flow system
with affine node bounds, rational constant-degree arc bound candidates,
and polynomially many pure parameter conditions. No vector-quality
equation has been discarded.

## 5. Boundary projection stays polynomial and constant degree

Delete exceptional nodes. For every retained boundary arc, remove it
from the internal graph, shift its signed transformed flow from both
adjacent node-divergence bounds, and keep all its capacity/equality
conditions separately in the core. Internal components remain paths,
cycles, or isolated nodes.

Apply the signed Hoffman inequalities to connected induced subsets.
There are at most quadratically many subsets, and each cut crosses at
most two internal arcs. Replace effective min/max bounds by the
conjunction over all bound-candidate combinations. Candidate lists may
now have polynomial size, but at most two lists occur in any cut, so the
number of combinations remains polynomial. Include every lower-versus-
upper candidate consistency inequality for each arc.

Each expanded cut contains at most two rational capacity candidates.
Clear only their selected denominators, whose nonzero signs are known
on the current cell. A product of at most two affine denominators has
degree at most two. Node sums are affine in `q` and linear in boundary
coordinates. Therefore the resulting polynomial rows have constant
degree (degree four is a safe bound) and polynomial coefficient length.
The same bound applies to candidate consistency and boundary rows.
It is unnecessary to multiply the denominators of all internal arcs.

This is the key distinction from a general dense aggregate or arbitrary
high-degree cut: here the cut boundary contains at most two arcs.

## 6. Exact optimization and recovery

For each of the polynomially many chart/sign cells, combine these rows,
the retained physical constraints, and global equations (1). The number
of variables is bounded by `t+5s`, and polynomial degrees are bounded by
a constant. Fixed-dimensional real algebraic elimination therefore gives
polynomial bit-time decision and the attainable values of the standard
economic objective. That objective has the same affine core expression
as in the scalar note, because every ordinary node's total throughput
is fixed.

Take the union of attainable-value descriptions over all open or
lower-dimensional chart cells and all fixed-source-vector LPs. Their
union is exactly the original attainable-value set. The original model
with the chosen compact quality box has a closed bounded feasible set,
so any feasible instance has an attained maximum. Sample an attaining
core point from an actual cell. As in the scalar proof, do not replace
open chart conditions by their closures.

At the sampled core solve each signed incidence system over its common
represented real-algebraic field. Its constant integral coefficient
matrix implies a feasible vertex with coordinates that are rational
linear combinations of the sampled bounds. Evaluating the rational
bound candidates and recovering `z=w/gamma_i` stays in that same field.
Its degree and coordinate encodings are polynomial because the core
dimension is fixed and all transformations have polynomial encoding.
Recover eliminated pool arcs by the exact local contracts. Equations
(1) ensure actual global pool balances for every such local lift.

The result is not a general fixed-rank pooling algorithm: most external
contracts must be exact, bypass degree must be at most two, and the
shared pool bound must be redundant. Standard circulation, affine-basis
reduction, sign decomposition, and fixed-dimensional real algebra are
established tools. The claimed new contribution, if its source audit
holds, is this combined physical model and its exact algorithm.

## 7. Distinct verification evidence

The author checker
[check_fixed_rank_scaled_cuts.py](../code/pooling_bypass_paths/check_fixed_rank_scaled_cuts.py)
compares exact transformed cuts against an independently formulated
original physical LP retaining every pool arc and every vector-quality
balance. It passed 164 fixed-quality-vector fibers, of which 57 were
feasible, and 1,461 nonsingular chart comparisons. A further 193
source-vector singular cases use the original LP branch. Cases include
two and three quality coordinates, cycles and cut paths, missing pool
arcs, equal projected qualities, and repeated full input vectors.

Dropping the additional vector equations admitted false positives in
678 chart cases. This negative control checks that projecting onto one
quality direction alone is insufficient. The
[output](../code/pooling_bypass_paths/fixed_rank_scaled_cuts_output.txt)
distinguishes exact rational cut arithmetic from numerical HiGHS physical
LP decisions. These checks do not implement the full chart arrangement,
bounded-exception optimization, or real-algebraic global algorithm;
those require the mathematical proof and its independent audits.
