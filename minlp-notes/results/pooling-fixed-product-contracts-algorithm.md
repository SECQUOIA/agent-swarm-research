# Exact pooling optimization from conserved product masses

Date: 2026-09-05. Status: two independent full proof audits PASS.
A targeted source comparison found no matching theorem; literature
priority remains provisional.

This result gives polynomial feasibility and standard economic
optimization with one pool, a fixed number of pool outlets, and
arbitrarily many pool feeds. Exact input supplies and exact specifications
for the products not receiving pool flow make the shared pool mass and
attribute balances affine functions of a fixed boundary. The number of
qualities and their affine rank need not be fixed.

## 1. Model and theorem

Use the standard three-layer pooling model with one pool, known rational
input-quality vectors `C_i in Q^K`, and allowed direct input-output bypass
arcs. There are no pool-to-pool arcs. Let `J_P` be all outputs with an
allowed pool-output arc, including arcs whose upper capacity happens to
be zero, and write `r=|J_P|`. The number `r` is fixed. The number of
allowed input-pool arcs is unrestricted.

Assume the following conditions:

- The bypass graph has maximum degree at most two.
- Each input has a prescribed exact rational total supply `a_i>=0`.
- Every output `j` outside `J_P` has prescribed exact demand `b_j>=0`
  and prescribed exact quality vector `B_j in Q^K`.
- Outputs in `J_P` may have arbitrary rational lower and upper demand
  bounds and lower and upper quality bounds.
- Finite rational upper bounds are supplied for every arc flow. Lower
  and upper pool-throughput bounds and individual arc bounds are allowed.

An exact quality vector on a zero-demand output is interpreted through
its homogeneous mass equations; it does not require positive flow.
The economic objective has rational unit production costs `c_i` at inputs
and unit revenues `R_j` at outputs. The same result permits linear costs
on the fixed set of pool-output arcs and on pool throughput. It does not
include unrestricted separate costs on all bypass or intake arcs.

**Theorem.** Under these assumptions, feasibility and the
maximum economic profit are computable in polynomial rational bit time.
A feasible or optimal original flow can be recovered exactly with a
polynomial-size real-algebraic representation. The exponent can depend
on the fixed outlet count `r`. Neither a practical runtime bound nor
strongly polynomial complexity is claimed.

If `r=0`, conservation forces all pool intakes to zero. Check pool and
incident-arc lower bounds for compatibility with zero and solve the
remaining bounded rational LP, keeping all external-node contracts.
Below suppose `r>=1`.

## 2. Exact local elimination of every intake

Write `z_ij` for bypass flow and `y_i` for intake from input `i` to the
pool. Exact input supply gives

```
y_i = a_i - sum_(j:ij is a bypass) z_ij =: Y_i(z).
```

For an allowed input-pool arc, impose its lower and upper bounds on
`Y_i(z)`, including nonnegativity. If no such arc is allowed, impose
`Y_i(z)=0`. These rows use at most two bypass variables, since the
bypass degree of an input is at most two. Thus eliminating unboundedly
many intake variables creates only scalar two-variable-per-inequality
rows with rational constant coefficients.

For each `j` outside `J_P`, the physical output constraints are

```
sum_i z_ij = b_j,
sum_i C_ik z_ij = b_j B_jk,       k=1,...,K.
```

They also use at most two bypass variables. Arc bounds are local rows.
No mixing parameter occurs in these internal relations.

## 3. Pool mass and quality mass are boundary functions

Let `H` be the bypass arcs entering outputs in `J_P`. There are at most
`2r` such arcs. Retain these bypass coordinates, and define

```
T(z_H) = sum_i a_i - sum_(j outside J_P) b_j - sum_(ij in H) z_ij,

Q_k(z_H) = sum_i C_ik a_i
            - sum_(j outside J_P) b_j B_jk
            - sum_(ij in H) C_ik z_ij.
```

These are affine functions of at most `2r` retained flow coordinates.
Their constants have polynomial rational bit length: they are sums of
polynomially many explicitly encoded rational products.

For every bypass assignment satisfying the internal rows in Section 2,

```
sum_i Y_i(z) = T(z_H),
sum_i C_ik Y_i(z) = Q_k(z_H).                         (1)
```

The first identity follows by summing the exact input supplies and
subtracting all bypass output throughputs. The throughputs at outputs
outside `J_P` sum to their prescribed demands. The second follows by
the same calculation for attribute mass, using their exact demand and
quality equations. All remaining bypass mass and attribute terms belong
to `H`. These are identities of original physical constraints, not new
independent aggregate restrictions.

In particular, nonnegative intake bounds imply `T>=0`. If `T=0`, each
`Y_i=0`, and (1) forces `Q_k=0` for every attribute. Thus the zero-flow
case does not hide an inconsistent or nonzero quality mass.

## 4. Fixed core and path projection

Retain the at most `2r` boundary bypass coordinates, all `r` pool-output
flows `v_j`, and `r` output fractions `theta_j`. The total core dimension
is at most `4r`. Require

```
theta_j>=0, sum_(j in J_P) theta_j=1,
sum_(j in J_P) v_j=T(z_H),
v_j=theta_j T(z_H),             j in J_P.
```

Keep all pool capacity rows, pool-output arc bounds, and receiving-output
demand bounds. Their throughputs are
`d_j=v_j+sum_(i:ij in H) z_ij`. Their attribute mass is

```
theta_j Q_k(z_H) + sum_(i:ij in H) C_ik z_ij.
```

Impose their prescribed lower and upper quality bounds by comparing this
expression with the corresponding bound times `d_j`. Every core row has
degree at most two. Arbitrary many attributes increase only the number
of rows, not the dimension or degree.

Remove only the receiving output nodes `J_P` from the bypass graph.
Every remaining component is a path, cycle, or isolated vertex. A
component touching the deleted set is a scalar path with at most two
retained boundary arc flows. Its input rows include the local intake
bounds from Section 2; its output rows are the exact product equations
there. Replace each such path by its exact polynomial-size endpoint
relation using the reviewed
[balanced polygon composition theorem](pooling-degree-two-boundary-projection.md).
One-boundary components give intervals; components with no retained
boundary are ordinary bounded rational LP feasibility problems. Such a
component may still contain inputs feeding the pool. Its aggregate intake
and attribute masses are fixed by its own exact source and product
contracts, so independent feasible LP recovery does not alter the global
identities (1). A cycle
cut at one receiving output can have two distinct boundary arcs incident
to that same output, which is already covered by the endpoint theorem.

The remaining core is a fixed-dimensional compact semialgebraic set,
with polynomially many rows, bounded degree, and polynomial coefficient
bit length. Established fixed-dimensional real-algebraic algorithms
therefore decide feasibility and sample an exact algebraic core point.
The retained composition trees lift it through rational affine endpoint
operations in the same represented algebraic field. Set every intake to
its expression `Y_i(z)` afterward.

For positive `T`, the actual pool quality is `q_k=Q_k/T` by (1).
Since `v_j=theta_j T`, its actual outgoing attribute mass is
`q_k v_j=theta_j Q_k`, exactly the quantity used in the core. At `T=0`,
all pool flows and quality masses vanish, as proved in Section 3, and
any fraction vector is harmless. Thus every core sample and lifted path
assignment yields an original physical feasible flow. The converse
follows from its actual output fractions when `T>0`, and any legal
fractions when `T=0`.

## 5. Standard economics becomes a core objective

The profit is

```
sum_j R_j d_j - sum_i c_i a_i
 = sum_(j outside J_P) R_j b_j - sum_i c_i a_i
   + sum_(j in J_P) R_j (v_j+sum_(i:ij in H) z_ij).
```

The first two sums are constant, and the remaining terms use only core
coordinates. Pool-throughput and pool-output costs also use those
coordinates. Hence exact global profit optimization is a fixed-dimensional
polynomial optimization problem over the compact core. Its optimum is
attained whenever the model is feasible. Algebraic optimization and the
same reconstruction produce a globally optimal original flow.

An arbitrary intake-arc cost would contribute
`sum_i d_i Y_i(z)`, which can become a dense bypass cost after elimination.
An arbitrary bypass-arc cost is already dense. These objectives are not
covered merely because the number of pools is fixed. A fixed number of
additional designated cost-bearing coordinates can be retained as in
the earlier endpoint theorem. For a designated intake, retain its at most
two incident bypass coordinates, so that intake is affine in the enlarged
fixed core. No unrestricted dense-cost conclusion is claimed.

## 6. Scope and source status

The algorithm removes the previous dense pool-aggregate obstruction by
using exact physical conservation and product contracts. It does not
solve the class with general supply ranges or nonreceiving product
quality intervals. It also does not assume a fixed number of source
qualities, a fixed affine quality rank, or a fixed number of pool feeds.

The polygon projection and algebraic steps are the established tools
and reviewed lemmas cited in the endpoint result. Related pooling work
must be compared by its exact flow assumptions: fixed demands alone do
not fix outgoing attribute mass when product quality is only bounded.
Baltean-Lugojan and Misener,
[*Piecewise parametric structure in the pooling problem*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6417401/),
Section 2, fix product demands while dropping feed-availability and pool
capacity constraints for their single-quality algorithms. Those are
different assumptions from the exact source contracts, arbitrary quality
count, finite individual arc bounds, and degree-two bypass structure
used here. Boland, Kalinowski and Rigterink,
[*A polynomially solvable case of the pooling problem*](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf),
study a model without direct input-output arcs; their fixed-input result
does not settle the unbounded-input bypass class here. This bounded
comparison did not find the present combined theorem, but does not
establish priority for it or for conservation-based elimination generally.

## 7. Independent verification

The [first full audit](../notes/review-pooling-fixed-product-contracts.md) and
[second full audit](../notes/review-pooling-fixed-product-contracts-second.md)
both pass. They checked local intake elimination, both conservation
identities, detached components that still feed the pool, zero throughput,
all directions of the core correspondence, exact algebraic recovery,
and the standard economic objective.

The [author checker](../code/pooling_bypass_paths/check_fixed_product_contracts.py)
passed 90 comparisons between original-flow LP fibers and the formulation
with substituted intakes and affine boundary masses. These are 180 LP
solves with fixed output fractions; 63 tested fibers were feasible.
The cases use one to three qualities, missing feed arcs, zero pool
capacity, and zero output fractions. Feasible optimal values agree.
The [log](../code/pooling_bypass_paths/fixed_product_contracts_output.txt)
is retained. These tests check the new conservation and objective
substitution; they retain path interiors and do not implement the
endpoint projection or the full algebraic optimization algorithm.

An explicit negative control tests the need for exact nonreceiving
quality. Inputs A and B have qualities zero and two and exact supplies
one. The only bypass is A to X, with X demand one and upper quality one.
The sole receiving output Y has demand one and upper quality `3/2`.
The true network is infeasible: X consumes all of A, so the pool receives
only B and sends quality two to Y. Incorrectly treating X's upper bound
one as its exact quality would compute pool attribute mass `2-1=1`
and falsely accept the instance. The checker detects precisely this
false feasibility when that invalid substitution is enabled.

