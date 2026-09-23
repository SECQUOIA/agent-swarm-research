# Pooling with fixed affine quality rank and controlled bypass structure

Promoted after two independent audits into the combined
[result](../results/pooling-bypass-structure-algorithm.md). This file preserves
the investigation and earlier candidate language.

Date: 2026-09-05. Status: extension candidate awaiting independent review.
This extends the [bypass vertex-cover and bounded-component mapping](pooling-bypass-vertex-cover-algorithm.md).

## Candidate theorem

Fix the number of pools `p`, the affine dimension `t` of the input-quality
vectors, and the vertex integrity of the bypass graph. Standard pooling,
with the same rational capacities, lower bounds, linear costs, finite flow
bounds, and absence of pool-to-pool arcs as in the preceding mapping, is
exactly solvable in polynomial bit time. The numbers of inputs, outputs,
quality attributes, and bypass arcs are unrestricted.

Since `t<=K`, this includes the fixed-quality-count result. It also permits
arbitrarily many quality attributes when their input profiles lie in a fixed
affine-dimensional subspace. The rank condition concerns the input data;
output specification vectors may be arbitrary.

## 1. Rational quality coordinates

Assume there is at least one input. Let `C_i in Q^K` be its quality vector,
choose one input-quality vector as the reference `C_0`, and compute a rational basis
`b_1,...,b_t in Q^K` for the differences `C_i-C_0`. Gaussian elimination
returns rational coordinates `a_i in Q^t` with

```
C_i = C_0 + sum_{s=1}^t a_is b_s.
```

All intermediate and output bit lengths are polynomial. When `t=0`, every
input-quality vector equals `C_0`, and empty sums below have their usual
meaning. Instances with no inputs are processed as in the preceding note.

Represent pool quality by a core coordinate vector `q_ell in R^t`:

```
Q_ell = C_0 + sum_s q_ells b_s.
```

Bound `q_ells` between the smallest and largest `a_is`. Positive-throughput
pool coordinates are weighted averages of the `a_i`; inactive pools can be
assigned arbitrary boxed coordinates. Pool mass and quality-coordinate
balance equations are

```
sum_i y_iell = sum_j v_ellj,
sum_i a_is y_iell = q_ells sum_j v_ellj  (s=1,...,t).
```

These equations imply all original quality balances after multiplying by
the basis vectors and adding `C_0` times mass balance. Conversely, the basis
vectors are linearly independent, so the original quality balances and mass
balance imply these coordinate equations whenever qualities are represented
as above. Every physical positive-flow quality admits that representation.
Thus no original quality constraint is lost.

## 2. Noncover blocks

Use the same deletion sets `A subset I`, `B subset J`, of total size at most
`c`, and components of size at most `h`, as in the preceding mapping. Core
flow coordinates and all local flow assignments are unchanged. Replace the
`pK` pool-quality core variables by `pt` quality-coordinate variables.

For a noncover output `j`, each original attribute constraint still belongs
to its component block. Substitute

```
Q_ella = C_0a + sum_s b_sa q_ells
```

for its pool quality coefficient. Increasing `K` increases only the number
of local inequality rows; the block dimension remains at most
`ph+ch+h^2`. The fixed-core theorem explicitly permits an unbounded number
of inequalities per local block.

## 3. Covered outputs need additional core totals

It would be incorrect simply to replace `K` by `t` in the earlier aggregate
row count: a covered output can have `K` independent specification rows.
To avoid that issue, add core variables `T_j` and `M_js` for every `j in B`,
where `T_j` is total throughput and `M_js` is total quality-coordinate mass.
Impose the fixed number of defining aggregate equations

```
sum_beta sum_{i in I_beta} z_ij
= T_j - sum_ell v_ellj - sum_{i in A} z_ij,
```

```
sum_beta sum_{i in I_beta} a_is z_ij
= M_js - sum_ell q_ells v_ellj - sum_{i in A} a_is z_ij.
```

There are `|B|(t+1)` equations, with right-hand side degree at most two in
the core. All original covered-output constraints now belong to the core
formula. Throughput bounds apply directly to `T_j`. Upper and lower quality
bounds become, respectively,

```
(C_0a-U_ja) T_j + sum_s b_sa M_js <= 0,
(L_ja-C_0a) T_j - sum_s b_sa M_js <= 0.
```

These are linear core inequalities, even when there are arbitrarily many
attributes and arbitrary output bound vectors.

Finite rational bounds for the added variables are explicit. Let `H_j` be
the sum of finite upper bounds on all arcs entering output `j`, and let
`A_s=max_i |a_is|`. Put

```
0 <= T_j <= H_j,   -A_s H_j <= M_js <= A_s H_j.
```

Every feasible flow satisfies these bounds because every input or pool
quality coordinate lies in `[-A_s,A_s]`. Their bit lengths are polynomial.
The new core is therefore a compact set described by polynomial inequalities
of bounded degree; it need not be a box, which the fixed-core theorem allows.

## 4. Remaining aggregate rows and complexity

Pool mass and quality-coordinate balances require `p(t+1)` equations.
Pool throughput bounds contribute at most `2p` inequalities, and covered
input throughput bounds contribute at most `2|A|` inequalities. Covered
output throughput and quality constraints are now core constraints, not
additional aggregate rows. Including the defining output totals, the
aggregate row count after adding bounded scalar slack blocks is at most

```
k <= p(t+1) + |B|(t+1) + 2p + 2|A|.
```

The other parameters of the fixed-core theorem satisfy

```
r <= pt + pc + c^2 + |B|(t+1),
d <= max(1,ph+ch+h^2),
D=2.
```

All are fixed when `p,t,c,h` are fixed. The objective remains the original
linear arc cost. The new core totals are uniquely determined by the flows
and represented pool qualities, so adding them changes neither feasibility
nor attainable cost values. Applying the fixed-core theorem proves the
candidate complexity claim, subject to independent audit.

## Scope

This is a linear-algebraic compression of standard quality data, combined
with a fixed number of aggregate output mass variables. It does not assume
low rank of output specification vectors, approximate quality correlations,
or a numerical rank threshold. The rank and all transformations are exact
over rational input data.

Unrestricted bypass graphs and an unbounded number of pool-quality core
coordinates remain outside the theorem. Literature priority of this precise
rank-and-bypass classification has not yet been established.

A targeted search on 2026-09-05 combining `pooling problem`, `affine`,
`quality rank`, `low rank`, and polynomial algorithms found no matching
statement. Many rank-based pooling results concern rank-one constraints on
flow matrices, which is a different rank from the affine dimension of the
fixed input-quality data used here. This search observation is not a claim
that quality-coordinate compression itself is new.
