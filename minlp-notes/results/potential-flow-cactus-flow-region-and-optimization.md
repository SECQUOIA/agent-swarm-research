# Cactus flow regions: exact scenario recovery and an arithmetic limit

Date: 2026-09-05. Status: verified by two independent full audits, with a completed bounded source assessment. The scalar cycle mechanism is inherited from the weighted arc-flow results. Geometry and exact scenario recovery are separated from exact scalar objective comparison.

## Constructive statement

Fix rational balanced nominations on a connected simple cactus under quadratic passive laws. Give every edge an independent positive rational resistance interval, or a nonempty explicitly listed finite set of positive rational resistances. No physical operating bounds filter scenarios.

The following statements hold:

- Under interval resistances, the entire attainable flow set is an affine image of a box of independent scalar cycle circulations, possibly of lower dimension.
- For finite resistance sets, the convex hull of the attainable flow set is that same box image obtained from their interval hulls.
- Given any rational linear arc-flow objective, an exactly optimizing rational resistance scenario can be found in polynomial bit time, even when the cactus has arbitrarily many cycles. An additive optimal-value estimate is polynomial-time computable in input size and requested accuracy bits.
- Exact comparison of the resulting scalar objective with a rational threshold is square-root-sum hard, already with fixed resistances and unit source/sink nominations. Thus the scenario-search statement must not be conflated with exact scalar threshold evaluation.

The first two claims also imply that every convex function of the flow vector has a worst-case scenario at resistance endpoints, provided its maximum exists. This is a structural consequence, not a polynomial algorithm for maximizing arbitrary convex functions over the resulting box.

## 1. Compute every cycle interval exactly

Bridge flows are fixed. A cycle has fixed effective nominations and, after consistent orientation, flows x_e=q+d_e for rational offsets d_e. Its physical circulation solves

    H_beta(q)=sum_e beta_e(q+d_e)|q+d_e|=0.

Let L_e,U_e be the resistance endpoints. Define

    H_min(q)=sum_e min{L_e(q+d_e)|q+d_e|,
                      U_e(q+d_e)|q+d_e|},
    H_max(q)=sum_e max{L_e(q+d_e)|q+d_e|,
                      U_e(q+d_e)|q+d_e|}.

Both are continuous strictly increasing functions with limits of opposite signs at the two infinities. Let q_max be the unique zero of H_min and q_min the unique zero of H_max. Every original H_beta lies between these functions, so every physical q lies in [q_min,q_max]. Conversely, choosing each endpoint that attains the defining summand at the corresponding zero realizes each extreme exactly. These endpoints belong to the original finite sets as well as to the intervals.

Sorting rational breakpoints -d_e partitions each function into rational quadratic pieces. Locate and solve the relevant piece, treating a linear equation or a breakpoint root directly. Thus q_min and q_max have polynomial-size degree-at-most-two algebraic encodings and are computed exactly in polynomial bit time. Endpoint realization requires only comparing those roots with rational breakpoints. This yields a rational endpoint resistance vector realizing either circulation extreme.

Under interval resistances, physical circulation is continuous in the compact connected resistance box. Its image is therefore the entire interval between its minimum and maximum. Different cactus blocks use disjoint resistance sets and fixed effective nominations, so all their circulation choices can be made independently. If Z contains the signed cycle vectors and x0 is a rational particular conserved flow, the full attainable set is exactly

    {x0+Zq : q_C in [q_min,C,q_max,C] for every cycle C}.

Cycle vectors have disjoint edge supports, making this a possibly degenerate parallelotope in the conserved-flow affine space.

For finite resistance sets, block independence gives a Cartesian product of finite circulation sets. The convex hull of a Cartesian product equals the Cartesian product of its convex hulls. Each scalar convex hull is the same interval because its endpoints are attained. Taking the affine image proves the second geometric claim.

## 2. Exact optimizing scenarios versus scalar values

A rational linear objective d^T x becomes

    C+sum_C A_C q_C

with rational C and A_C. For A_C positive choose the endpoint scenario realizing q_max,C; for A_C negative choose q_min,C; for A_C zero choose any allowed scenario. Combine these choices across blocks. Every selected resistance is a rational input endpoint, and the resulting global scenario is exactly optimal. No comparison of independent radicals is required to select it.

For an additive value error epsilon, approximate each selected circulation to precision epsilon/[2(1+sum_C |A_C|)]. Summing the resulting rational approximations gives the required error, with polynomial dependence on the accuracy bits. Each quadratic root can be enclosed by rational arithmetic in polynomial bit time. One may also return the physical flow coordinates by their separate quadratic encodings; constructing a common algebraic field for all cycles is unnecessary.

The same geometric representation permits exact membership testing of a rational candidate flow in the interval-attainable region, equivalently in the convex hull for finite resistance sets, by conservation and separate quadratic interval comparisons. It does not decide attainability by the original finite resistance sets; that problem is already NP-complete on one cycle, as recorded in the separate inverse-design investigation. This is not a new generic interval-resistance feasibility principle: for any fixed rational flow on any graph, existence of interval resistances satisfying cycle laws is already a rational linear feasibility question. The cactus contribution here is the explicit convex region and optimizing-scenario construction.

For a continuous convex performance function of flows, every point of the parallelotope is a convex combination of its vertices. Each vertex is realized by an endpoint resistance scenario. Convexity therefore bounds its value by a vertex value, proving endpoint worst-case attainment. This does not make arbitrary convex maximization over many cycle coordinates polynomial.

## 3. Explicit square-root-sum reduction for scalar comparison

Use the positive-integer convention of square-root-sum:

    sum_i sqrt(a_i)<=K.

Remove every term a_i=1 and subtract its count from K. If no term remains, compare zero with the adjusted K directly. If terms remain but the adjusted K is nonpositive, the instance is a no instance. Send these decided cases to the fixed outputs described below. Otherwise let m be the remaining number of radicands, all greater than one, and retain the adjusted positive integer threshold K. Build a chain of separate triangles joined by resistance-one bridges, with unit injection at the first terminal and unit withdrawal at the last. Each triangle carries unit through-flow. In triangle i, give the direct arc resistance a_i and give the alternate two-edge path resistances 1/2 and 1/2.

The direct and alternate flows are positive and sum to one. Their equal pressure drops satisfy a_i x_i^2=(1-x_i)^2, so the direct-arc flow is

    x_i=1/(1+sqrt(a_i)).

Assign it the positive integer objective coefficient a_i-1, with zero coefficients on every other edge. Then

    F=sum_i (a_i-1)x_i=sum_i sqrt(a_i)-m.

Consequently F<=K-m is exactly the original square-root-sum comparison after preprocessing. Multiply every resistance by two to obtain positive integer data; flows and F do not change. The graph is simple, is a cactus of maximum degree three, and has only the fixed unit source/sink nominations. No resistance uncertainty is needed.

Fixed preprocessing outputs can use the triangle with direct resistance 8 and alternate resistances 1,1: its direct flow is 1/3 and objective coefficient 3 gives F=1. Threshold 1 is a yes output and threshold 0 a no output, within the same triangle-chain family. The source convention is explicitly given in [Etessami and Yannakakis](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf), Section 1, PDF page 4, and Section 3, PDF page 22.

This is an exact arithmetic barrier, not an NP-hardness claim. It does not contradict the polynomial optimizing-scenario algorithm: in this restricted example all resistances are fixed, so choosing the scenario is trivial, while comparing the weighted radical sum is the arithmetic task.

## Independent verification and source scope

Both [the first full audit](../notes/review-potential-flow-cactus-flow-region-and-optimization.md) and [the second full audit](../notes/review-potential-flow-cactus-flow-region-and-optimization-second.md) passed. They checked scalar quadratic roots, the block product and convex hull, exact endpoint-scenario recovery, additive scalar evaluation, membership scope, and the square-root-sum reduction with preprocessing.

The [focused source assessment](../notes/potential-flow-cactus-flow-region-and-optimization-novelty.md) found no matching complete guarantee, while identifying classical uncertain-resistor geometry and the established distinction between a structural solution and radical-sum evaluation. The affine-box geometry is an elementary consequence of scalar cycle freedom and block independence. The result is positioned as a useful structural corollary with precise computational output guarantees, not a wholly new circuit-geometric mechanism. The literature search remains bounded.
