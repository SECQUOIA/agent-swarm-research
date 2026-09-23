# Cacti characterize universal linear arc-flow resistance hulls

Date: 2026-09-05. Status: verified by two independent full mathematical audits, with a completed bounded source assessment and qualified publication priority. Simple connected graphs only; all scenarios are unconstrained passive states under the common quadratic law.

## Characterization

For a finite connected simple graph G, the following are equivalent:

1. G is a cactus: every block is an edge or a simple cycle.
2. For every fixed balanced nomination and every linear arc-flow objective d^T x, that objective is separately monotone in each resistance over every positive resistance box.
3. For every fixed balanced nomination and every linear arc-flow objective, independent nonempty compact positive resistance sets have the same maximum and minimum as their interval hulls.

Here separate monotonicity means that each one-variable section is monotone after fixing all other resistances. The increasing/decreasing direction may depend on those fixed values; no common direction vector for the entire resistance box is required.

Every noncactus counterexample can use only four nonzero nominations (4,-4,3,-3), two objective coefficients (-9,5), one uncertain resistance, and positive rational data of polynomial encoding length. The interior scenario exceeds both endpoints by a fixed positive gap.

This statement concerns all linear objectives of flows. The [reviewed individual-arc characterization](../results/potential-flow-series-parallel-arc-characterization.md) has the larger series-parallel graph class. No exact polynomial comparison of sums of independent cycle extrema is inferred here.

## 1. Fixed-nomination cactus cycles separate

Every bridge flow is fixed. Each cycle block has fixed effective nominations obtained by summing nominations in its attached components. Orient the cycle consistently. Its flows are x_e=q+d_e, with fixed offsets d_e, and its circulation uniquely solves

    H_beta(q)=sum_e beta_e(q+d_e)|q+d_e|=0.

Distinct blocks depend on disjoint resistance sets. A linear flow objective is consequently a bridge constant plus one affine function A_C q_C+B_C per cycle.

Hold all cycle resistances except beta_e fixed. At q=-d_e, H_beta is independent of beta_e. Since H_beta strictly increases, the sign of its physical flow q+d_e is constant as beta_e varies; if it is zero once, it is zero always. Increasing beta_e changes H at its old root by a term with that fixed sign. Strict root comparison shows that q is monotone in beta_e or constant. Its affine objective contribution is therefore monotone, proving property 2.

Compact resistance products have attained extrema. Move an optimizing coordinate to an appropriate endpoint without reducing its objective, then repeat for the remaining coordinates. Every endpoint belongs to its original compact scalar set. Thus maxima and minima equal their interval-hull values, proving 1=>2=>3.

## 2. Exact theta obstruction

Use the [weighted-flow theta gadget](potential-flow-weighted-arc-cycle-rank-hardness.md). Edges 0->2,2->1,0->3,3->1 have resistances (1,1,1,2), while 2->3 has resistance theta. At nominations (4,-4,3,-3), writing a=x_02 and q=x_23 gives

    a=q+9-2sqrt(2q+18),
    theta q^2=16-8a,
    F=-9a+5q=-9/2-2(sqrt(2q+18)-9/2)^2.

At theta*=448/81, a=q=9/8 and F=-9/2. The two settings

    theta_L=1792/5329: q=73/32, a=57/32,
    theta_U=12032: q=1/32, a=17/32

both give F=-37/8. The interval interior advantage is exactly 1/8. These are exact rational physical states; the computational candidate proves their physical signs and equations.

## 3. Subdivision into any noncactus simple graph

A noncactus graph has a block that is neither an edge nor a cycle. Choose a cycle in that block. A chord and the two cycle arcs form a theta. If there is no chord but there are off-cycle vertices, an off-cycle component must have two distinct cycle neighbors, since otherwise its attachment is an articulation. A path through that component and the two cycle arcs also form a theta. Thus there are three internally disjoint paths between two vertices.

Designate these branch vertices 2 and 3. Simplicity implies that at most one path has no internal vertex. Choose internal vertices 0 and 1 on two paths, and reserve the third for the uncertain cross resistance. Split the first two paths at 0 and 1 and distribute resistance totals (1,1,1,2) over their respective segments. Put the four fixed nominations at these vertices and zero elsewhere on the selected theta.

If the uncertain path has one edge, its resistance is theta. Otherwise distribute fixed total d=theta_L/2=896/5329 over all but one edge and give the last resistance theta-d. Both endpoint values remain positive. Choose one edge of segment 0->2 as the objective arc with coefficient -9, and one edge of path 2->3 with coefficient 5. At zero internal nominations these flows equal a and q. All subdivision data have polynomial rational encoding length.

## 4. Restore extra edges with an explicit gap

Write m=|E(G)|. Every extra edge receives a common positive integer resistance R, and additional vertices have nomination zero. For all three resistance settings a conservation-feasible comparison flow has

    a=q=9/8, x_21=3, x_03=23/8, x_31=1

on the selected paths and zero on extra edges. Its energy is

    [(9/8)^3+3^3+(23/8)^3+2+theta(9/8)^3]/3.

At theta_U this is 91657/16<6000. Therefore each extra-edge physical flow has magnitude at most

    u=(18000/R)^(1/3).

Total positive nomination is seven, so every full physical flow has magnitude at most seven. Restrict that state to the selected theta and let b' be its induced nominations. Selected degree is at most three, giving |b'_v|<=21. The original and induced nominations lie in a common balanced box with total absolute coordinate bound B<=21m, and

    ||b'-b||_1<=2m u.

For either selected objective edge e, quadratic strong monotonicity and the reviewed nomination-to-pressure Lipschitz estimate along the single-edge path give

    |x_e(b')-x_e(b)|^2
      <=(2/beta_e)|[pi_tail-pi_head](b')-[pi_tail-pi_head](b)|
      <=4B||b'-b||_1<=168m^2 u.

The resistance cancels, so this applies even to the selected edge of the subdivided uncertain path. The weighted objective error is at most 14sqrt(168m^2 u). Set

    R=18000(10^9 m^2)^3.

Then u=1/(10^9m^2), and the squared error bound is

    14^2*168/10^9=1029/31250000<1/1024.

Each scenario changes by less than 1/32. The restored interior scenario therefore exceeds both endpoints by more than 1/8-2(1/32)=1/16. All input resistances have polynomial encoding length and only one is uncertain. Thus every noncactus violates properties 2 and 3, completing the equivalence.

## Interpretation and verification limits

For a fixed nomination and resistance box, agreement of extrema for every linear flow objective is equivalent to equality of the convex hulls of the attainable flow sets. This support-function interpretation is standard. The [focused hierarchy source assessment](../notes/potential-flow-weighted-objective-hierarchy-novelty.md) credits the earlier scalar-cycle and tree results and records unresolved older circuit sources.

The structural proof makes no exact arithmetic claim for sums over many cactus blocks. Independent cycle extrema can belong to different algebraic fields. The separate computational hardness gadget uses only one rank-two block, where exact algebraic verification is polynomial.

Both [the first full audit](../notes/review-potential-flow-weighted-arc-cactus-characterization.md) and [the second full audit](../notes/review-potential-flow-weighted-arc-cactus-characterization-second.md) passed. They checked scalar monotonicity, theta subdivision, induced nominations, the single-edge Hölder estimate, all restoration constants, and universal objective quantifiers. The [weighted-flow source assessment](../notes/potential-flow-weighted-arc-cycle-rank-hardness-novelty.md) records related circuit work. The focused hierarchy assessment found no directly matching full classification in the inspected primary literature, but a closely related older nonlinear-tolerance source remains unread. Mathematical promotion does not assert publication priority.

## A witness with positive objective coefficients

The noncactus obstruction can use the two coefficients `(9,5)` instead of `(-9,5)`. In the isolated theta, select the arc on segment `0->3` and the cross-path arc. Their objective is `9x_03+5x_23=F+36`, so its interior advantage remains `1/8`. After restoring extra edges, use these two selected arcs directly in the error estimate: their coefficient sum is still fourteen, hence the same `R` preserves an advantage greater than `1/16`. The identity with a constant shift is needed only on the isolated theta and is not assumed after restoration. Both independent auditors confirmed this strengthening.
