# Pooling with all four degree bounds two: candidate hardness

Date: 2026-09-05. Status: retained investigation record. The core proof is now
in [the result](../results/pooling-all-degrees-two.md) and has passed two
independent reviews. Its structural extension below passed the second review.

## Candidate theorem

The one-quality standard pooling problem is strongly NP-hard even when every
input has out-degree two, every pool has in-degree and out-degree two, every
output has in-degree at most two, all vertex capacities equal one, input
qualities and output upper bounds belong to `{0,1}`, and costs belong to
`{-2,-1,0,1}`. There are no direct or pool-to-pool arcs. Moreover, maximizing
the nonnegative profit (negative of the specified cost) on this restricted
family has no PTAS unless P=NP.

This strengthens the existing [degree-two pool result](../results/pooling-one-quality-degree-two-hardness.md)
by removing its remaining degree-three aggregation vertices. The essential
new point is to allow some pools to be inactive and prove that fractional
flows cannot improve profit. Requiring all pools to be active leads instead
to a Boolean feasibility problem that is too weak for this reduction.

## Source problem and primary reference

Maximum Independent Set is NP-hard and has a constant approximation gap on
simple cubic graphs supplied with a proper three-edge-coloring. A primary,
openly accessible proof is Chlebík and Chlebíková, *Complexity of approximating
bounded variants of optimization problems*, the [author manuscript](https://pure.port.ac.uk/ws/portalfiles/portal/1887750/3DM_JOURNAL_revision_old.pdf),
Section 5(A), especially printed pages 25–26. The construction there explicitly
produces an edge-three-colored three-regular graph `f(I)` with the same
independent-set objective and preserves the gap. The coloring is constructed,
not merely promised to exist. This is sufficient for the source used below;
we do not need a numerical approximation constant.

## Construction

Let `G=(V,E1 ∪ E2 ∪ E3)` be the source graph, `n=|V|`, with each `Ei` a
perfect matching. For each vertex `v`, make a pool `l_v` and a private lax
output `b_v`. For each `e∈E1`, make a clean input `a_e`. For each `e∈E3`,
make a dirty input `d_e`. For each `e∈E2`, make a strict output `s_e`.
All vertex capacities are one. Clean and dirty qualities are zero and one;
strict and lax bounds are zero and one. If `e_i(v)` is the unique edge of
`Ei` incident to `v`, use exactly these four arcs at pool `v`:

```
a_{e_1(v)} -> l_v        cost  1
d_{e_3(v)} -> l_v        cost  0
l_v -> s_{e_2(v)}        cost -2
l_v -> b_v              cost -1.
```

Every input feeds two pools, each pool has two inputs and two outputs, strict
outputs have two incoming arcs, and lax outputs have one. The construction
uses `n` pools, `n` inputs, and `3n/2` outputs.

## Lemma 1: removing unprofitable cross-routing

At pool `v`, write clean and dirty intakes as `a_v,d_v`, strict and lax
outflows as `s_v,b_v`, and throughput as `t_v=a_v+d_v=s_v+b_v≤1`.
The contribution to cost is

```
a_v - 2 s_v - b_v = -s_v - d_v.
```

Thus total profit is `P=Σ_v(s_v+d_v)≥0`. If `s_v>0`, the zero upper
quality bound of the shared strict output implies pool quality zero: every
positive-throughput pool has quality in `[0,1]`, so all terms of that output's
quality inequality are nonnegative and individually vanish. Hence `d_v=0`.

Given any feasible solution, perform these changes independently at all pools:

* If `s_v>0`, keep only `a_v'=s_v'=s_v`, set `d_v'=b_v'=0`, and set quality
  zero. The old clean intake was `a_v=s_v+b_v`, so no resource use increases.
* If `s_v=0`, keep only `d_v'=b_v'=d_v`, set `a_v'=s_v'=0`, and set quality
  one (or any bounded quality when `d_v=0`). The old lax outflow was
  `b_v=a_v+d_v`, so no resource use increases.

All capacities and mass balances hold, and output quality constraints hold
because strict outputs receive only quality zero and lax outputs allow one.
Profit is unchanged. Each pool now has at most one pure mode: clean input to
strict output, or dirty input to lax output. This statement applies to every
feasible point, not merely a purported optimal one.

## Lemma 2: integral replacement

Fix the choice of one allowed mode per pool made in Lemma 1 (an inactive pool
can be assigned either mode). Represent each chosen mode by an edge between
its input and its output. These edges form a bipartite graph with inputs on
one side and outputs on the other. Feasible pure throughputs are precisely
the fractional matchings in that graph: each vertex has incident total at
most one, and each edge throughput is at most one. The latter bound also
enforces the pool capacity; there is only one retained mode per pool.

The bipartite matching polytope is integral. Therefore a maximum-cardinality
matching has size at least the sum of the feasible fractional throughputs.
Route one unit through every corresponding pool and zero through all others.
This produces an integral feasible pooling point with at least the old profit.
It is computable in polynomial time, including from any rational feasible
pooling point. Consequently the optimum is attained with every active pool
using exactly one unit in one pure mode.

## Lemma 3: the exact objective identity

Form `H` from `G` by subdividing each edge in `E3` twice. For `uv∈E3`, the
replacement path is `u - d_u - d_v - v`. Vertices `v∈V` stand for clean
modes, and new vertices `d_v` stand for dirty modes.

Two clean modes conflict exactly along `E1` (shared clean input) or `E2`
(shared strict output). Two dirty modes conflict exactly on the middle edge
`d_u d_v` for `uv∈E3` (shared dirty input). The modes `v,d_v` conflict because
they belong to one pool. There are no other conflicts. Thus integral
pooling solutions correspond exactly to independent sets in `H`, preserving
profit.

We have `α(H)=|E3|+α(G)`. To prove the lower bound, take an independent set
`S` of `G`; on each subdivided edge choose one internal vertex nonadjacent
to any selected endpoint. At most one endpoint is in `S`, so this is always
possible. This gives `|S|+|E3|` vertices in `H`.

For the upper bound and algorithmic recovery, take any independent set `T`
of `H`. If both original endpoints `u,v` of an edge of `E3` are in `T`,
neither internal vertex is in `T`; delete `u` and add `d_u`. The new set is
independent, has the same size, and has fewer pairs of conflicting original
endpoints. Since `E3` is a matching, these operations do not interfere.
After all such changes, the selected original vertices form an independent
set `S` of `G`. At most one internal vertex was selected per subdivided edge,
so `|S|≥|T|-|E3|`. This proves the upper bound and gives polynomial recovery.

Combining the lemmas yields the exact identity

```
maximum pooling profit = n/2 + α(G).
```

The decision threshold for an independent set of size at least `k` is pooling
cost at most `-(n/2+k)`. All physical and cost data are bounded constants and
the threshold is linear in `n`, so this is strong NP-hardness. It does not
assert NP membership for general pooling; the explicitly constructed
subfamily has integral optimal certificates.

## Approximation transfer

From any feasible pooling solution of profit `P`, Lemmas 1–3 produce in
polynomial time an independent set of `G` of size at least `P-n/2`.
Since every degree-three graph has an independent set of size at least `n/4`
(the elementary greedy bound), `P*=n/2+α(G)≤3α(G)`. A profit guarantee
`P≥(1-ε)P*` therefore gives an independent set of size at least
`α(G)-εP*≥(1-3ε)α(G)`. A PTAS for the stated profit problem would yield a
PTAS for the source problem, contradicting its fixed approximation gap.
Approximation claims concern this nonnegative profit objective, not a ratio
applied directly to negative minimum costs.

## Investigation history and novelty limitations

The obvious extension of the earlier capacitated-orientation reduction has
a degree-two source graph and is polynomial. More generally, forcing every
binary two-mode pool active makes the pairwise incompatibilities a 2-SAT
feasibility problem. Optimization over *partially* active pools avoids this
obstruction, but requires the pure-mode and integral-replacement arguments.

An older unreviewed script already in `code/pooling_degree_two/max2sat_reduction.py`
explores a MAX-2-SAT construction with cycle/path variable gadgets and large
throughput rewards. No corresponding result file was present when this note
was written. The present reduction uses constant costs and capacities and
requires no variable-consistency gadget or large reward argument.

Open-literature searches on 2026-09-05 found Boland, Kalinowski, Rigterink
(2017), *A polynomially solvable case of the pooling problem*, still listing
the one-quality bounded-in-degree and bounded-out-degree questions in
[the primary paper](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf).
Searches for all-degree-two pooling did not locate a subsequent answer.
This search is evidence for novelty, not a proof that the result is unknown.
The restricted pool-degree pattern `(2,2)` by itself was already known hard
in [Haugland's MAGO 2014 proceedings](https://www.hpca.ual.es/~MAGO14/MAGO14-Proceedings.pdf);
the claim here is the simultaneous four degree bounds and unit capacities.

## Verification status

The proof has been sent to the root agent for independent review. A dedicated
small-instance [check](../code/pooling_all_degrees_two/check_reduction.py)
passed on 60 random properly three-edge-colored cubic graphs with 4–12
vertices. It compares brute-force independent-set values with global solves
of the original nonconvex P-formulation. On 35 instances with at most eight
vertices it also independently enumerates every pure-mode support and solves
the resulting graph matching problem with NetworkX. All agree exactly to
the solver tolerance; [output](../code/pooling_all_degrees_two/check_output.txt).

## General structural extension (second independent review PASS)

The pure-mode argument has a useful generalization. Allow arbitrary
nonnegative integer input, output, and pool capacities, arbitrary sharing
degrees, one clean and one dirty input per pool, and one strict and one lax
output per pool. Input qualities remain zero and one and output bounds zero
and one. For any nonnegative rational mode rewards `α_v,β_v`, choose costs

```
clean intake β_v, dirty intake 0,
strict outflow -(α_v+β_v), lax outflow -β_v.
```

Then pool cost is `-α_v s_v-β_v d_v`. Lemma 1 removes cross-routing while
preserving cost. After fixing a mode per pool, maximize weighted flow on
the input/output bipartite graph, with integer vertex capacities and each
edge bounded by its pool capacity. This is capacitated bipartite
`b`-matching and has an integral optimum. Thus an optimal pooling solution
exists with integer throughputs and pure pool qualities. The optimization
remains hard because choosing the modes is discrete; integrality of the
optimal flows does not make the full feasible set convex.

For unit capacities this is exactly maximum-weight rainbow matching on the
bipartite input/output graph: a pool contributes two edges of one color, and
one may select at most one edge of each color. The two mode edges are
vertex-disjoint because their endpoint quality types differ. This gives a
direct route to combinatorial algorithms for this particular pooling
subfamily. It does not assert that general pooling, or general costs, have
an integral optimum. Relevant adjacent literature includes Le and Pfender,
*Complexity Results for Rainbow Matchings*, which establishes hardness for
several sparse graph families; the present application additionally requires
the physical clean/dirty separation, established by our explicit reduction.

## Positive strict-quality tolerance

The robustness extension is now in [a separate note](pooling-positive-tolerance-extension.md)
and passed the second independent review.
