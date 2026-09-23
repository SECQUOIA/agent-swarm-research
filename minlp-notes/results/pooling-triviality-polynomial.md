# Polynomial detection of profitable flow in acyclic generalized pooling

Date: 2026-09-04. Status: independently checked explicit consequences of known
pooling formulation machinery. The standard-pooling consequence is already implicit
in Dey–Gupte (2015), and the generalized-network destination disaggregation below
is already present in Boland–Kalinowski–Rigterink (2016). This note supplies a
self-contained affirmative answer to the stated triviality question and records
its sign and conic-hull consequences. No priority is claimed for the disaggregation;
the consequences were not located explicitly in the targeted literature search.

## Model and question

Let `G=(I∪L∪J,A)` be a finite directed acyclic graph. Inputs `I` have no incoming
arcs, outputs `J` have no outgoing arcs, and all remaining vertices are pools `L`.
Input `i` has a vector of `K` given qualities `λ_i`. All flows are nonnegative,
each pool conserves total flow, and every outgoing arc from a pool carries that
pool's perfectly mixed incoming quality. Outputs have prescribed lower and upper
bounds on each quality of their aggregate inflow. Arc costs are arbitrary and
linear. Arcs and nodes have finite nonnegative upper capacities. There are no
positive lower flow requirements, intermediate quality restrictions, fixed
charges, losses, or nonlinear mixing rules. All data are rational.

Write `P` for the feasible set of arc-flow vectors and

```
z* = min{cᵀy : y∈P} ≤ 0.
```

These are the assumptions in Section 2 of Gupte, Ahmed, Dey, and Cheon,
*Relaxations and discretizations for the pooling problem*. Remark 2.2 asks whether
testing `z*=0` is polynomial-time solvable. The source is
[[gupte2017-relaxations-and-discretizations-for-the]] p.4-6, specifically PDF p.6,
printed p.5, and the [open manuscript](https://www.pure.ed.ac.uk/ws/files/136877755/4883.pdf).

## Theorem 1: a polynomial family of linear programs

For each output `j`, form the following LP, denoted `LP_j`. Keep the original arc
and node capacities and pool flow balances. Force every arc into an output other
than `j` to zero. Define

```
s_i = Σ_{v:(i,v)∈A} y_iv,       t_j = Σ_{u:(u,j)∈A} y_uj.
```

Replace all quality-tracking equations with the linear inequalities

```
µ_jk^min t_j ≤ Σ_i λ_ik s_i ≤ µ_jk^max t_j       (k=1,…,K),
```

and minimize `cᵀy`. Let its optimal value be `z_j≤0`. Then

```
z*=0  ⇔  z_j=0 for every j∈J.
```

Thus pooling triviality is decidable using at most `|J|` rational linear programs
of polynomial size. If one LP has a negative objective value, it supplies a
profitable feasible pooling flow, with pool qualities recovered by a topological
pass. No fixed bound on the numbers of inputs, pools, outputs, or qualities is
required.

### Lemma 1: splitting a physical flow by its final output

Take any feasible physical flow `y` and its pool qualities `p`. For each output
`j`, define numbers `h_j(v)` in reverse topological order. At outputs set
`h_j(j')=1[j'=j]`. At a pool with positive throughput
`F_v=Σ_w y_vw=Σ_u y_uv`, set

```
h_j(v) = (Σ_w y_vw h_j(w))/F_v.
```

At a zero-throughput pool set every `h_j(v)=0`. A positive-flow arc cannot enter
such a pool. These numbers lie in `[0,1]`. Every positive-throughput pool has a
positive-flow path terminating at an output: flow conservation and acyclicity
exclude termination at a pool or infinite continuation. Reverse induction gives
`Σ_j h_j(v)=1` at each positive-throughput pool, and the same equality holds at
outputs by definition.

For each arc `u→v`, define

```
y^j_uv = y_uv h_j(v).
```

The probability is evaluated at the **head** of the arc. At a pool `v`, all
incoming flows are multiplied by the same number `h_j(v)`. Their total is
`h_j(v)F_v`; the total outgoing flow is also `h_j(v)F_v` by the defining recursion.
Thus the component conserves flow.

Keep the original pool qualities `p`. Its incoming quality mass for coordinate
`k` is

```
Σ_u p_uk y^j_uv = h_j(v)Σ_u p_uk y_uv
                 = p_vk h_j(v)F_v,
```

where `p_uk=λ_uk` at input vertices. This is exactly the quality-tracking equality
for the new throughput. Zero-throughput cases give the identity `0=0`.
Only output `j` receives flow; its incoming arc flows are identical to those
in the original solution, so its quality constraints hold. Other outputs receive
zero flow. Because `0≤y^j≤y` coordinatewise, all upper capacities remain valid.
Therefore every `y^j` is feasible for the original pooling model.

Finally,

```
y = Σ_{j∈J} y^j,       cᵀy = Σ_{j∈J} cᵀy^j.
```

Every positive-flow arc has a head where the probabilities sum to one; zero-flow
arcs contribute zero. If `cᵀy<0`, at least one component has negative cost.

### Lemma 2: a single output removes the nonlinear obstruction

For a flow serving only `j`, sum all pool quality balances. Internal quality flows
cancel, leaving the sink quality mass equal to `Σ_i λ_ik s_i`. Thus every physical
single-output flow is feasible for `LP_j`.

Conversely, take a feasible `LP_j` flow. Process pools in topological order. At a
positive-throughput pool, assign its quality to the incoming weighted average of
input or previously computed pool qualities. At a zero-throughput pool, assign
any finite quality vector. This enforces every tracking equation. Summing them
shows that output `j` receives total quality mass `Σ_i λ_ik s_i`, so its required
quality bounds follow from the LP. If `t_j=0`, conservation and acyclicity imply
that every arc flow is zero, and all multiplied quality bounds are satisfied.
Hence `LP_j` is exactly the projection of the single-output pooling problem onto
its arc flows.

Together, the lemmas prove Theorem 1. Direct input-output arcs are included in
both arguments. Signed quality numbers cause no change in the cancellation or
weighted-average arguments. Exact sign testing uses rational LP algorithms;
floating-point tolerances alone do not certify `z_j=0`.

## Quantitative consequence

Let `m=|J|≥1`, and let `z_best=min_j z_j`. Decomposing an optimal flow yields

```
z* ≤ z_best ≤ z*/m ≤ 0.
```

After changing sign to profit maximization, selecting the best single-output LP
is an `m`-approximation. This is a generalized-network extension of the familiar
standard-pooling one-output approximation principle, not a new principle for
standard pooling. If `J` is empty, acyclicity and conservation force the zero
flow and triviality is immediate.

The same argument yields an approximation guarantee relative to a single LP
relaxation. Introduce separate nonnegative flows `y^j` satisfying the single-output
balances and quality inequalities, and impose the original upper capacities on
their sum `y=Σ_j y^j`. Let `z_rel` be its minimum cost. Every physical flow has such
a decomposition, so it is a relaxation. Each component individually satisfies the
upper capacities and is physical by Lemma 2. Consequently

```
z_rel ≤ z* ≤ z_best ≤ z_rel/m ≤ 0.
```

This LP therefore has the exact zero-optimality status and gives an
output-count approximation by selecting its cheapest component. The construction
extends the standard-pooling one-output relaxation argument to acyclic generalized
networks using established terminal-commodity variables.

## Theorem 2: shortest paths and small blending LPs suffice for the sign

Delete every arc of zero capacity and every node of zero capacity, together with
its incident arcs. On the remaining graph, every retained upper capacity is
strictly positive. For each input `i` that can reach output `j`, let `δ_ij` be the
minimum total arc cost of an `i→j` path. Negative arc costs cause no difficulty in
a DAG. Let `I_j` be the set of such inputs. Solve

```
β_j = min Σ_{i∈I_j} δ_ij γ_i
      s.t. γ≥0, Σ_i γ_i=1,
           µ_jk^min ≤ Σ_i λ_ik γ_i ≤ µ_jk^max     (k=1,…,K).
```

Set `β_j=+∞` if this LP is infeasible, including when `I_j` is empty. Then

```
z*<0  ⇔  β_j<0 for at least one output j.
```

To prove the forward implication, first use Lemma 1 to obtain a negative-cost
single-output flow. Decompose its conserved ordinary flow into input-output
paths and let `t>0` be its total output. Put `γ_i=s_i/t`. Its actual cost per
unit output is at least `Σ_i δ_ij γ_i`, while aggregate quality conservation
makes `γ` feasible for the blending LP. Therefore `β_j<0`.

Conversely, choose a feasible negative-cost mixture `γ` and one shortest path for
each input in its support. Sending `γ_i` units on each chosen path gives a
single-output conserved flow whose total cost is negative. By Lemma 2 it admits
physical mixing with the required output quality. Because all retained capacities
are positive, multiply this entire flow by a sufficiently small positive scalar
to satisfy every node and arc upper capacity. Quality ratios and cost sign do not
change. This proves the converse.

Thus positive capacities affect the sign only through which arcs and nodes remain
usable; their positive numerical magnitudes affect the achievable profit but not
whether any profit is possible. Computing all required DAG shortest paths and
solving the `|J|` blending LPs is polynomial in rational input size.

An optimal blending LP solution can be chosen with at most `K+1` positive entries.
Indeed, at a vertex with support size `s`, normalization supplies one independent
equality and active quality bounds supply at most `K` additional independent
equalities. If `s>K+1`, a nonzero supported direction preserves all these equalities,
and sufficiently small perturbations in either direction preserve inactive
inequalities and nonnegativity, contradicting extremality. Therefore a profitable
instance has a witness obtained from at most `K+1` shortest input-output paths,
followed by common scaling. This does not bound the number of pools along a path.

All witness data can have polynomial bit length: shortest paths have at most
`|N|−1` arcs, an LP vertex is rational with polynomial encoding length, and the
scaling factor can be chosen as the minimum of finitely many positive capacity
to throughput ratios. Pool qualities can then be recovered rationally in
topological order. A common denominator for the flow and a product of the
positive integer pool throughputs bound the additional denominator bit length
polynomially, since no DAG path revisits a pool.

## Theorem 3: exact polyhedral conic hull

Continue on the graph after deleting zero-capacity arcs and nodes. Let `S` be the
set of physical pooling arc flows after removing all remaining upper capacities.
It includes zero and is closed under nonnegative scaling, but generally need not
be convex. Let `C_j` be the polyhedral cone defined by `LP_j` after removing its
upper capacities and objective. Lemma 2 says that `C_j` is exactly the
single-output physical flow set. Then

```
conv(S) = cone(S) = Σ_{j∈J} C_j
                   = {y : y=Σ_j y^j, y^j∈C_j for every j}.
```

Here `cone(S)` denotes the set of finite nonnegative linear combinations of
points in `S`, and the displayed sum is a Minkowski sum. The destination
decomposition proves `S⊆Σ_j C_j`. Conversely, every `C_j` is contained in `S`,
so their sum lies in `cone(S)`. Since `S` is closed under nonnegative scaling
and contains zero, `conv(S)=cone(S)`. This proves every equality and supplies
a polynomial-size linear extended formulation with `O(|J||A|)` flow variables.
The resulting cone is polyhedral and hence closed.

For the original capacitated feasible flow set `P` on this graph,

```
cone(P)=conv(S).
```

Indeed, `P⊆S`, and each finite flow in `S` can be scaled into `P` because all
remaining capacities are strictly positive. Consequently every homogeneous
linear inequality valid for the original pooling flows is captured by this
polyhedral cone. The criterion `z*=0` is equivalently membership of `c` in the
dual cone `{c:cᵀy≥0 for every y∈conv(S)}`.

This is a conic-hull statement, not a capacitated convex-hull description.
Intersecting the displayed cone with the upper-capacity box need not recover
`conv(P)`: convexification and imposing positive upper capacities do not in
general commute.

For a concrete strict example, take two inputs with qualities zero and one, one
pool, and two outputs requiring qualities exactly zero and exactly one. Include
only input-to-pool and pool-to-output arcs. Give every input, arc, and output
capacity one, and the pool capacity two. A physical flow serves at most one output,
so total output is at most one throughout `conv(P)`. The sum of the two pure
single-output flows lies in the uncapacitated conic hull and satisfies all these
capacities, yet sends one unit to each output. Its total output is two.

## Prior art and status

Dey and Gupte, *Analysis of MILP Techniques for the Pooling Problem*, Operations
Research 63 (2015), 412–427, already prove an output-count approximation by
one-output rounding. Their [open article manuscript](https://optimization-online.org/wp-content/uploads/2013/04/3849.pdf)
Section 1.1 explicitly restricts pool outflow to outputs, excluding pool-to-pool
arcs. Section 4, Theorem 2, gives the approximation, and Section 6 notes the
single-output polynomial case. Therefore the standard-pooling triviality test
is already a consequence of their theorem.

Boland, Kalinowski, and Rigterink, *New multi-commodity flow formulations for the
pooling problem*, Journal of Global Optimization 66 (2016), 669–710, already
introduce destination fractions on arbitrary generalized networks. Their
[open manuscript](https://optimization-online.org/wp-content/uploads/2015/06/4959.pdf),
Section 4.2.1, PDF p.8-9, defines the same head-indexed terminal fractions and
disaggregated flows. Equations (18), (19), (20), and (21) give commodity conservation,
aggregate output quality, bilinear consistency, and summation. Hence neither
destination-based disaggregation nor its aggregate quality equations are new.
Their relevant formulation and conclusion sections were checked; no explicit
zero-optimality or uncapacitated conic-hull theorem was found there.

The right interpretation is an explicit consequence of established formulation
machinery that answers Remark 2.2 under its stated assumptions. The shortest-path
sign criterion and sparse profitable witness make the consequence especially
transparent. A novelty claim stronger than that requires further evidence.
Independent reviews are in [the main audit](../notes/review-pooling-triviality.md)
and [a second audit](../notes/review-pooling-triviality-second.md); the first also
checks Theorems 2–3. The decomposition does not provide the exact capacitated
convex hull or exact optimization of the generally NP-hard objective.
