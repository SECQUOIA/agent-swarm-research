# Pooling triviality with recirculation and a singular-circulation caveat

Date: 2026-09-04. Status: independently checked extension and source correction;
no priority claim. This note extends the algebraic model in
[pooling-triviality-polynomial.md](../results/pooling-triviality-polynomial.md)
to arbitrary directed cycles among pools. The cyclic formulation machinery is
already studied by Boland–Kalinowski–Rigterink (2016); no new claim is made for
allowing cycles or using terminal commodities.

## Model semantics matter

Inputs have no incoming arcs and outputs have no outgoing arcs. All other vertices
are pools, which conserve mass and mix incoming streams linearly. Capacities are
nonnegative upper bounds, costs are arbitrary linear arc costs, and quality bounds
apply only to final outputs. All data are rational. Remove zero-capacity arcs and
nodes when discussing sign-only algorithms or conic hulls.

Unlike the DAG case, this algebraic model permits a positive pure circulation with
no source withdrawal or output delivery. A constant common quality on every pool
of a directed cycle satisfies its mixing equations. This is a legitimate solution
of the stated steady-state equations, regardless of whether a particular physical
application would require initialization, pumping costs, or source tracing. The
claims below apply to these equations. They do not silently impose a rule that
every circulating unit must originate at an input.

## Proposed sign criterion

The model admits a negative-cost feasible flow if and only if at least one of the
following holds on its positive-capacity support:

1. There is a directed cycle with negative total arc cost.
2. There is no such negative cycle, and for some output `j` the shortest-path
   blending LP from Theorem 2 of the DAG result has a negative optimum.

Shortest paths in the second case are ordinary finite shortest paths, computed
by a polynomial algorithm that permits negative arc costs. A shortest walk can
be replaced by a simple path because every directed cycle has nonnegative cost.
The blending LP uses all inputs that can reach the chosen output and the same
aggregate quality inequalities as before.

For sufficiency in case 1, send a small positive amount around the negative
cycle and assign a common quality to its pools. Scale to satisfy capacities.
For sufficiency in case 2, route the negative blending mixture on chosen shortest
paths and scale it to capacities. Their union may contain directed cycles even
though each path is simple. Repeatedly cancel the minimum flow on a positive-flow
directed cycle. This preserves all source withdrawals and output deliveries,
reduces arc flows, and does not increase cost because every cycle is nonnegative.
Each cancellation removes at least one positive arc and never creates one, so at
most `|A|` cancellations are needed. The remaining support is acyclic and still
has negative cost. Topological quality reconstruction now proves feasibility,
using precisely the same aggregate output quality as the selected mixture.

The cancellation step is important: the union of simple shortest paths need not
be acyclic. No claim that it is acyclic is needed.

## Destination decomposition with closed circulations

Fix any physical flow `y` and its pool qualities. Work on its positive-flow support.
At an active pool `v`, write `F_v` for its conserved positive throughput and route
forward from `v` to `w` with probability `y_vw/F_v`.

Any strongly connected class of pools that has no positive arc leaving it also
has no positive arc entering it. Indeed, summing the mass balances over the class
equates total entering flow to total leaving flow. Thus a closed class is an
isolated pure circulation in this positive-flow support. This does not mean it
is disconnected in the original graph, whose connecting arcs may carry zero flow.

Remove these isolated classes and their flows, denoting the removed flow by `y^0`.
Every remaining active pool has a positive-flow path to an output. The finite
forward routing chain is consequently transient before output absorption. For
each output `j`, its eventual absorption probabilities `h_j(v)` satisfy

```
F_v h_j(v) = Σ_w y_vw h_j(w),
h_j(j')=1[j=j'],           Σ_j h_j(v)=1.
```

Set `h_j=0` on the removed classes. Define

```
y^j_uv = y_uv h_j(v).
```

Exactly as in the DAG proof, the head multiplier scales every incoming flow at a
pool by one common number. The harmonic equation preserves total flow, and the
original pool qualities remain valid. Every component satisfies the original
upper capacities and serves at most output `j`. We obtain

```
y = y^0 + Σ_j y^j.
```

The removed flow is a nonnegative circulation. Such a circulation decomposes
into directed cycles. If there are no negative-cost cycles, its cost is
nonnegative. Therefore a negative-cost physical flow has a negative-cost
single-output component. Ordinary path-and-cycle decomposition of that component,
followed by deletion of its nonnegative-cost cycles, gives a negative-cost path
mixture with unchanged source withdrawals and hence unchanged aggregate output
quality after reconstruction. Intermediate pool qualities need not be preserved
by this cycle cancellation. Replacing paths
by cheapest paths only improves its cost, proving necessity in the sign criterion.

The absorption probabilities are used for an existence proof. The sign algorithm
does not need an optimal nonlinear flow or its probabilities: it uses negative-cycle
detection, shortest paths, and blending LPs directly.

## Exact single-output LP projection still holds

The preceding sign proof avoids recovering qualities on a cyclic support, but the
stronger projection statement also holds. Any ordinary balanced nonnegative flow
serving at most one output satisfies all mixing equations for some pool qualities.
Its output quality mass equals the total input quality mass. Consequently imposing
the aggregate quality inequalities gives an exact LP description of its arc-flow
projection, even in the presence of cycles.

Here is a direct proof of the existence claim. Remove zero-throughput pools and
process strongly connected components of the remaining pool support in a
topological order of the component graph. For a component `D`, the mixing equations
for one quality coordinate are

```
F_v p_v − Σ_{u∈D} y_uv p_u = b_v,       v∈D,
b_v = Σ_{u∉D} y_uv p_u.
```

All qualities in the right-hand side are known from inputs or earlier components.
After dividing row `v` by `F_v`, the within-component coefficients form a
nonnegative substochastic matrix. If some positive flow enters the component,
at least one row sum is strictly below one. Strong connectivity then implies
that its spectral radius is below one: the associated finite backward chain has
a positive-probability route out of the component from every state. Hence `I−Q`
has the inverse `Σ_{r≥0}Q^r`, and the system has a unique solution. This solution
is a weighted average of the incoming boundary qualities.

If no positive flow enters the component, aggregate conservation also forbids
any positive flow leaving it. It is an isolated circulation, and any constant
common pool quality solves its equations. After all components are handled,
summing the quality balances cancels internal quality mass and yields the claimed
input-output identity. For a zero-delivery flow, all source withdrawals are zero,
and its circulations are still allowed; unlike the DAG case, the flow need not
vanish.

For rational flow data, the nonsingular component systems have rational solutions
of polynomial encoding length by standard determinant bounds. Isolated classes
can be assigned quality zero. Thus exact quality reconstruction is polynomial.

When at least one output exists, the same `|J|` single-output LPs already detect
negative circulations as well as negative delivery flows: a pure circulation is
feasible for every such LP. If there are no outputs, the problem reduces to
minimum-cost circulation, and the negative-cycle criterion alone decides sign.

## Conic-hull consequence

Let `S` be the uncapacitated physical-flow set on the positive-capacity support,
let `C_0` be the ordinary nonnegative circulation cone, and let `C_j` be the
single-output polyhedral cone given by conservation and aggregate quality bounds.
Then

```
conv(S)=cone(S)=C_0 + Σ_j C_j.
```

The destination-plus-circulation decomposition proves one containment; exact
single-output LP projection and constant-quality realization of a circulation
prove the other. When outputs exist, every `C_j` already contains `C_0`, so the
extra summand is redundant. With no outputs, the right-hand side is just `C_0`.
This is a polynomial linear lift, and common positive scaling again gives the
same conic hull for the capacitated feasible set. As before, it is not an exact
description of the capacitated convex hull.

## A precise issue in a prior cyclic uniqueness lemma

The [Boland–Kalinowski–Rigterink manuscript dated June 11, 2015](https://optimization-online.org/wp-content/uploads/2015/06/4959.pdf)
already treats cyclic networks in Section 4.3. Its Lemma 1 on PDF p.12 claims
invertibility of both mixing matrices for every conserved capacity-feasible flow.
That assertion needs an exception for closed positive circulations.

Consider vertices `i,a,b,j`, with input `i`, pools `a,b`, output `j`, and arcs

```
i→a, a→b, b→a, b→j.
```

All capacities are one. Set `y_ab=y_ba=1` and `y_ia=y_bj=0`. This satisfies the
source's graph-degree assumptions and every flow balance. Even every vertex
lies on an input-output path in the original graph. The two pool qualities may
equal any common constant, so their values and the corresponding internal quality
mass are not uniquely determined by this flow.

In the source's forward matrix, with unknown arcs ordered `ab,ba,bj`, direct
substitution in its definition gives

```
F = [[ 1,−1,0],
     [−1, 1,0],
     [ 0, 0,1]].
```

This matrix is singular. The backward matrix likewise has a singular cycle
block. The proof step claiming that a positive arc necessarily enters the
maximizing level set fails when that set is an isolated circulation class.

This is a counterexample to the invertibility/uniqueness lemma as stated in that
2015 manuscript. The proof in the final 2016 journal article has not been inspected.
It is not a counterexample to the main projected-feasible-set
equivalence. The equivalence can be repaired by treating closed circulation
classes separately, as the argument above does. No claim is made here that an
erratum or later version has never addressed this issue. The exact published
version and any correction should be checked before a public criticism is made.

The source's cyclic formulation analysis is also a reason to classify the current
sign and conic-hull results as consequences and clarifications of existing
machinery rather than as a new cyclic formulation. The full independent review is
recorded in [review-pooling-recirculation.md](review-pooling-recirculation.md).

## Conditioning near a closed circulation

The singular example has a quantitative nearby version. On the same four arcs,
set flows `y_ia=ε`, `y_ab=1`, `y_ba=1−ε`, `y_bj=ε`, with `0<ε<1`.
Both pools have throughput one. If the input quality is `λ`, the pool-quality
system is

```
[[ 1, −(1−ε)],     [p_a]     [ελ]
 [−1,      1]]  ·  [p_b]  =  [ 0].
```

Its determinant is `ε`, and its exact solution is `p_a=p_b=λ`. Setting both
pool qualities to `λ+1` changes the first mixing-equation residual to `ε` and
leaves the second residual zero, despite a unit concentration error. Thus small
absolute tracking residuals alone need not imply accurate concentrations near a
closed circulation. This is an elementary conditioning observation, not a new
general theorem about numerical stability.
