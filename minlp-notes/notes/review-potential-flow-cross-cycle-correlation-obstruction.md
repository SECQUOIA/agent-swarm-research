# Independent review: shared resistance across two cycles

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS.

Reviewed [the supporting example](potential-flow-cross-cycle-correlation-obstruction.md). The two triangles in series each carry unit through-flow; the bridge carries one. Their direct resistances theta and alternate-path totals 1 and 4 give exactly `x1=1/(1+sqrt(theta))` and `x2=2/(2+sqrt(theta))`. Eliminating the parameter yields the stated strictly concave curve. Its endpoints are `(1/2,2/3)` and `(1/3,1/2)`, whose midpoint is `(5/12,7/12)`. At the same first coordinate the curve gives 10/17, and `10/17-7/12=1/204` exactly. Nonconvexity of this projection proves nonconvexity of the full flow region.

At theta=2, the linear objective x2-x1 equals `3-2*sqrt(2)`; each endpoint gives 1/6. Rationalization gives the displayed positive gap `1/[36*(17/6+2*sqrt(2))]`, and its denominator is less than 216. The alternate-first-path edge plus second direct edge realizes the same objective plus one with positive unit weights and positive flows.

The graph is connected, simple, cactus, has maximum degree three, and admits the stated acyclic flow orientation. The uncertainty set is a rational segment coupling only the direct resistances. Uniform scaling by two preserves fixed-nomination flows and makes every fixed resistance integral, with the uncertain shared interval [2,8]. No hardness or broad negative algorithmic conclusion follows from this example, as the note correctly states.

The example validly identifies independence **between cycles** as a necessary hypothesis for the product-region argument; polyhedral correlation inside one cycle is still covered by the independently reviewed positive theorem.
