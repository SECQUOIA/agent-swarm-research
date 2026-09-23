# Fully contracted one-pool feasibility with arbitrarily many attachments

Date: 2026-09-05. Status: this quasipolynomial proof passed two full
independent audits. It is now superseded, for this physical class, by
the stronger [polynomial incidence-flow proof](pooling-quality-scaled-path-flow.md).
The present derivation and its scope counterexamples are retained as
useful development notes. No priority claim is made.

Exact flow and quality contracts at every product remove the dense pool
balance equations. This gives a quasipolynomial feasibility algorithm
with one pool, one scalar quality, a degree-two bypass graph, and
arbitrarily many pool feeds and outlets. Nontrivial common pool-capacity
bounds are excluded. The result combines the reviewed one-parameter
path projection with the conservation idea behind the
[fixed-outlet product-contract algorithm](pooling-fixed-product-contracts-algorithm.md).

## 1. Model and candidate theorem

Use a standard three-layer pooling network with one pool and no
pool-to-pool arcs. Input `i` has known rational scalar quality `C_i`
and exact total supply `a_i>=0`. Output `j` has exact total demand
`b_j>=0` and exact scalar quality `B_j`, interpreted by its homogeneous
quality-mass equation. Every arc has finite rational lower and upper
flow bounds, including nonnegativity. The bypass graph has degree at
most two. There is no bound on the number of input-pool or pool-output
arcs.

The common pool throughput bounds are redundant: its lower bound is
zero and its upper bound is at least `sum_i a_i`. Equivalently, no
additional common throughput restriction is imposed. Individual pool
arc bounds remain unrestricted rational input data.

**Candidate theorem.** Feasibility can be decided in
`N^(O(log(N+1)))` rational bit time, where `N` is the full input encoding
length. When feasible, an original feasible flow can be recovered with
polynomial algebraic degree and polynomial encoding length. This is an
upper bound; no matching lower bound or polynomial-time classification
is claimed.

If the pool has no allowed input or no allowed outlet, conservation
forces every pool arc to zero. Reject incompatible positive lower bounds
on those arcs, remove them, retain all external contracts, and solve the
remaining bounded rational LP. Below assume both kinds of pool arc exist.

## 2. Necessary global constants

Every feasible network must satisfy

```
sum_i a_i = sum_j b_j,
sum_i C_i*a_i = sum_j B_j*b_j.                         (1)
```

Check these rational equalities first. They express conservation of
total flow and the conserved scalar attribute over the entire network.
A quality specification at zero demand contributes zero to the second
identity and requires no positive flow.

Let `q` denote the pool concentration. It is enough to consider the
compact rational interval

```
min_(allowed pool feeds i) C_i <= q <= max_(allowed pool feeds i) C_i.
```

At positive pool throughput this follows from convex mixing. At zero
throughput, assigning any value in this nonempty interval has no effect
on physical mass or quality flow. Thus this restriction discards no
feasible original flow.

## 3. Eliminate every pool arc locally

Let `z_ij` denote a bypass flow. Input conservation determines

```
Y_i(z) = a_i-sum_(bypass ij) z_ij.
```

For an allowed feed arc impose its lower and upper bounds on `Y_i`.
If no feed arc is allowed, impose `Y_i=0`. Similarly define at each
output

```
V_j(z) = b_j-sum_(bypass ij) z_ij.
```

Impose the allowed pool-outlet bounds on `V_j`, or `V_j=0` if that
outlet is absent. Each of these rows involves at most two bypass flows.
All original bypass bounds remain.

At an output with a pool outlet, exact quality requires

```
q*V_j(z)+sum_i C_i*z_ij = B_j*b_j,
```

or equivalently

```
sum_i (C_i-q)*z_ij = b_j*(B_j-q).                    (2)
```

At an output without a pool outlet, use its ordinary exact bypass
quality equation. Using (2) there too would give the same constraint
because the separately imposed `V_j=0` removes the `q` term.

Thus, at fixed `q`, every node contributes linear inequalities or
equalities in at most two neighboring bypass arc variables. Their
coefficients are polynomials of degree at most one in the single common
parameter `q`. Coordinate bounds are uniformly finite and rational.
No dense aggregate row has been introduced in this local system.

## 4. Global pool balances follow automatically

For any assignment satisfying these local rows and (1),

```
sum_i Y_i(z) = sum_i a_i-sum_all_bypass z_ij,
sum_j V_j(z) = sum_j b_j-sum_all_bypass z_ij.
```

The first equality in (1) therefore gives pool flow conservation.
Summing all local exact output-quality equations gives

```
q*sum_j V_j(z) + sum_all_bypass C_i*z_ij = sum_j B_j*b_j.
```

Using the second equality in (1),

```
q*sum_j V_j(z)
 = sum_i C_i*a_i-sum_all_bypass C_i*z_ij
 = sum_i C_i*Y_i(z).                                  (3)
```

Equations (1)--(3) prove both actual pool balances. If their common
throughput is positive, (3) identifies `q` with the weighted average of
the actual nonnegative feeds. If it is zero, all nonnegative feed and
outlet flows vanish; every physical quality mass is zero and `q` is
irrelevant. Individual arc bounds hold by construction. The redundant
common pool bounds are automatic.

Conversely, every original feasible flow supplies its own bypass flows
and pool concentration, or any allowed concentration when inactive,
and satisfies every local row. Hence the local one-parameter formulation
is exactly equivalent to the physical network under the stated scope.

## 5. Compose components and intersect their feasible parameter sets

The bypass components are paths, cycles, and isolated nodes. A path
becomes a scalar path relation in its arc variables. Endpoint univariate
rows can be attached to the adjacent relation or encoded with a dummy
coordinate fixed to zero. Apply the independently reviewed
[one-parameter path theorem](one-parameter-path-projection-investigation.md)
to obtain a quasipolynomial parameter partition and polynomially many
endpoint rows on each cell.

For a cycle, choose one bypass arc variable `t` and open the cyclic
sequence at that variable. This produces an ordinary path with two
endpoint occurrences of the same coordinate. Its endpoint relation
`R_q(x,z)` gives cycle feasibility precisely when `R_q(t,t)` is nonempty.
Append `x=z` and its opposite inequality before testing the projected
bounded planar relation. This operation adds only constantly many rows.

On every endpoint-description cell, a further split at the coefficient
and augmented-minor roots makes nonemptiness constant. There are only
polynomially many additional roots per cell, of polynomial degree and
coefficient height. This also handles cycles after the diagonal equation
is added. Each component therefore has a quasipolynomial description of
its feasible `q` set as a union of intervals and isolated algebraic points.

Isolated nodes have no bypass variable. Their eliminated feed or outlet
is fixed by the corresponding contract. Check its arc bounds; a positive
fixed outlet can impose the scalar equation `q=B_j`. These elementary
parameter conditions fit the same representation.

All components share only the parameter `q`. In one dimension their
partitions are overlaid by taking the union of their breakpoints, not
by enumerating a product of independent cells. Their feasible sets can
therefore be intersected within quasipolynomial bit complexity. Test a
rational sample of each surviving open interval and every surviving
isolated point. Nonemptiness of this intersection is exactly physical
feasibility by Section 4.

## 6. Exact witness and excluded objectives

Every candidate boundary parameter has polynomial algebraic degree and
coefficient height; rational interval samples have polynomial bit length.
After selecting one common feasible `q`, choose feasible component
endpoints and lift their paths, using the same represented field
`Q(q)`. All local rows originally have degree at most one in `q`.
Original-component vertex solutions are therefore Cramer ratios of
polynomial-degree, polynomial-height integer polynomials evaluated at
this one parameter. Balanced symbolic rational-function reconstruction
gives the constructive encoding bound already proved in the path theorem.
No compositum of different component parameter fields is needed: every
component uses the same selected `q`.

Set the physical feed and outlet flows to `Y_i(z)` and `V_j(z)`.
Section 4 verifies the original pool. A polynomial-size witness results.

With exact supplies and demands everywhere, standard input-production
costs and output revenues give the constant profit
`sum_j R_j*b_j-sum_i c_i*a_i`. This candidate is a feasibility algorithm.
Unrestricted costs on individual bypass, feed, or outlet arcs are not
covered by its projection argument. Neither is a nonconstant common
pool-processing cost.

## 7. Why the common pool-capacity exclusion is necessary for this proof

Consider input qualities zero and two, each with exact supply one.
Both feed the pool. The clean input also bypasses to product `A`, with
exact demand one and quality `1/2`; the dirty input also bypasses to
product `B`, with exact demand one and quality `3/2`. Both products
receive pool flow. Every individual arc has upper capacity one.
The global constants (1) hold.

For a feasible concentration `q`, the local rows force

```
Y_clean=V_A=1/(2q),
Y_dirty=V_B=1/(2(2-q)),
1/2 <= q <= 3/2.
```

Their common pool throughput is

```
T=1/(2q)+1/(2(2-q))=1/(q(2-q)) >= 1.
```

The local formulation is feasible, for example at `q=1`. A common pool
upper capacity `3/4` makes the physical network infeasible. Thus a
nontrivial pool-capacity bound is not implied by the global constants
and local rows. It reintroduces a dense sum of eliminated feeds or
outlets and requires a separate argument. This example is a scope
counterexample, not a complexity lower bound.

## 8. Source and novelty status

This is a synthesis of exact global conservation and the reviewed
quasipolynomial parameterized path projection. It does not follow merely
from having one pool or one quality. Every product's exact quality mass
is used, and the common pool-capacity assumption is explicit.
No separate primary-source priority search for this precise contracted
class has yet been completed. Mathematical verification and novelty
assessment must remain distinct.

## 9. Independent original-network checks

The independently written
[check_all_product_contracts.py](../code/pooling_bypass_paths/check_all_product_contracts.py)
builds two different fixed-concentration LP formulations. The original
formulation retains every actual pool feed and outlet and both explicit
pool balances. The reduced formulation contains only bypass variables,
local node rows, and the preliminary global-constant checks.

Across 24 rationally generated networks it passed 235 fixed-quality
comparisons, including 78 feasible fibers. Instances include full bypass
cycles, paths obtained by deleting cycle arcs, isolated nodes, missing
pool arcs, and varying pool attachment counts. These are numerical LP
comparisons of exactly generated rational data, not certified numerical
global optimization or an implementation of symbolic parameter projection.

Three separate controls confirm essential hypotheses. Omitting global
mass conservation admits a one-input/one-output instance with unequal
exact throughputs. Omitting global quality conservation admits equal
throughputs with incompatible source and product quality. Adding the
restrictive pool capacity from Section 7 invalidates a locally feasible
instance. The checker detects all three differences. The mathematical
proof, rather than these finite comparisons, establishes the algorithmic
complexity and full parameter-domain equivalence.
