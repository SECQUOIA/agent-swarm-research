# One-quality pooling with degree-two pools is strongly NP-hard

Date: 2026-09-04. Status: proofs written by the root agent; Gurobi cross-check
passed; two independent reviews passed (Theorems 1–2); a third review passed
Lemma 2 and Theorem 3 with minor corrections (applied). Novelty is
qualified by the literature audit in
[the pooling degree-bound novelty note](../notes/pooling-degree-two-novelty.md).

## Summary

Haugland (2016) and Boland, Kalinowski, and Rigterink (2017) left open whether
the standard pooling problem with a single quality is polynomially solvable
when (a) all in-degrees of pools and outputs are at most two, or (b) all
out-degrees of inputs and pools are at most two. Both questions are answered
negatively here: each restricted class is strongly NP-hard, already with all
numerical data in `{-2,-1,0,1,2}`, two input quality values, two output
quality bounds, every pool having exactly two inputs and two outputs, and
the one layer that is not of degree one (outputs in the first class, inputs
in the second) of degree at most three (Theorem 3). Since
the problem is polynomially solvable when every pool has in-degree one or
out-degree one (row 14 of the Boland et al. table, attributed there to
Haugland's Proposition 3; see Remark 2 for the short argument), the
pool-degree pattern `(2,2)` is the smallest possible hard pattern.

The reduction is from capacitated graph orientation (a bipartite form of the
`{1,2}`-weighted minimum-maximum-outdegree problem of Asahiro, Jansson, Miyano,
Ono, and Zenmyo, 2011). Each edge becomes a pool with one "strict" and one
"lax" side; the two orientations of the edge correspond to running the pool on
clean input only or on dirty input only. Splitting the pool's flow between the
two sides forces the pool to be clean and is charged for the dirty-side flow,
so any fractional orientation loses profit. No quality lower bounds, no
direct input–output arcs, and no pool-to-pool arcs are used.

## Problem statement

We use the standard pooling problem (SPP) and P-formulation exactly as in
Boland, Kalinowski, and Rigterink (2017, Section 1). A directed graph
`G=(V,A)` has `V=I ∪ L ∪ J` (inputs, pools, outputs) and
`A ⊆ (I×L) ∪ (L×J)`. Data: arc costs `c_a` (possibly negative), vertex
capacities `C_v ≥ 0`, one quality with input values `λ_i` and output upper
bounds `μ_j`. Variables: flows `x_a` on input-to-pool arcs, `y_a` on
pool-to-output arcs, pool qualities `p_ℓ`. Constraints:

```
(1) sum_{a in A^in_ℓ} x_a = sum_{a in A^out_ℓ} y_a           for all pools ℓ,
(2) sum_{a in A^out_i} x_a <= C_i,   sum_{a in A^in_ℓ} x_a <= C_ℓ,
    sum_{a in A^in_j} y_a <= C_j,
(6) sum_{a in A^in_ℓ} λ_a x_a = p_ℓ sum_{a in A^in_ℓ} x_a    for all pools ℓ,
(7) sum_{a in A^in_j} p_a y_a <= μ_j sum_{a in A^in_j} y_a   for all outputs j,
```

with `λ_a = λ_i` for `a` leaving input `i` and `p_a = p_ℓ` for `a` leaving
pool `ℓ`, all flows nonnegative, objective `minimize sum_a c_a (x_a or y_a)`.
Arc capacities are not needed (set to the tail capacity). The decision
problem asks, for rational data and a rational threshold `K`, whether a
feasible point of cost at most `K` exists. `p_ℓ` is a free variable when pool
`ℓ` carries no flow, but such a pool has zero outflow by (1), so its `p_ℓ`
enters no other constraint and can be set to any value in `[min λ, max λ]`
without changing flows or cost. Restricting `p` to that box therefore loses
nothing, makes the feasible set compact, and shows the minimum is attained.
The decision reduction below does not use attainment: it shows every feasible
point has cost at least `K` and exhibits a cost-`K` point exactly when the
orientation exists.

Degrees refer to the arc set `A`: `|A^out_i|`, `|A^in_ℓ|`, `|A^out_ℓ|`,
`|A^in_j|`.

## Source problem: capacitated orientation

**Capacitated orientation (CO).** Input: a loopless multigraph `H=(V,E)`,
integer edge weights `w_e ≥ 1`, integer vertex capacities `T_v ≥ 0`. Question:
is there an orientation of `E` such that for every vertex `v`, the total
weight of edges oriented into `v` is at most `T_v`?

CO is in NP. It is strongly NP-hard: Asahiro, Jansson, Miyano, Ono, and Zenmyo
(J. Comb. Optim. 22 (2011) 78–96, Section 5) reduce At-most-3-SAT(2L) to
`{1,k}`-MMO and prove (Lemma 1) that the constructed simple graph `G_φ`, with
weights in `{1,k}`, has an orientation with maximum weighted outdegree at most
`k` if and only if `φ` is satisfiable; Theorem 6 states that `{1,k}`-MMO is
strongly NP-hard for every fixed `k ≥ 2`. Reversing every arc exchanges
outdegree and indegree, so with `k=2`: deciding whether a simple graph with
weights in `{1,2}` has an orientation with in-load at most `2` at every vertex
is NP-complete. This is CO with `T ≡ 2` and `w ∈ {1,2}`.

**Lemma 1 (bipartite subdivision).** Given a CO instance `(H,w,T)`, build
`H'` by replacing each edge `e={u,v}` by a path `u — m_e — v`, giving both new
edges weight `w_e` and setting `T_{m_e}=w_e`; keep `T_v` for original
vertices. Then `H'` is bipartite (original vertices versus subdivision
vertices), all numbers are unchanged, and `(H',w',T')` is a yes-instance if
and only if `(H,w,T)` is.

*Proof.* Suppose `H` has a feasible orientation. For `e` oriented into `v`,
orient `{u,m_e}` into `m_e` and `{m_e,v}` into `v`. Then `m_e` receives
exactly `w_e = T_{m_e}`, `v` receives what it received in `H`, and `u`
receives nothing from these two edges; all capacities hold. Conversely, take a
feasible orientation of `H'`. Both half-edges cannot point into `m_e`, since
`2w_e > w_e = T_{m_e}`. If `{u,m_e}` points into `m_e`, then `{m_e,v}` points
into `v`; orient `e` into `v`. Symmetrically, orient `e` into `u` if
`{m_e,v}` points into `m_e`. If neither half-edge points into `m_e`, both `u`
and `v` receive `w_e`; orient `e` into `u`. In all cases the in-load of every
original vertex in `H` is at most its in-load in `H'`, hence at most `T_v`. □

Consequently CO restricted to simple bipartite graphs with weights in `{1,2}`
and capacities in `{1,2}` is NP-complete. Parallel edges are also allowed in
the constructions below; they are not needed for hardness.

**Lemma 2 (bounded degree).** CO is NP-complete on simple graphs of maximum
degree three with weights in `{1,2}` and `T ≡ 2`. Combined with Lemma 1, CO
is NP-complete on simple bipartite graphs of maximum degree three with
weights and capacities in `{1,2}`, where every vertex of degree three lies in
one class.

*Proof.* We rerun the reduction of Asahiro et al. (Section 5) from
At-most-3-SAT(2L), in which each clause has at most three literals and each
literal occurs at most twice, with `k=2` and one change: the single special
cycle is replaced by vertex-disjoint triangles. At-most-3-SAT(2L) is
NP-complete: Tovey (1984, Theorem 2.1) proves NP-completeness of
satisfiability with two or three distinct variables per clause and at most
three occurrences per variable, and his construction (replace a variable
with `k ≥ 2` occurrences by `x_1, …, x_k` and add the cycle clauses
`x_i ∨ ¬x_{i+1}`) makes every literal occur at most twice. Asahiro et al.
attribute the same fact to problem [LO1] of Garey and Johnson (1979); that
text was not checked by this project. For each variable `v_i`
create vertices `v_i`, `¬v_i` joined by an edge of weight `2`. For each
clause `c_j` create a vertex `c_j` joined by weight-`1` edges to the vertices
of its literals; if `c_j` has fewer than three literals, create a fresh
triangle of weight-`2` edges and join `c_j` by weight-`1` edges to
`3 - |c_j|` distinct vertices of that triangle, so that every clause vertex
has degree exactly three. Clauses are sets of literals, as in Tovey (1984)
and Garey and Johnson (1979), so no literal vertex is joined twice to the
same clause vertex (a clause containing both `x` and `¬x` is allowed and
produces the simple triangle `c_j – x – ¬x`). The graph is therefore simple,
and its maximum degree is three: a literal vertex has its variable edge and at most two clause edges,
a clause vertex has degree three, and a triangle vertex has two triangle
edges and at most one clause edge. The load of a vertex is the total weight
oriented into it; the target is load at most `2` everywhere.

Suppose the formula is satisfiable. Orient each variable edge into the false
literal vertex (load `2` there, `0` at the true vertex). Orient every
triangle cyclically (load `2` at each triangle vertex). For each clause
`c_j` pick one true literal `ℓ` in it, orient the edge `{c_j, ℓ}` into `ℓ`,
and orient the other two edges of `c_j` into `c_j`. Then `c_j` has load `2`;
a true literal vertex receives at most one unit per clause in which it is the
chosen literal, hence at most `2` because each literal occurs at most twice;
a false literal vertex receives only its variable edge, load `2`; a triangle
vertex receives only its cyclic triangle edge, load `2`. All loads are at
most `2`.

Conversely, take an orientation with all loads at most `2`. In each triangle
the three weight-`2` edges enter three distinct vertices (two entering the
same vertex would give load `4`), so every triangle vertex has load exactly
`2` and every clause edge at a triangle vertex is oriented into the clause
vertex. Each variable edge enters one endpoint; call that endpoint false and
the other true. A false literal vertex has load `2` from its variable edge,
so all its clause edges are oriented into the clause vertices. A clause
vertex has degree three and load at most `2`, so at least one of its unit
edges is oriented out of it; by the above, that edge enters a true literal
vertex. Setting each variable according to which of its two literal vertices
is true (exactly one is) therefore satisfies every clause. □

Lemma 1 applied to this graph keeps the degrees of the original vertices and
adds subdivision vertices of degree two; the original vertices form one
class of the bipartition. The
[brute-force check](../code/pooling_degree_two/check_degree_three_gadget.py)
confirms Lemma 2 on 405 small formulas (158 unsatisfiable).

## Theorem 1 (bounded out-degrees, answering open problem 3)

**Theorem 1.** The one-quality standard pooling problem is strongly NP-hard,
already when every input has out-degree one, every pool has in-degree two and
out-degree two, every cost lies in `{-2,-1,0,1}`, every capacity lies in
`{1,2}`, input qualities lie in `{0,1}`, and output bounds lie in `{0,1}`.
Outputs may have arbitrary in-degree.

**Construction.** Given a bipartite CO instance `(U ∪ W, E, w, T)`:

- Inputs: for each edge `e`, a clean input `a_e` with `λ=0` and a dirty input
  `b_e` with `λ=1`, both of capacity `w_e`.
- Pools: for each edge `e`, a pool `ℓ_e` of capacity `w_e`.
- Outputs: every vertex `v` is an output with `C_v=T_v`; `μ_u=0` for `u ∈ U`
  and `μ_w=1` for `w ∈ W`.
- Arcs, for `e={u,w}`: `(a_e,ℓ_e)` at cost `1`, `(b_e,ℓ_e)` at cost `0`,
  `(ℓ_e,u)` at cost `-2`, `(ℓ_e,w)` at cost `-1`.
- Threshold `K=-sum_e w_e`.

Inputs have out-degree one, pools have in-degree two and out-degree two, and
output `v` has in-degree `deg_H(v)`.

**Claim.** The minimum cost is at least `K`, with equality if and only if the
CO instance has a feasible orientation.

*Proof.* Fix a feasible point. For edge `e={u,w}` write `x_a, x_b` for the
intakes of `ℓ_e`, `t=x_a+x_b ≤ w_e` for its throughput, and `y_u, y_w` for its
outflows, so `y_u+y_w=t` by (1). The cost attributable to `e` is

```
cost_e = x_a - 2 y_u - y_w = x_a - y_u - t.
```

We show `x_a ≥ y_u`. If `y_u=0` this is trivial. If `y_u>0`, then `t>0`, and
constraint (7) at output `u` reads `sum_{e'} p_{ℓ_{e'}} y_{e'u} ≤ 0`. Every
pool quality with positive throughput satisfies `p ∈ [0,1]` by (6), and a pool
with zero throughput has zero outflow, so all terms are nonnegative and the
term of `e` must vanish: `p_{ℓ_e} y_u = 0`, hence `p_{ℓ_e}=0`. By (6),
`x_b = p_{ℓ_e} t = 0`, so `x_a = t ≥ y_u`.

Therefore `cost_e ≥ -t ≥ -w_e` and the total cost is at least `K`. Equality
forces, for every `e`, `t=w_e` and `x_a=y_u`. If `y_u>0`, the argument above
gives `x_b=0`, so `y_u=x_a=t=w_e` and `y_w=0`: the pool runs on clean input
only and sends all `w_e` units to `u`. If `y_u=0`, then `x_a=0`, so
`x_b=t=w_e=y_w`: the pool runs on dirty input only and sends all `w_e` units
to `w`. Orient `e` into `u` in the first case and into `w` in the second. The
in-load of any vertex `v` equals its total inflow, which is at most
`C_v=T_v` by (2). So a cost-`K` point yields a feasible orientation.

Conversely, given a feasible orientation, route for each `e` oriented into `u`
the flow `a_e → ℓ_e → u` of value `w_e` (pool quality `0`, cost
`w_e - 2w_e = -w_e`), and for each `e` oriented into `w` the flow
`b_e → ℓ_e → w` of value `w_e` (pool quality `1`, cost `0 - w_e = -w_e`).
Constraint (7) holds at `u ∈ U` because every pool sending to `u` has
quality `0`, and at `w ∈ W` because `μ_w=1` bounds every quality. Vertex
capacities hold because inflows equal orientation in-loads. The cost is `K`. □

Since CO with weights and capacities in `{1,2}` on simple bipartite graphs is
NP-complete (Asahiro et al. Theorem 6 with Lemma 1 above), and the pooling
instance has size polynomial in `|V|+|E|` with all numbers bounded by `2`,
Theorem 1 follows.

## Theorem 2 (bounded in-degrees, answering open problem 2)

**Theorem 2.** The one-quality standard pooling problem is strongly NP-hard,
already when every output has in-degree one, every pool has in-degree two and
out-degree two, and all data are as in Theorem 1. Inputs may have arbitrary
out-degree.

**Construction.** Given a bipartite CO instance `(U ∪ W, E, w, T)`:

- Inputs: every vertex `v` is an input with `C_v=T_v`; `λ_u=0` for `u ∈ U`
  and `λ_w=1` for `w ∈ W`.
- Pools: for each edge `e`, a pool `ℓ_e` of capacity `w_e`.
- Outputs: for each edge `e`, a strict output `A_e` with `μ=0` and a lax
  output `B_e` with `μ=1`, both of capacity `w_e`.
- Arcs, for `e={u,w}`: `(u,ℓ_e)` at cost `1`, `(w,ℓ_e)` at cost `0`,
  `(ℓ_e,A_e)` at cost `-2`, `(ℓ_e,B_e)` at cost `-1`.
- Threshold `K=-sum_e w_e`.

Outputs have in-degree one, pools have in-degree two and out-degree two, and
input `v` has out-degree `deg_H(v)`.

*Proof.* For edge `e={u,w}` let `x_u, x_w` be the intakes of `ℓ_e`,
`t=x_u+x_w ≤ w_e`, and `y_A, y_B` its outflows with `y_A+y_B=t`. Then
`cost_e = x_u - 2y_A - y_B = x_u - y_A - t`. If `y_A>0`, then `t>0`,
constraint (7) at `A_e` reads `p_{ℓ_e} y_A ≤ 0`, and `p_{ℓ_e}=x_w/t ≥ 0` by
(6), so `p_{ℓ_e}=0`, hence `x_w=0` and
`x_u=t ≥ y_A`; if `y_A=0` then `x_u ≥ y_A` trivially. So `cost_e ≥ -w_e`,
total cost at least `K`, and equality forces `t=w_e` and `x_u=y_A` for every
`e`: either `y_A>0`, giving `x_u=w_e` and `x_w=0`, or `y_A=0`, giving `x_u=0`
and `x_w=w_e`. Orient `e` into `u` in the first case and into `w` in the
second. The in-load of vertex `v` equals the total outflow of input `v`,
which is at most `C_v=T_v` by (2). Conversely a feasible orientation gives the
flows `u → ℓ_e → A_e` (quality `0`, cost `-w_e`) or `w → ℓ_e → B_e` (quality
`1`, cost `-w_e`), which satisfy (2), (6), (7) and cost exactly `K`. □

## Theorem 3 (bounded degrees on both layers)

**Theorem 3.** The one-quality standard pooling problem is strongly NP-hard
when every input has out-degree one, every pool has in-degree two and
out-degree two, and every output has in-degree at most three; and,
separately, when every output has in-degree one, every pool has in-degree
two and out-degree two, and every input has out-degree at most three. All
data are as in Theorem 1.

*Proof.* Apply the constructions of Theorems 1 and 2 to the bipartite CO
instances of Lemma 2 (after Lemma 1). The degree of output `v` in Theorem 1
(input `v` in Theorem 2) is `deg_H(v) ≤ 3`. □

The case in which all four bounds (input out-degree, pool in-degree, pool
out-degree, output in-degree) are simultaneously at most two is settled by
the subsequent [all-degree-two result](pooling-all-degrees-two.md). That
independently reviewed result proves strong NP-hardness even when all four
degree counts are exactly two and all vertex capacities equal one.

## Corollaries and remarks

1. **Two outputs or two inputs.** Taking `H` to be a multigraph on two
   vertices `u ∈ U`, `w ∈ W` with parallel edges of weights `s_1,…,s_n` and
   `T_u=T_w=B` encodes PARTITION. Theorem 1 then gives NP-hardness with
   `|J|=2`, one quality, input out-degree one, and pool degrees `(2,2)`;
   Theorem 2 gives NP-hardness with `|I|=2`, one quality, output in-degree
   one, and pool degrees `(2,2)`. These are weak hardness statements
   (Haugland and Hendrix (2016) give a pseudo-polynomial algorithm for
   `|I|=|J|=2`, `|K|=1`). Row 9 of the Boland et al. table already gives
   strong NP-hardness for `|J|=2` with one quality, and row 11 adds pool
   degrees at most six; the degree structure of those reductions, and of the
   bin-packing reduction of row 10 (`|I|=|J|=2`), was not available to this
   project, so the only content of this corollary that we can claim as new is
   the private-input (resp. private-output) structure. We do not know whether
   `|J|=2` with input out-degree at most two, or `|I|=2` with output
   in-degree at most two, is strongly NP-hard; the present construction needs
   many vertices on both sides.
2. **Tightness in pool degrees.** If every pool has in-degree one or
   out-degree one, the problem is polynomially solvable (Boland et al. row
   14, attributed to Haugland's Proposition 3, whose text was not checked).
   The argument is short: a pool with in-degree one has the fixed quality of
   its input, and a pool with out-degree one can be merged into its unique
   output, whose constraint (7) then becomes linear in the pool's intakes;
   after these substitutions (6) and (7) are linear, so the problem is an LP.
   So Theorems 1 and 2 identify the pool-degree pattern `(2,2)` as the exact
   threshold for one quality.
3. **Fixed pool out-degree.** Dey and Gupte (2015) list among their open
   problems "the complexity status for a fixed value of the out-degree of the
   pool nodes". Theorem 1 shows strong NP-hardness at pool out-degree two
   even with one quality and private inputs. Haugland's Theorem 6 already
   covered out-degree two with an unbounded number of qualities.
4. **All four degree bounds two.** The constructions above require
   degree-three aggregating vertices (outputs in Theorem 1, inputs in
   Theorem 2). A different, independently reviewed reduction now proves
   strong NP-hardness with all four degree counts exactly two and all
   capacities one; see [the all-degree-two result](pooling-all-degrees-two.md).
5. **No numerical subtlety.** The reduction is exact at the threshold `K`;
   in the constructions above every cost-`K` point is integral, and the
   argument uses only the sign structure of the data. The pool capacities can
   be dropped, leaving only `C_{a_e}=C_{b_e}=w_e` (Theorem 1) or
   `C_{A_e}=C_{B_e}=w_e` (Theorem 2), at the price of a different bound: the
   throughput can then reach `2w_e`, but in Theorem 1 `y_u>0` still forces
   `x_b=0` and hence `t=x_a ≤ w_e`, while `y_u=0` gives `cost_e=-x_b ≥ -w_e`;
   in Theorem 2 `y_A>0` forces `x_w=0` and `cost_e=-y_A ≥ -w_e`, while
   `y_A=0` gives `t=y_B ≤ w_e` and `cost_e=-x_w ≥ -w_e`. Equality still
   forces the orientation pattern, though cost-`K` points are then not
   unique (in Theorem 1 an edge oriented into `w` may carry any
   `x_a ∈ [0,w_e]` alongside `x_b=w_e`; in Theorem 2 an edge oriented into
   `u` may carry any `y_B ∈ [0,w_e]` alongside `y_A=w_e`).

## Sources

- N. Boland, T. Kalinowski, F. Rigterink, A polynomially solvable case of the
  pooling problem, J. Global Optim. 67 (2017) 621–630; arXiv:1508.03181.
  Section 4 lists the open problems; Table 2 summarizes Haugland's results.
- D. Haugland, The computational complexity of the pooling problem, J. Global
  Optim. 64 (2016) 199–215. Theorem numbering is taken from Boland et al.'s
  table and Haugland's INOC 2019 cross-references; the full text was not
  available to this project.
- D. Haugland, E. M. T. Hendrix, Pooling problems with polynomial-time
  algorithms, J. Optim. Theory Appl. 170 (2016) 591–615 (pseudo-polynomial
  algorithm for two inputs, two outputs, one quality; abstract verified).
- Y. Asahiro, J. Jansson, E. Miyano, H. Ono, K. Zenmyo, Approximation
  algorithms for the graph orientation minimizing the maximum weighted
  outdegree, J. Comb. Optim. 22 (2011) 78–96. Lemma 1 and Theorem 6 were read
  in the author PDF (`https://www.df.lth.se/~jj/Publications/mmoutdegr10_JOCO_2011.pdf`).
- C. A. Tovey, A simplified NP-complete satisfiability problem, Discrete
  Appl. Math. 8 (1984) 85–89. Theorem 2.1 and the construction preceding it
  were read by the third reviewer in the author PDF
  (`https://cedric.cnam.fr/~bentzc/INITREC/Files/CB11.pdf`).
- S. S. Dey, A. Gupte, Analysis of MILP techniques for the pooling problem,
  Oper. Res. 63 (2015) 412–427 (open problem on fixed pool out-degree; the
  local copy is a slide-format exposition, item 2 of its open-problem list).

## Verification

- [Gurobi cross-check](../code/pooling_degree_two/verify_reduction.py): for
  random CO instances (bipartite multigraphs, and non-bipartite graphs passed
  through Lemma 1, weights in `{1,2,3}`, capacities in `{0,…,4}`), both
  pooling instances were solved to global optimality with `NonConvex=2` and
  the optimum compared with `K`; brute force over all orientations decided
  feasibility. Lemma 1 was checked directly on every non-bipartite instance.
  Seeds 0 (60 trials) and 1 (40 trials) passed with no discrepancy; the full
  logs are in `verify_output.txt` next to the script.
- [Referee review](../notes/review-pooling-degree-two-hardness.md): PASS WITH
  CORRECTIONS (all applied above; none affected the theorems). The referee's
  own exhaustive check over bipartite multigraphs with `|U|,|W| ≤ 2`, at most
  three edges, weights in `{1,2}`, capacities in `{0,…,3}` (250 instances),
  with pool capacities present and dropped and with `p` free, found no
  discrepancy, and a deliberately broken variant was caught.
- [Second independent review](../notes/review-pooling-degree-two-independent.md):
  PASS. The reviewer wrote independent proofs before reading the author's,
  re-verified the Asahiro et al. source in the author PDF, and ran an
  exhaustive checker (Gurobi and an independent exact disjunctive-LP solve,
  18,656 bipartite instances under both constructions and 7,264 subdivision
  instances, no failures, smallest no-instance gap `1.0`; log in
  `independent_check_output.txt`). The
  reviewer suggested the degree-three refinement now proved as Lemma 2 and
  Theorem 3; the root agent wrote that proof and its brute-force check after
  the review.
- [Third review (Lemma 2 and Theorem 3)](../notes/review-pooling-degree-three-refinement.md):
  PASS WITH CORRECTIONS (clause-as-set convention made explicit; Tovey
  cited for At-most-3-SAT(2L)). The referee's exhaustive check over all
  formulas with at most three variables, at most four clauses, and each
  literal at most twice (42,140 formulas, 3,121 unsatisfiable, tautological
  clauses included) confirmed Lemma 2 and the Lemma 1 subdivision on top of
  it.
