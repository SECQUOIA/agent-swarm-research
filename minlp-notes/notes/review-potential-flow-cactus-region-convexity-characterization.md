# Independent review: universal convexity of resistance-attainable regions

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS for the stated quadratic-law, connected simple-graph scope. This is a mathematical review, not an independent priority claim.

Reviewed [the candidate](potential-flow-cactus-region-convexity-characterization.md), the [weighted-flow obstruction](../results/potential-flow-weighted-arc-cactus-characterization.md), and the [weighted-potential obstruction](../results/potential-flow-weighted-potential-tree-characterization.md). The inherited obstruction estimates were already independently reviewed; this review checks their exact hypotheses and the new geometric deduction.

## Deletion and strict parametrization

The varying edge belongs to a selected cycle in each imported witness. Deleting it leaves a connected graph, including after the restoration of other edges. For distinct prescribed edge flows q1 and q2, the remaining nomination vectors differ by `-(q2-q1)(e_u-e_v)`. The remaining physical flow vectors therefore differ. Strict monotonicity of the quadratic laws makes their monotonicity inner product strictly positive. Conservation and the potential-drop equations give exactly

    (g(x2)-g(x1)) dot (x2-x1) = -(q2-q1)(P(q2)-P(q1)).

Thus the displayed negative sign is correct, and P is strictly decreasing. Existence, uniqueness, and continuity for these remaining-network states follow from coercive strictly convex energy on the nonempty affine conservation space. They hold for all real q; no operating bounds restrict these states.

The full equation `P(q)=beta*q*abs(q)` has a strictly decreasing left-minus-right function. Its root has the sign of P(0). If P(0)=0, the root is always zero, and uniqueness of the normalized remaining-network state makes the entire state constant. Otherwise the root varies strictly with beta: it decreases for positive flow and increases for negative flow. Continuity gives an interval parametrized bijectively by the varying resistance. Fixed or singleton parameter intervals present no exception to the positive results.

## Convexity arguments

The flow curve has exactly one vector at each value of its own-edge flow coordinate. If convex, it contains its endpoint chord. The chord covers the whole own-edge interval and has one vector above each coordinate; uniqueness then identifies the entire curve with that chord. This proves the endpoint-extremum implication used in the noncactus converse.

For normalized potentials, the relevant linear coordinate is the drop P(q), not the edge flow q itself. P is strictly decreasing, so it also parametrizes the curve injectively. Given q, the connected remaining network has one potential vector after fixing any reference vertex. The same chord argument therefore applies. Changing the reference causes no difficulty: it is a linear isomorphism between the two normalized potential spaces.

The imported strict interior advantages exclude the constant-state case and contradict the corresponding chord conclusions. Their uncertain edges remain cyclic, their other resistances are fixed, and their nominations are fixed and balanced, exactly as required here. The nonconvex potential projection proves nonconvexity of the joint region. On trees, conservation fixes flow and resistance enters every potential drop linearly, so both positive tree assertions are immediate.

The cactus positive direction uses the already established independent circulation intervals. The broader positive observation for continuously parametrized passive laws additionally relies on independent block parameters and continuous state dependence, as explicitly stated. No negative classification beyond the quadratic case is imported.

## Scope

The statements quantify over all nominations and boxes; they do not assert nonconvexity for every nomination on a graph containing the relevant obstruction. Zero nominations, fixed resistances, and some special parameter choices can produce singleton or convex regions. Normalization and absence of operating constraints are necessary parts of the stated setting. The simple-graph assumption is retained: the tree converse must not be applied without proof to a two-vertex parallel-edge graph.

No defect was found. The candidate is suitable for promotion after its separate source audit and second review.

## Additional robust version

The negative directions do not require degenerate boxes. Let S be one of the compact nonconvex one-parameter state images. There are a,b in S and t in (0,1) for which y=(1-t)a+tb is outside S. Compactness gives `dist(y,S)>0`. Thicken every fixed resistance interval by sufficiently small positive rational widths, staying in the positive orthant and containing the old box. The old states a,b remain attainable. Uniform continuity of the physical state on a common compact positive parameter neighborhood implies that the thickened image lies arbitrarily close to S. Hence y remains unattainable, and the new image is nonconvex. Every coordinate interval can thus have positive width in both universal characterizations.

The same reasoning proves local persistence under small balanced nomination perturbations: use the endpoint states at the perturbed nomination, whose chord point converges to y, and uniform convergence of all state images. One may choose rational generic nominations in that neighborhood. These are existence statements; no polynomial bound on the required thickening or perturbation precision is established by this compactness argument.
