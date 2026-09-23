# Independent audit: pooling with recirculation

Date: 2026-09-04. Reviewer: independent `fbbt` agent. Scope: the cyclic extension developed in [the recirculation investigation](pooling-recirculation-investigation.md), and the closely related invertibility claim in an open source manuscript.

**Verdict:** the sign decision, single-output LP reduction, and conic-hull extension are valid for the algebraic lossless pooling model with directed pool cycles, nonnegative upper capacities, no positive lower flows, and no intermediate quality restrictions. Isolated positive circulations must be handled explicitly. A blanket claim that every active mixing matrix is invertible is false.

These statements concern the algebraic steady-state model. A circulation with no active source or output is feasible there and may have an arbitrary common quality. The audit does not silently impose an additional requirement that all circulated material originate from active external inputs.

## Separating isolated circulations

Fix any nonnegative conserved flow. Consider the directed support consisting only of positive-flow arcs and active pools. For every set `W` of pools, summing conservation gives

`flow entering W from outside = flow leaving W to outside`.

Therefore a strongly connected pool component with no positive outgoing arc to another component or an output has no positive incoming arc either. It is an isolated circulation component. This includes single-node components only when a self-loop is allowed and carries flow. Without self-loops an active singleton cannot be closed.

Remove these isolated components from the positive support. Every remaining active pool reaches an output along positive arcs: otherwise a terminal component reachable from it would be a closed component of the kind just removed. Likewise every remaining pool is reachable from an input. To see the latter, trace the component condensation graph backward; a source component without external input has zero external output by aggregate conservation and would be isolated.

This argument uses the **positive-flow support**, not merely graph-theoretic reachability in the original network. Inactive arcs into or out of a circulation do not make its mixing equations nonsingular.

## Forward destination fractions

On the remaining pools, use transition probabilities `y_vw/F_v` along outgoing arcs, with outputs absorbing. Every state has a positive-probability path to an output. Since there are finitely many states, there is a common finite step count and positive probability of absorption within that many steps from every state. Iterating this bound proves absorption with probability one.

Consequently the hitting probabilities `h_j(v)` satisfy the backward harmonic equations and `sum_j h_j(v)=1`. They can be computed by a nonsingular rational linear system; a topological recursion is no longer available.

The head-weighted component `y^j_uv=y_uv h_j(v)` obeys exactly the same conservation and unchanged-quality identities as in the acyclic proof. No step in those identities requires acyclicity once the harmonic fractions exist. Each designated output retains its original inflow, other outputs receive zero, and component flows are dominated by the original flow.

The isolated circulation part is also dominated by the original flow and preserves feasibility. Its original qualities can be retained because it has no positive external arcs. Alternatively, assign any common finite quality to every pool in each such component. Thus an arbitrary physical flow is the sum of feasible single-output components and a feasible isolated circulation component, with cost additivity.

## Exact single-output reconstruction

Take an ordinary conserved flow serving at most one output and satisfying the aggregate source-quality inequalities. Remove its isolated circulation components temporarily. On each remaining pool define the backward transition probability from `v` to predecessor `u` as `y_uv/F_v`; inputs are absorbing.

Every remaining pool has a positive path backward to an input, by the support argument above. This backward chain is transient. If `Q` is its pool-to-pool transition matrix and `b_k` the contribution from predecessor inputs of quality `k`, then

`p_k = Q p_k + b_k`, and `p_k=(I-Q)^(-1)b_k`.

The inverse exists because absorption is certain. These concentrations are convex combinations of input qualities and satisfy every pool mixing equation. On isolated circulation components assign a common arbitrary quality. Inactive pools can also receive arbitrary finite vectors. The full resulting concentration vector satisfies all tracking equations.

Summing tracking equations cancels every internal quality flow, including cycles, so the sole output's quality mass is `sum_i lambda_ik s_i`. The LP's aggregate inequalities therefore enforce its required quality. Signed quality numbers do not alter this cancellation. If output throughput is zero, the flow need not be zero; it can be a circulation. This is the essential correction to the corresponding acyclic proof paragraph.

Thus the single-output LP remains exact in the cyclic model, including its circulation flows. Its rational concentration reconstruction has polynomial bit complexity by ordinary rational linear-system bounds, with arbitrary fixed rational constants on closed classes.

## Sign algorithms and conic hull

If at least one output exists, any circulation is feasible in every single-output LP. The decomposition therefore implies that the same family of single-output LPs detects a negative physical objective: if the circulation part has negative cost, any one LP detects it; otherwise a negative total requires a negative single-output component. For no outputs, the problem reduces to minimum-cost circulation with upper capacities.

An alternative sign test first deletes zero-capacity arcs and nodes and checks for a negative directed cycle. Such a cycle is a feasible negative direction after small common scaling and constant-quality assignment. Conversely any negative-cost nonnegative circulation contains a negative cycle by ordinary cycle decomposition.

If no negative cycle exists, minimum input-output path costs are finite on reachable pairs and can be computed using algorithms that permit signed costs. Cycles in a source-output flow decomposition then have nonnegative cost, so the shortest-path blending lower bound remains valid. A negative blending mixture routed on shortest paths and scaled to capacities gives the converse. Thus the negative-cycle test followed by the blending LPs is sound. A DAG-only shortest-path routine must be replaced in this extension.

Let `Z` be the nonnegative conserved pool-circulation cone and let `C_j` be the uncapacitated single-output LP cone, allowing circulations. Then the convex conic hull of uncapacitated physical flows is

`Z + sum_j C_j`.

The inclusion from physical flows follows from the decomposition, and each cone on the right consists of physical flows, giving the reverse conic-hull inclusion. If `J` is nonempty, `Z` is already contained in every `C_j`, so it can be omitted. If `J` is empty, retain `Z`. Positive capacity magnitudes can again be accommodated by common scaling, proving the corresponding equality for the convex conic hull of the original capacitated set. This remains a conic-hull result, not a capacitated convex-hull formula.

## A defect in the open manuscript's invertibility claim

Boland, Kalinowski, and Rigterink's [June 11, 2015 open manuscript](https://optimization-online.org/wp-content/uploads/2015/06/4959.pdf), Section 4.3, extends formulation equivalence to networks with cycles. Lemma 1 states that its matrices `F(y)` and `B(y)` are invertible for every capacity-feasible conserved flow. Section 3 imposes graph-degree conditions but no active-flow reachability condition. The counterexample below disproves that invertibility statement in this checked manuscript. The final published version was not independently compared during this audit.

Use one input `i`, two pools `a,b`, and one output `j`. Include arcs `ia,ab,ba,bj`; every node and arc capacity is one. Set

`y_ia=y_bj=0`, and `y_ab=y_ba=1`.

The graph satisfies the stated degree assumptions. In fact every pool is graph-theoretically reachable from the input and can reach the output. The flow is nevertheless an isolated positive two-pool circulation, since those external connecting arcs are inactive.

Using the manuscript's displayed matrix definitions, order `F` by `(ab,ba,bj)` and `B` by `(ia,ab,ba)`. Then

```
F = [ 1 -1  0 ]       B = [ 1  0  0 ]
    [-1  1  0 ]           [ 0  1 -1 ]
    [ 0  0  1 ]           [ 0 -1  1 ].
```

Both determinants are zero. Their respective null vectors include `(1,1,0)` and `(0,1,1)`. Every common finite pool quality satisfies the physical tracking equations, demonstrating the associated nonuniqueness. The proof's asserted existence of a positive arc entering its extremal pool set fails for the closed component `{a,b}`.

This does **not** disprove equivalence of the feasible arc-flow projections. Those projections can remain equivalent after assigning closed-class commodity fractions and qualities appropriately. The narrow conclusion is that the stated universal invertibility and unique-extension argument needs the closed-class correction. Once isolated classes are removed, the transient-block argument above supplies the valid replacement.

## Exact check on a nontrivial recirculating flow

An independent rational calculation used two inputs with qualities 0 and 2, pools `u,v`, and outputs `j,k`. Send one unit from each input to its respective pool, two units on each of `uv` and `vu`, and one unit on each of `uj` and `vk`. Pool throughputs are three.

The mixing system gives `p_u=4/5`, `p_v=6/5`; destination-`j` probabilities are `h_j(u)=3/5`, `h_j(v)=2/5`. The component flows on the ordered arcs `(input0,u),(input2,v),uv,vu,uj,vk` are

`(3/5,2/5,4/5,6/5,1,0)`.

Exact arithmetic verifies conservation, preservation of both original pool qualities, and the output's aggregate quality. Exact symbolic calculation also verifies both singular matrices in the closed-cycle counterexample. These checks support the general proofs and distinguish transient recirculation from a source-free closed class.

## Final draft additions

The sign proof's cycle cancellation is valid when all cycle costs are nonnegative: subtracting the minimum arc flow on a positive cycle preserves source withdrawals and output deliveries, reduces capacities used, and cannot increase cost. Each cancellation removes a positive arc and creates none, so at most `|A|` cancellations leave an acyclic support. Intermediate qualities may change; the preserved source totals imply the same aggregate output quality after single-output reconstruction. The union of individually simple paths need not itself be acyclic, and the draft correctly includes cancellation rather than assuming otherwise.

The final conditioning example also checks exactly. With `y_ia=epsilon`, `y_ab=1`, `y_ba=1-epsilon`, `y_bj=epsilon`, pool throughputs are one and the mixing matrix is `[[1,-(1-epsilon)],[-1,1]]`. Its determinant is `epsilon`; both exact pool qualities equal the input quality `lambda`. Assigning both pools `lambda+1` instead gives residual `(epsilon,0)` while the concentration error is one. This is a valid elementary warning about absolute residuals near a closed circulation, without requiring a novelty claim.
