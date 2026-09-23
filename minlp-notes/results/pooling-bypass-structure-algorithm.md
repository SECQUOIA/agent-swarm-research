# Exact pooling optimization with controlled bypass structure

Date: 2026-09-05. Status: two independent mapping audits passed:
[first structural audit](../notes/review-pooling-bypass-vertex-cover.md),
[first rank-extension audit](../notes/review-pooling-quality-rank-extension.md),
and [fresh second audit](../notes/review-pooling-bypass-structure-second.md).
The underlying
[fixed-core block theorem](fixed-core-block-polyhedral-optimization.md)
has passed two independent reviews. Literature priority for this structural
pooling corollary remains provisional.

Standard pooling can be solved exactly in polynomial bit time when three
parameters are fixed: the pool count, the affine rank of the input-quality
vectors, and the vertex integrity of the bypass graph. Inputs, outputs,
quality attributes, and bypass arcs may all grow without bound. Bounded
vertex integrity means that deleting a fixed number of bypass endpoints
leaves components of bounded size. Thus the result permits a fixed number of arbitrarily large
bypass stars, an unbounded matching of bypass arcs, and combinations of these
patterns.

This is an exact complexity theorem based on real-algebraic algorithms. Its
parameter-dependent exponent may be large. It is not a practical runtime,
strongly polynomial, or fixed-parameter tractability claim.

## 1. Model and theorem

Let `I` be the input nodes, `J` the output nodes, and `p` the number of pools.
Each input has a rational quality vector `C_i in Q^K`. The nonnegative flows
are `y_iell` from inputs to pools, `v_ellj` from pools to outputs, and `z_ij`
on direct input-output bypass arcs. Missing arcs have flow zero. The bypass
graph `G` is the bipartite graph on `I union J` formed by the direct arcs.

The model allows rational lower and upper bounds on input, pool, output,
and individual arc throughputs, lower and upper output quality bounds, and
rational linear arc costs. Finite rational flow upper bounds are supplied,
or derived from finite input or output capacities. There are no
pool-to-pool arcs or unbounded families of binary design variables.

For nonempty `I`, define the affine quality rank by

```
t = dim span{C_i-C_i0 : i in I},
```

where `i0` is any input. Define the vertex integrity of `G` by

```
iota(G) = min_W ( |W| + max_component |V(component of G-W)| ),
```

where the maximum is zero when no vertices remain.

**Theorem.** For fixed bounds on `p`, `t`, and `iota(G)`, feasibility and
global optimization of this standard pooling model can be solved in time
polynomial in its rational input bit length. If feasible, an exact
real-algebraic optimum and optimizer of polynomial encoding length can be
returned. The numbers of inputs, outputs, attributes, and direct arcs need
not be fixed, and the output specification vectors can be arbitrary.

It suffices to assume fixed integers `c,h` such that deleting at most `c`
vertices from `G` leaves components of at most `h` vertices. This is
equivalent, for the present fixed-parameter statements, to bounded vertex
integrity. Bounded bypass vertex cover is the special case `h=1`.

The empty-input case has all flows zero and is checked directly; it does
not require assigning an affine rank to an empty set. Other elementary LP
cases are recorded in Section 7.

## 2. Compress the quality coordinates exactly

Choose one input-quality vector as `C_0`. Rational Gaussian elimination
gives independent basis vectors `b_1,...,b_t in Q^K` and rational input
coordinates `a_i in Q^t` such that

```
C_i = C_0 + sum_s a_is b_s.
```

The computation and its coefficient bit lengths are polynomial. This is
exact affine rank over rational data, not a numerical rank approximation.
Represent pool quality by `q_ell in R^t`, so attribute `a` has value

```
Q_ella = C_0a + sum_s b_sa q_ells.
```

Bound each `q_ells` between `min_i a_is` and `max_i a_is`. Positive-flow
pool coordinates are weighted averages of the input coordinates. Inactive
pools can take arbitrary boxed coordinates without changing any flow or
quality mass. Pool conservation becomes

```
sum_i y_iell = sum_j v_ellj,
sum_i a_is y_iell = q_ells sum_j v_ellj  (s=1,...,t).
```

These imply all original quality balances by the affine representation and
mass balance. Conversely, the independent basis vectors make the original
balances equivalent to these coordinate balances for represented pool
qualities. Every physical positive-flow pool quality is represented.

## 3. Partition the bypass graph and the flow variables

Choose deleted vertices `A subset I`, `B subset J`, with
`cI=|A|`, `cJ=|B|`, and `cI+cJ<=c`. Write `I_beta,J_beta` for the input
and output vertices of each remaining component; isolated vertices are
components. Each component has at most `h` vertices. No bypass connects
two different remaining components.

For fixed `c`, enumerating vertex subsets of size at most `c` and checking
component sizes finds such a decomposition in polynomial time whenever one
exists. Failure to find a decomposition is failure of this structural
condition, not an infeasibility certificate for the pooling instance.

Put the following variables in the core:

```
q_ells                for every pool and quality coordinate,
y_iell                for i in A,
v_ellj                for j in B,
z_ij                  for i in A, j in B,
T_j, M_js             for j in B, s=1,...,t.
```

The last variables will represent covered-output throughput and quality
coordinate masses. Their defining constraints are given in Section 5.
All existing covered-node flow arcs retain their individual finite bounds;
missing arcs can be omitted or fixed to zero.

For component `beta`, its local block contains

```
y_iell                for i in I_beta,
v_ellj                for j in J_beta,
z_ij                  for i in I_beta, j in J_beta,
z_ij                  for i in A, j in J_beta,
z_ij                  for i in I_beta, j in B.
```

Every arc flow is assigned exactly once. The local dimension is at most
`ph+ch+h^2`; in the vertex-cover case the sharper bound is `p+c`.

Impose all individual arc bounds within the owning block. Every noncover
input throughput constraint belongs to its component block, because all
its incident flows are there. The same holds for every noncover output
throughput constraint. For its upper quality bound `U_ja`, impose

```
sum_ell (C_0a + sum_s b_sa q_ells - U_ja) v_ellj
+ sum_i (C_ia-U_ja) z_ij <= 0.
```

The lower bound `L_ja` uses coefficients
`L_ja-C_0a-sum_s b_sa q_ells` and `L_ja-C_ia`. All appearing bypass
variables belong to the same component block. Given the core, the block
is a polyhedron with explicit finite rational flow boxes. The number of
quality inequalities may grow with `K`, which the fixed-core theorem permits.

## 4. Pool and covered-input aggregate constraints

Pool mass and quality-coordinate equations become

```
sum_beta [sum_{i in I_beta} y_iell - sum_{j in J_beta} v_ellj]
= sum_{j in B} v_ellj - sum_{i in A} y_iell,
```

```
sum_beta [sum_{i in I_beta} a_is y_iell
          - q_ells sum_{j in J_beta} v_ellj]
= q_ells sum_{j in B} v_ellj - sum_{i in A} a_is y_iell.
```

Their block coefficients are affine in the core; their right-hand sides
have degree at most two. There are `p(t+1)` equations.

Pool throughput bounds apply to

```
sum_{j in B} v_ellj + sum_beta sum_{j in J_beta} v_ellj.
```

For each covered input `i in A`, its throughput bounds apply to

```
sum_ell y_iell + sum_{j in B} z_ij
+ sum_beta sum_{j in J_beta} z_ij.
```

These contribute at most `2p+2cI` aggregate inequalities. No other input
or pool bounds remain unassigned.

## 5. Covered-output totals keep the aggregate dimension fixed

A covered output may have arbitrarily many quality specifications, so they
cannot simply be left as aggregate rows. Instead define its core totals by

```
sum_beta sum_{i in I_beta} z_ij
= T_j - sum_ell v_ellj - sum_{i in A} z_ij,
```

```
sum_beta sum_{i in I_beta} a_is z_ij
= M_js - sum_ell q_ells v_ellj - sum_{i in A} a_is z_ij.
```

There are `cJ(t+1)` equations. The right-hand sides have degree at most two
in the core. Covered-output throughput bounds now apply directly to `T_j`.
Its original upper and lower quality bounds become the core inequalities

```
(C_0a-U_ja) T_j + sum_s b_sa M_js <= 0,
(L_ja-C_0a) T_j - sum_s b_sa M_js <= 0.
```

The number of these inequalities can grow with `K`; the core dimension is
still fixed. Output specification vectors need not lie in a low-rank family.

For compactness, let `H_j` be the sum of finite upper bounds on all arcs
entering output `j`, and put `A_s=max_i |a_is|`. Valid explicit bounds are

```
0 <= T_j <= H_j,   -A_s H_j <= M_js <= A_s H_j.
```

Every input or pool coordinate lies in `[-A_s,A_s]`, so every physical
flow satisfies these bounds. Their bit lengths are polynomial. The core
domain is a compact set described by bounded-degree polynomial inequalities;
it need not be a box.

## 6. Exactness and complexity

A physical feasible flow maps directly into its uniquely assigned core and
block flow coordinates. Positive-flow pool coordinates are their averages;
zero-flow pool coordinates are arbitrary within the boxes. Set `T_j,M_js`
to the actual covered-output totals. Every displayed constraint holds and
the cost is unchanged.

Conversely, local constraints enforce all noncover input/output bounds and
all local arc bounds. Core arc bounds and Sections 4–5 enforce every
remaining input, pool, and output condition. Pool coordinate balances imply
perfect mixing in every positive-flow pool. Inactive pools transmit no flow.
The defining equations for `T_j,M_js` make the covered-output inequalities
exactly their original throughput and quality conditions. Thus the feasible
flow vectors and their costs agree in both models.

Each original linear arc cost belongs to its core or block objective.
The fixed-core theorem applies with parameters bounded by

```
r <= pt + pc + c^2 + cJ(t+1),
d <= max(1,ph+ch+h^2),
k <= p(t+1) + cJ(t+1) + 2p + 2cI,
D=2.
```

Here `k` counts the aggregate equations and inequalities. Replace each
aggregate inequality by an equation with a bounded scalar slack block.
Finite rational slack bounds follow by interval arithmetic from the known
core and flow boxes, with polynomial bit length. If no local blocks remain,
solve the fixed-dimensional core directly or append a scalar block fixed
to zero. Empty or inactive pools do not require division by their throughput.

The cited theorem solves this instance and recovers all blocks over a common
real-algebraic extension in polynomial bit time. Recovering every original
pool-quality attribute through the rational affine map is also polynomial.
This proves the theorem.

## 7. Corollaries and elementary cases

- Fixing the number of attributes `K` implies `t<=K`. Hence fixed pool
  count, quality count, and bypass vertex integrity are sufficient.
- A fixed number of distinct input-quality profiles also bounds their affine
  rank, even when the number of inputs and attributes is unbounded.
- A bypass vertex cover of size `c` gives `h=1`. This permits an unbounded
  number of bypass arcs incident to a fixed number of input or output hubs.
- Components of bounded size give `c=0`. An unbounded bypass matching is
  therefore allowed even though its vertex cover is unbounded.
- With a fixed number `m` of inputs, `t<=m-1` and all inputs form a
  bypass vertex cover. This recovers Corollary 3 of the fixed-core theorem:
  fixed input and pool counts allow arbitrary attributes and bypasses.
- With no bypasses, the result strengthens Corollary 4 of the fixed-core
  theorem by replacing fixed attribute count with fixed affine quality rank.
- If there are no pools, the model is a direct blending LP for any bypass
  graph, so neither structural nor quality-rank bounds are needed.
- If `t=0`, every input has the same quality vector. Fix every pool to that
  quality. The remaining model is an LP for any pool count or bypass graph.
  Zero-flow pools introduce no exception.

A fixed number of design binaries can be included in the core when their
constraints preserve the stated polynomial core/block form. This does not
extend to arbitrary local activation or assignment binaries.

## 8. Verification, sources, and novelty limits

Both independent reviewers checked the integrated theorem, including all
arc ownership and aggregate signs, exact quality compression, the compact
core totals, inactive pools, and the elementary LP cases. The
[independent symbolic checker](../code/pooling_bypass_copy/check_structure_mapping_review.py)
passed 375 exact ownership and residual checks across 15 configurations:
quality ranks zero, one, and two with four attributes; mixed, input-only,
output-only, empty, and complete deletion sets; and missing pool arcs.
These checks validate the reduction, not an implementation of the general
real-algebraic optimization algorithm.

The two component investigations are
[the fixed-quality structural mapping](../notes/pooling-bypass-vertex-cover-algorithm.md)
and [the affine-quality-rank extension](../notes/pooling-quality-rank-extension.md).
The general algorithm, exact algebraic output guarantee, and its two reviews
are in [the fixed-core block result](fixed-core-block-polyhedral-optimization.md).

Vertex integrity is established graph terminology; see
[Bentert, Heeger, and Koana](https://arxiv.org/abs/2403.01839)
(abstract inspected). The algorithm here finds a suitable deletion set by
elementary fixed-size enumeration and does not invoke their graph algorithms.

Targeted searches on 2026-09-05 combining pooling with vertex cover, vertex
integrity, bypass components, affine quality rank, and polynomial algorithms
found no matching structural theorem. This is limited search evidence,
not proof of priority. The earlier
[bypass-model literature audit](../notes/pooling-single-quality-bypass-novelty.md)
records the difference between unrestricted bypass claims and results under
flow-availability relaxations. Quality-coordinate compression itself is
ordinary linear algebra; the contribution claimed for investigation is the
resulting exact structural tractability theorem.

Arbitrary bypass graphs with positive quality rank remain outside this
result. Small graph degree or treewidth alone does not establish the bounded
vertex-integrity hypothesis. No extension to unbounded nonlinear local
blocks is claimed.
