# Graph classes for convex resistance-attainable flow and potential regions

Date: 2026-09-05. Status: verified by two independent full mathematical audits. The geometric deduction uses previously reviewed quadratic obstructions; source priority remains qualified.

## Characterizations

For a finite connected simple graph G, the following are equivalent under the common quadratic passive law:

1. G is a cactus.
2. For every fixed balanced nomination and every positive resistance box, the set of attainable physical flow vectors is convex.

Boxes may have fixed coordinates. Every noncactus witness can have only one resistance varying over an interval, all other resistances fixed, and the four small nominations used in the reviewed weighted-flow obstruction. No operating constraints filter scenarios.

## Positive direction

The [cactus flow-region construction](../notes/potential-flow-cactus-flow-region-and-optimization.md) expresses the interval-attainable set as an affine image of independent scalar cycle-circulation intervals. It is therefore a possibly degenerate parallelotope and is convex.

This structural observation does not itself require a quadratic law: on any cactus with fixed nominations, each block has at most one circulation coordinate. If independent continuous edge-law parameters range over connected compact domains and the passive state depends continuously on them, each block's circulation image is an interval. The theorem here keeps quadratic scope because that is sufficient for the negative direction and the existing constructive algorithms.

## One varying cyclic resistance parametrizes a graph, not a surface

Let e=(u,v) lie on a cycle. Fix every resistance except beta_e, and remove e from the graph. The remaining graph is connected. If the removed edge is to carry flow q, the remaining network has nominations

    b(q)=b-q(e_u-e_v).

Let P(q) be its physical potential difference pi_u-pi_v. For q_2>q_1, subtract the two remaining-network physical states. Strict monotonicity of the edge laws and the different nomination vectors give

    0<sum_f [g_f(x_f(q_2))-g_f(x_f(q_1))]
               [x_f(q_2)-x_f(q_1)]
      =-(q_2-q_1)[P(q_2)-P(q_1)].

Thus P is strictly decreasing. The full graph's own-edge flow uniquely solves

    P(q)=beta_e q|q|.

Its sign is determined by P(0), independently of beta_e. If P(0)=0, then q=0 and the entire state is constant for all beta_e. Otherwise increasing beta_e changes the equation at its old root by a strictly nonzero term with the sign of q. Hence q(beta_e) is strictly monotone. Continuity of the passive solution makes it a continuous bijection from the resistance interval onto an interval of q values.

All other flows are uniquely determined by q through the remaining network. Therefore the attainable flow set has exactly one vector above each value of its own-edge coordinate q.

If that set were convex, it would contain the line segment between its two endpoint flow states. Every q between the endpoint values occurs on this segment, and uniqueness above q forces the entire attainable set to equal that segment. In particular, every linear flow objective would attain its extrema at endpoint resistance settings.

## Negative direction

The [reviewed weighted-flow cactus characterization](../results/potential-flow-weighted-arc-cactus-characterization.md) provides, on every noncactus simple graph, a box with one varying cyclic resistance and a linear flow objective whose interior setting exceeds both endpoint settings by more than 1/16. The construction retains positive rational data of polynomial encoding length and four fixed nonzero nominations.

The constant-state case in the preceding argument is excluded by this strict objective difference. If its attainable set were convex, the argument would force it to be the endpoint segment, contradicting the interior advantage. Thus its attainable flow set is nonconvex. This proves the converse without introducing a new restoration estimate.

## Potential and joint-state regions: the analogous class is trees

Fix a reference vertex and normalize its potential to zero. The corresponding characterization for potentials is:

> A connected simple graph is a tree if and only if, for every balanced fixed nomination and positive resistance box, its attainable normalized potential region is convex. The same characterization holds for the attainable joint region of flows and normalized potentials.

On a tree, conservation fixes every flow independently of resistance. Each edge drop is linear in its resistance, and normalized potentials are linear combinations of those drops. Thus both the potential region and the joint-state region are affine images of the resistance box.

For the converse, the [reviewed weighted-potential tree characterization](../results/potential-flow-weighted-potential-tree-characterization.md) gives, on every simple graph containing a cycle, one varying cyclic resistance and a linear potential objective with a strict interior advantage over both endpoints. Apply the deletion construction above to that edge. The constant-state case is again excluded. The own-edge flow q varies strictly, and the remaining-network terminal drop P(q) is strictly decreasing. The scalar linear functional pi_u-pi_v therefore takes distinct endpoint values and parametrizes the entire potential curve injectively. Every normalized potential vector is determined by q, hence by this terminal drop.

If the potential region were convex, it would contain the segment joining the endpoint potentials. Every intermediate terminal-drop value occurs on that segment. Uniqueness at each value then forces the entire potential curve to equal the segment, contradicting the strict interior advantage of a linear potential objective. Thus the potential region is nonconvex. The joint-state region is also nonconvex, since its linear projection onto potentials is nonconvex.

This argument inherits the quadratic obstruction, its positive rational data, and its polynomial encoding from the reviewed tree characterization. It uses no new perturbation estimate. The two classifications concern different outputs: cactus structure suffices for convex flow regions, while every cycle can obstruct convex potential regions.

## Every resistance interval may have positive width

The same universal classifications hold if every resistance interval is required to have strictly positive width. The positive directions already allow such boxes. For the converse, start with any compact nonconvex attainable region S above and choose a point z on a chord between two states of S that is absent from S. Compactness gives dist(z,S)>0.

Thicken each fixed resistance coordinate into a sufficiently small positive-width rational interval around its old positive value. The original box remains included. Passive states are jointly continuous in resistances, uniformly on a compact positive-resistance neighborhood. Hence the attainable image of every sufficiently small thickening lies within less than half dist(z,S) of S. It still excludes z, while retaining the two states whose chord contains z, so it remains nonconvex. This argument applies to flows, normalized potentials, and joint states.

This is an existential thickening statement. It supplies no new explicit or polynomial bit bound on the necessary widths; the original one-varying-coordinate witnesses retain their quantitative encoding guarantees.

## Scope, verification, and source qualification

The first characterization concerns flow vectors; the separate tree characterization concerns normalized potentials and the joint state. These are not convexity classifications for arbitrary graphs under fixed linear Ohmic laws. The inherited witnesses use quadratic laws, and only that scope is claimed.

Both [the first full audit](../notes/review-potential-flow-cactus-region-convexity-characterization.md) and [the second full audit](../notes/review-potential-flow-cactus-region-convexity-characterization-second.md) passed. They checked the strict deletion identity, constant-state exception, injective coordinates, potential normalization, and the imported obstruction hypotheses. The positive-width extension is an existential continuity consequence, with no new encoding bound.

The [weighted-objective hierarchy source assessment](../notes/potential-flow-weighted-objective-hierarchy-novelty.md) records classical tree and cycle mechanisms and unresolved older nonlinear-tolerance sources. A separately located Wang–Hasler manuscript, [*Convexity of Resistive Circuit Characteristics*](https://infoscience.epfl.ch/bitstreams/d2fb4e43-bb7e-42b7-977c-39560d9e7d46/download), describes scalar transfer characteristics under source variation in its indexed first page; its full primary PDF could not be retrieved, so no complete theorem comparison has been made. These facts do not establish duplication, but they prevent an exhaustive priority claim for the present region classifications. The elementary convex-graph argument and the established circuit mechanisms are not claimed as new methods.
