# Second independent audit of convex worst-case performance on cacti

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-cactus-convex-performance-hardness.md) realizes classical convex quadratic Max-Cut maximization on a bounded-data passive cactus. Its strong hardness, fixed additive accuracy consequence, and restricted-family NP/coNP membership are correct. No new combinatorial hardness mechanism is established or claimed.

## 1. Independent cube realization

Use vertex-disjoint triangles, with distinct entrance and exit vertices in each triangle, and join consecutive exit/entrance pairs by bridges. The resulting graph has `3n` vertices and `4n-1` edges. It is simple, is a cactus, and has maximum degree at most three. Directing both routes through each triangle forward and directing all bridges forward gives an acyclic orientation.

The single unit source and unit sink force every joining bridge and every triangle's total through-flow to equal one. Both triangle route flows are positive. The alternate path has resistance four, so equal terminal drops give

```
beta_i x_i^2=4(1-x_i)^2,
x_i=2/(2+sqrt(beta_i)).
```

The function decreases continuously from `2/3` at resistance one to `1/3` at resistance sixteen. Conversely, every `x_i` in this interval is realized by `beta_i=4(1-x_i)^2/x_i^2` in `[1,16]`. Each triangle's resistance affects only its own split; attached blocks see fixed unit effective nominations. Thus the direct flows range over the full independent box, not merely a subset of it.

Consequently `z_i=3x_i-1` ranges over the entire cube. Its zero/one vertices are attained by resistance sixteen/one respectively. All corresponding direct, alternate, and bridge flow coordinates are rational. Every resistance interval or fixed resistance lies in `[1,16]`, and nominations are exactly one and minus one at the two terminals.

## 2. Convex maximization gives Max-Cut exactly

The proposed objective is a sum of squares and therefore convex and nonnegative on the full flow space, not only on its attainable subset. Since differences remove the affine shift in `z`,

```
9 sum_(ij in E(H)) (x_i-x_j)^2
   =sum_(ij in E(H)) (z_i-z_j)^2.
```

At a binary vertex, each summand is one exactly when the corresponding endpoints are on opposite sides of the cut. For every point in the cube, successive one-coordinate convexity comparisons select a vertex with no smaller value. Therefore the continuous cube maximum equals the maximum binary cut value; there is no integrality assumption on the actual resistance decisions and no relaxation gap to estimate.

The result concerns **maximization** of a convex function. The continuous convex-design algorithm minimizes such a function over the same type of convex attainable region. It is fully consistent with this hardness result. In this particular example minimization even has the immediate value zero, attained when all direct flows equal one half. The hardness is in choosing the worst-case jointly coupled cycle endpoints.

## 3. Threshold direction, certificates, and numerical strength

For an integer Max-Cut threshold `K`, a cut of size at least `K` exists if and only if the physical maximum is at least `K`. Since that maximum is an integer, the no case has maximum at most `K-1`. Thus the claimed unit separation holds exactly.

The robust upper predicate `F<=K-1/2` for every resistance scenario holds exactly when no cut reaches `K`. A violating binary endpoint scenario is a polynomial certificate for its complement. On the stated hardware-and-objective family, one verifies a weak threshold or a strict robust violation by evaluating the corresponding integer cut value. Rational endpoint physical states are also available if a direct network certificate is desired. This establishes the asserted NP- and coNP-completeness with the correct quantifier and inequality orientations.

The source can be unweighted simple Max-Cut. All network numbers are constants. In expanded polynomial form, the objective coefficient of `x_i^2` is `9 deg_H(i)` and the coefficient of an edge cross term is `-18`. In the normalized form `F=(1/2)x^T Qx`, the selected-coordinate block of Q is eighteen times the graph Laplacian, with zeros on unused flow coordinates. Its coefficients and the relevant threshold have magnitude polynomial in the graph size. Encoding these numerical data in unary therefore still gives a polynomial-size reduction. Strong NP-hardness is justified; the complementary robust predicate is correspondingly strongly coNP-hard. The candidate keeps completeness membership confined to the verified family.

An additive estimate within one quarter of the optimal value has a unique nearest integer, namely the maximum cut size. It therefore decides Max-Cut. No resistance or nomination scaling is needed. The objective range grows with the comparison graph, so this is not a fixed-error statement for an objective normalized to `[0,1]`.

## 4. Coupling and endpoint scope

The objective couples direct flows from different physical cycle blocks. The physical cactus remains a collection of independent cycle intervals; its geometry and endpoint attainment theorem remain valid. Maximizing a separable sum of scalar cycle objectives would separate, whereas these cross-cycle squared differences encode the comparison graph. Thus neither the positive linear-objective scenario search nor the positive convex minimization theorem is contradicted.

The Max-Cut formulation is classical. The cited Del Pia–Dey–Molinaro preprint explicitly gives the binary cut polynomial in Section 1.1; on binary variables it is the squared-difference expression used here. [Primary preprint](https://arxiv.org/pdf/1407.4798). The present audit establishes the passive-network mapping and its restrictions, not priority for convex maximization hardness.

## Verification

I independently derived the pressure split, inverse resistance map, objective transformation, endpoint reduction, and numerical/certificate bounds. Rerunning `cactus_convex_performance_hardness_checks.py` passed 5,184 exact rational grid states across all 64 simple comparison graphs on four vertices, including endpoint cut values and the bounded-resistance realization. These finite checks support the general proof and do not replace it. No correction is required.
