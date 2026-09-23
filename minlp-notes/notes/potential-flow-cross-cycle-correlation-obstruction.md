# A shared resistance destroys cactus flow-region convexity

Date: 2026-09-05. Status: verified elementary supporting example; the [independent review](review-potential-flow-cross-cycle-correlation-obstruction.md) passed. It isolates the independence assumption in the cycle-polytope algorithm; no complexity hardness claim is made.

## Construction

Join two consistently oriented source-to-sink triangles in series by a bridge of resistance one. Put nomination +1 at the first source, -1 at the last sink, and zero elsewhere. Each triangle carries unit through-flow; the graph is a simple cactus of maximum degree three with an acyclic orientation.

The first triangle's alternate two-edge path has resistances 1/2 and 1/2, total one. The second has resistances 2 and 2, total four. The two direct edges share the same resistance theta in [1,4]. This uncertainty set is a rational polytope: it consists of a box with the linear equality beta_direct,1=beta_direct,2. All other resistances are fixed.

For the common quadratic law, the two direct flows are

    x1=1/(1+sqrt(theta)),
    x2=2/(2+sqrt(theta)).

All physical flows are positive. Eliminating theta gives

    x2=2x1/(1+x1),   1/3<=x1<=1/2.

This is a strictly concave nonaffine graph, so its attainable two-flow projection, and therefore its full attainable flow region, is nonconvex. For example the endpoint midpoint is (5/12,7/12), while the graph above x1=5/12 has second coordinate 10/17. Their discrepancy is exactly 1/204.

## Failure of a shared-parameter endpoint worst case

Consider F=x2-x1. At theta=1 and theta=4 its value is 1/6. At theta=2,

    F=3-2sqrt(2),
    F-1/6=17/6-2sqrt(2)
           =1/[36(17/6+2sqrt(2))]>1/216.

The last inequality uses 17/6+2sqrt(2)<6, which follows by squaring the positive rational bound sqrt(2)<19/12. Thus the convex interval hull of the two correlated endpoint profiles contains a strictly worse linear-flow scenario than either endpoint.

The same conclusion holds with positive unit objective coefficients: use one edge of the first alternate path and the second direct edge, giving (1-x1)+x2=1+F. Both measured flows remain strictly positive.

All data are rational. Multiplying every resistance by two makes every fixed resistance integer and changes the shared interval to [2,8]; it leaves flows and the objective gap unchanged.

## Meaning

Independent polytopes within each cycle preserve the product of circulation intervals. A constraint coupling two cycles need not preserve that geometry. This example is neither a hardness reduction nor a claim that all correlated cactus optimization is difficult. It shows that the independent-cycle theorem and the uncorrelated endpoint-hull theorem cannot simply be applied after introducing shared resistance parameters.
