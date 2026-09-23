# Candidate: region convexity for every nonlinear power law

Date: 2026-09-05. Author: `benders_property`. Status: verified qualitative extension after [two](review-potential-flow-power-law-region-convexity-extension.md) [independent audits](review-potential-flow-power-law-region-convexity-extension-second.md), with a [bounded source assessment](potential-flow-power-law-region-convexity-novelty.md). The claim is qualitative; no quantitative restoration or polynomial encoding bound is supplied.

The reviewed quadratic [region characterization](potential-flow-cactus-region-convexity-characterization.md) appears to extend to every fixed exponent p>0 with p different from 1, for the common passive law

    g_e(x)=beta_e*sign(x)*abs(x)^p.

For connected simple graphs, the proposed universal convexity classes remain cacti for flow regions and trees for normalized potential or joint regions. Uncertainty consists of independent positive resistance intervals and nominations are fixed and balanced. There are no operating bounds. The exponent is fixed, not binary-encoded varying input. The construction below makes no assertion about the exceptional linear exponent p=1.

## 1. A two-nomination theta witness for flow curvature

Use edges 0→2, 2→1, 0→3, 3→1, and 2→3. Their first four resistances are respectively 1,3,2,2. Let the nominations at (0,1,2,3) be (2,-2,0,0). Write q for cross-edge flow and a for flow 0→2. Conservation gives outer flows

    (a, a-q, 2-a, 2-a+q).

Near a=1,q=0, all are positive, and the outer-cycle equation is

    F(a,q)=a^p+3(a-q)^p-2(2-a)^p-2(2-a+q)^p=0.

At that point F=0 and F_a=8p>0. The implicit function a(q) exists and is smooth in a neighborhood of zero. Direct differentiation gives

    a'(0)=5/8,
    a''(0)=(p-1)/32.

For the second identity, the differentiated numerator divided by p(p-1) is

    (1-2)*(5/8)^2+(3-2)*(5/8-1)^2=-1/4.

The cross-edge potential drop at q=0 is 2-1=1. It remains positive for sufficiently small positive q. Thus

    beta_cross(q)=P(q)/q^p

is finite and positive there and realizes the state. Deleting the cross edge gives the strict monotonicity argument of the quadratic review for any strictly increasing edge law. Therefore this beta-to-q parametrization is injective and continuous. Its image contains a nontrivial interval of small positive q.

Since a'' remains nonzero on a sufficiently small such interval, its flow curve cannot be an affine segment. The curve has one vector above each own-edge q. If it were convex, it would equal its endpoint chord, a contradiction. All flows are positive on these selected intervals, and only the two terminals have nonzero nominations.

More explicitly, a has a strict curvature sign on the chosen interval. Let L(q) be its endpoint secant. The linear flow objective `a-L(q)` has zero value at the endpoints and a strictly signed value at any interior point. Reverse its sign if needed to obtain a strict interior advantage. This objective is used only to preserve the obstruction under restoration.

## 2. A triangle witness for potential curvature

Use a path 0→1→2 with both resistances 1 and a direct arc 0→2 with variable resistance. Set nominations (2,1,-3). The path flows are a and a+1; direct flow is 2-a. For a in any compact subinterval of (0,2), choose

    beta_direct(a)=[a^p+(a+1)^p]/(2-a)^p.

It is positive and strictly increasing. With potential at vertex 2 normalized to zero, the remaining potential coordinates are

    (pi_0,pi_1)=(a^p+(a+1)^p, (a+1)^p).

The second coordinate is strictly increasing, and

    d pi_0/d pi_1 = 1+[a/(a+1)]^(p-1).

This derivative is strictly nonconstant when p differs from 1. Thus the potential curve is not a segment and is nonconvex by the same scalar-coordinate argument. Its graph has strict curvature on a compact interior subinterval, yielding a linear potential objective with strict interior advantage over its two endpoints. The joint region is nonconvex because its potential projection is nonconvex.

## 3. Subdivision and restoration on larger graphs

Every noncactus simple graph contains a theta subgraph. At most one of its three branch-to-branch paths is a direct edge, so two distinct paths have internal vertices that can serve as the two nomination terminals in Section 1. Split each of the four outer links and the cross link into paths, assigning zero nominations at new internal vertices. Along such a path the flow is constant, and positive resistance coefficients add for every common exponent p. Fixed link totals can be divided into positive rational shares. On the varying link, reserve a positive fixed total smaller than its interval's lower endpoint and vary one remaining edge. This leaves exactly one uncertain resistance coordinate.

Likewise, subdividing any simple cycle into three nonempty paths embeds the triangle witness. Its three displayed nominations remain the only nonzero ones.

Assign a common large resistance R to every edge outside the selected subgraph. A zero-flow extension of each selected-subgraph feasible comparison flow is feasible on the whole graph. On the compact uncertain interval, these comparison states have uniformly bounded energy

    sum_e beta_e*abs(x_e)^(p+1)/(p+1).

The full physical state minimizes this strictly convex energy. Therefore every extra-edge flow is O(R^(-1/(p+1))), uniformly on that interval. The full graph has fixed nominations and passive strictly increasing laws, so its edge flows are also bounded independently of R by total positive nomination. Restriction to the selected subgraph gives nomination perturbations tending uniformly to zero. Uniqueness and continuity of its physical state then imply uniform convergence of all selected flows as R tends to infinity.

For the potential witness, normalize at a selected vertex. Potential differences along selected paths are continuous functions of the selected flows and their bounded positive resistances, so the three selected potentials converge uniformly as well. The linear objective gives coefficient zero to all added vertices. Hence the strict interior objective advantage survives for sufficiently large finite R.

The varying edge is cyclic in the restored graph. The deletion lemma for strictly increasing laws again makes its own-edge flow, and its terminal potential difference, injective scalar coordinates unless the entire state is constant. The preserved strict advantage excludes the constant case. The chord argument therefore proves nonconvexity on the whole graph.

The interval endpoints chosen through q or a may initially be real. Strict interior inequalities and continuous dependence permit positive rational approximations of the uncertain endpoints and an interior resistance setting; choose rational R sufficiently large as well. Thus rational resistance data exist, but this argument does not bound their encoding lengths uniformly as a function of graph size or exponent.

## 4. Positive directions and scope

For every fixed p>0, strict monotonicity and coercive energy give unique continuous passive flow. On a cactus, each block has one independent circulation coordinate; its compact connected resistance box has an interval image. The complete flow region is consequently an affine product of intervals. On a tree, flow is fixed by conservation and each potential drop is linear in beta even for nonlinear p, so potential and joint regions are affine images of the resistance box.

These arguments would prove the two proposed equivalences once the local curvature and restoration steps receive independent review. They concern universal convexity, not algorithmic complexity. The p=1 curvature identities vanish, so these constructions say nothing about that case. Simplicity is retained because the tree converse can fail on two-vertex parallel-edge graphs.

## 5. Initial source comparison and validation

A symbolic differentiation check independently produced `a'(0)=5/8` and `a''(0)=(p-1)/32` from the displayed F. This checks the local identity only, not the complete theorem.

An initial open-literature search located [Brandenberg and Stursberg, Extremal Solutions for Network Flow with Differential Constraints (2025)](https://link.springer.com/article/10.1007/s10957-025-02792-4). Their Definitions 1.1–1.2 and Section 1.2 fix positive edge elasticities, impose linear potential-flow relations, and vary admissible nomination and capacity bounds. Their cactus characterization concerns nondegeneracy of a polytope's extreme-point description. It is a relevant graph-structural antecedent, but these definitions differ from the present fixed-nomination, variable-resistance, nonlinear-power state image. This direct comparison does not establish novelty.

Search also located the primary preprint titled [Convexity of Resistive Circuit Characteristics](https://infoscience.epfl.ch/bitstreams/d2fb4e43-bb7e-42b7-977c-39560d9e7d46/download); retrieval failed during this initial pass. Its full treatment of characteristic curvature should be checked before making a priority claim. Existing repository source audits of circuit tolerance regions remain relevant. No exhaustive literature exclusion has been completed here.
