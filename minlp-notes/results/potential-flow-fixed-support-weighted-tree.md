# Fixed objective support makes weighted tree optimization tractable

Date: 2026-09-05. Status: verified by two independent full mathematical audits; the bounded source search found no matching support-parameter theorem. The contribution under investigation is the objective-support parameter and exact rational algorithm, not the established electrical sensitivity or fixed-dimensional optimization ingredients.

## Theorem

Fix an integer `p`. On a connected tree, consider unconstrained passive quadratic states

```
Ax=b,   A^T pi=(beta_e x_e|x_e|)_e,
l<=b<=u,   sum b=0,
```

where the incidence column of an oriented edge is `+1` at its tail and `-1` at its head. All nomination bounds are finite rational numbers. Each positive resistance belongs independently either to a closed rational interval or to an explicitly listed finite rational set. Let `c` be a rational vector with `sum c=0` and at most `p` nonzero entries.

Then the exact maximum and minimum of `c^T pi` can be computed in `N^{O(p)}` bit operations, where `N` is the total binary input length. An optimal nomination, resistance choice, flow, and potential vector can all be returned as rational numbers of polynomial binary length for fixed `p`. No additional pressure or flow bounds restrict the scenario set. Empty nomination domains are detected first.

This is a fixed-parameter-size polynomial statement, not a claimed fixed-parameter tractable running time `f(p)N^C`. The distinction from growing objective support matters: a separate convex-knapsack reduction gives nomination-box hardness already on a tree when the support of `c` grows. It also matters that the graph is a tree: fixed support three permits discrete-resistance hardness on one cycle, as shown in the [reviewed cycle result](../results/potential-flow-weighted-potential-cycle-hardness.md).

## 1. Eliminate edges absent from the objective

Fix a reference potential. On a tree, there is a unique vector `w` satisfying `Aw=c`, and

```
c^T pi=w^T A^T pi=sum_e w_e beta_e x_e|x_e|.       (1)
```

Each `w_e` is the signed sum of `c` on one side of the edge cut. Similarly, the physical flow is the unique vector satisfying `Ax=b`; it depends linearly on nominations and is independent of resistances. Every such flow has a unique potential vector modulo constants under the edge laws.

Contract every edge with `w_e=0`. The objective has no contribution on a contracted edge. Each contracted cluster becomes one vertex with nomination interval equal to the sum of its original intervals and objective coefficient equal to the sum of its original coefficients. The projection of a product of real intervals under summation is exactly the summed interval. Thus every feasible aggregate nomination has an original feasible disaggregation, and the retained edge flows and objective agree exactly with those of the original tree. Balancedness is preserved. Rational aggregate nominations can be disaggregated greedily using rational arithmetic.

The contracted graph is a tree. Every remaining edge has nonzero `w_e`, and at most `p` vertices have nonzero aggregate `c`. A leaf must have nonzero `c`, since its only incident edge has cut weight equal to its signed leaf coefficient. If no edge remains, the objective is zero and the problem is immediate.

Mark all vertices with nonzero `c` and all vertices of degree at least three. There are at most `p` marked objective vertices and at most `p-2` branching vertices. Thus there are at most `2p-2` marked vertices. Suppressing all other vertices produces a tree on the marked vertices, with at most `2p-3` paths. An internal vertex of such a path has degree two and coefficient zero, so after orienting the path consistently, its nonzero cut weight `w_e` is constant along the path.

## 2. A polynomial family of nomination faces

First hold all resistances fixed. For `rho>0`, replace the scalar edge law by

```
g_e^rho(x)=beta_e(x|x|+rho x).
```

Tree flows remain linear in nominations. Let `F_rho(b)` denote the resulting weighted potential objective. It is continuously differentiable. If `h` is its nomination gradient modulo a constant, then along an edge

```
h_tail-h_head=w_e beta_e(2|x_e|+rho).              (2)
```

One can obtain this directly by differentiating (1) and using cut-flow formulas; equivalently it is the electrical adjoint identity. Since the multiplier of `w_e` is strictly positive, `h` is strictly monotone along each suppressed path. Its direction depends only on the oriented cut weight, not on nominations or resistances.

At a maximum of `F_rho` on the nomination box intersected with balance, the normal cone of that polytope supplies a scalar `lambda` such that

```
h_v>lambda implies b_v=u_v,
h_v<lambda implies b_v=l_v,
l_v<b_v<u_v implies h_v=lambda.                  (3)
```

For coordinates with `l_v=u_v`, the coordinate is fixed and can be assigned either endpoint status. Formula (3) follows from the normal cone of a polyhedron and does not require an interior feasible nomination. In particular, along every suppressed path there is at most one internal coordinate that is neither fixed to its lower bound nor fixed to its upper bound. The endpoint statuses on either side of that coordinate follow the strict monotone order of `h`.

For each path, enumerate all placements of a single free internal coordinate with all preceding and succeeding coordinates fixed to their prescribed endpoint types. Also enumerate all cuts between successive internal vertices, including the two extreme cuts, with no free coordinate. At each marked vertex independently enumerate lower, upper, and free status. The path orientation determines which side is lower and which is upper. Empty paths require one choice. These choices define closed box faces; balance is imposed afterward. The number of faces is `N^{O(p)}`. Every face has at most

```
(2p-3)+(2p-2)=4p-5
```

free nomination coordinates before eliminating balance.

This finite family is independent of resistances and of `rho`. On the compact nomination polytope, `F_rho` converges uniformly to `F_0`: the perturbation is `rho sum_e w_e beta_e x_e`, with bounded tree flows. Select smoothed maximizers along a sequence `rho->0`. A subsequence belongs to one fixed closed face and converges to a nomination in that face. Uniform convergence proves that its limit maximizes the original objective. This proves existence of an original maximizer on the enumerated family, without assuming nonzero physical flows.

For joint resistance optimization, choose a joint maximizer `(b*,beta*)`, which exists by compactness and continuity. Hold `beta*` fixed and apply the preceding result. A nomination on the same resistance-independent face family achieves the joint optimum at `beta*`. Thus the face family is also complete for joint optimization. Finite resistance sets are compact, so the same argument applies to them.

## 3. Eliminate all resistance variables exactly

On a tree the flow is fixed once nominations are fixed. Therefore (1) is separately linear in each resistance. Write `L_e` and `U_e` for the minimum and maximum allowed resistance, whether the input set is finite or an interval. An optimal resistance is

```
beta_e=U_e if w_e x_e|x_e|>=0,
beta_e=L_e if w_e x_e|x_e|<0.                     (4)
```

At zero either endpoint works. Both endpoints are actual allowed values. Choices on contracted zero-weight edges are arbitrary allowed endpoints.

Consider one enumerated nomination face. Intersect it with balance, eliminate a free coordinate when one exists, and parameterize its remaining affine space using at most `4p-5` rational variables `z`. Infeasible faces are discarded. A zero-dimensional face is evaluated directly. Every edge flow is an affine rational function of `z`. Partition the face by the hyperplanes `x_e(z)=0`; in fixed dimension, there are polynomially many sign cells. It is enough to use the closures of the full-dimensional cells relative to the feasible affine hull. Identically zero flows are removed from the arrangement; lower-dimensional feasible sets are first parameterized in their rational affine hull. Standard incremental hyperplane arrangement enumeration can be implemented using rational linear feasibility queries in fixed dimension.

On each closed sign cell, the endpoint rule (4) is fixed, and the objective is a single rational quadratic polynomial in `z`. At a zero-flow boundary, either neighboring choice gives the same zero contribution, so use of closed cells introduces no inconsistency. All cells are bounded rational polyhedra. Coefficient bit lengths remain polynomial under cut summation, affine substitution, and endpoint selection.

## 4. Exact rational maximization of a quadratic in fixed dimension

The following elementary procedure avoids an algebraic output claim when rational output is available. Polynomial-size rational optimal witnesses for rational quadratic programming are classical: Vavasis (1990), restated as Theorem 3 in Section 2.2 of [Del Pia, Dey, and Molinaro](https://arxiv.org/pdf/1407.4798), PDF page 3. The direct procedure below supplies the fixed-dimensional algorithm used here; neither its rationality conclusion nor general quadratic-programming membership is claimed new.

Let `P={z:Az<=d}` be a nonempty bounded rational polyhedron in a fixed-dimensional affine coordinate system, and let

```
q(z)=1/2 z^T Q z+g^T z+k,
```

where `Q` is symmetric rational. Enumerate every subset `I` of at most `dim(z)` inequality rows whose normals are linearly independent. Include the empty subset. For each subset solve the rational linear feasibility system in `(z,mu)`

```
Az<=d,
A_I z=d_I,
Qz+g=A_I^T mu.                                  (5)
```

No sign restriction on `mu` is needed: only stationarity on the selected affine face is being used. Each feasible system yields a rational feasible point and its exact rational objective value.

A global maximizer lies in the relative interior of its minimal face of `P`. The active normals have a linearly independent basis `I`, and first-order stationarity along that face gives (5). Hence the enumeration includes at least one nonempty system containing a global maximizer. Moreover, every solution of that same system has the same quadratic objective: for two solutions `z,z'`, their difference `v` satisfies `A_I v=0` and `Qv=A_I^T(mu'-mu)`, so `v^TQv=0` and `v^T(Qz+g)=0`. The quadratic expansion then gives `q(z')=q(z)`.

Consequently choosing an arbitrary rational feasible point for each system and retaining the largest value is exact. Other stationary systems can give smaller values, but every returned point is feasible in `P`. Rational linear programming returns a polynomial-bit feasible point whenever (5) is feasible; this holds even if the multiplier set is unbounded. There are only polynomially many subsets at fixed dimension. Thus each sign-cell maximum and a rational optimizer are computed exactly in polynomial bit time.

## 5. Recovery, complexity, and boundaries

Compare all cell and face values by rational arithmetic. The winning aggregate nomination disaggregates rationally into the original intervals. Use (4) to recover allowed resistances. Tree cut summation gives rational flows, and summing rational quadratic edge drops along a spanning tree gives rational potentials after fixing one reference to zero. All these outputs have polynomial bit size for fixed `p`.

The total number of faces, sign cells, and active-normal subsets is `N^{O(p)}`. Every subproblem is rational linear feasibility or linear algebra with polynomial-bit data. This proves the proposed complexity bound for the maximum. Replacing `c` by `-c` gives the minimum and preserves objective support.

The algorithm uses tree flow uniqueness and objective cut weights at several essential points. It does not extend unchanged to one-cycle graphs, additional physical feasibility constraints, or objectives with growing support. The face proof does extend structurally to strictly increasing smooth edge laws, but this note only claims the quadratic algorithm and its rational output.

## Independent verification and novelty limits

Both [the first independent audit](../notes/review-potential-flow-fixed-support-weighted-tree-independent.md) and [the second independent audit](../notes/review-potential-flow-fixed-support-weighted-tree-second.md) passed. They checked contraction, degenerate nomination domains, closed-face limits, joint resistance optimization, rational quadratic stationarity systems, and output bit complexity.

The [focused source audit](../notes/potential-flow-fixed-support-weighted-tree-novelty.md) found no equivalent exact support-parameter theorem. Cut-flow formulas, two-terminal tree nomination algorithms, electrical sensitivities, and rational quadratic optimizer results are established. The plausible new part is the support-controlled, resistance-independent nomination-face family and its combined optimization guarantee. This bounded search does not establish exhaustive novelty.

## Reproducible checks

[`fixed_support_weighted_tree_checks.py`](../code/potential_flow_mpd/fixed_support_weighted_tree_checks.py) checked five small trees with objective support two, three, and four. For every flow-sign cell, it enumerated all independent active-normal sets and solved the corresponding stationary systems, including singular systems by linear feasibility. Across 3,119 feasible stationary candidates, the best value was always attained by a nomination in the proposed threshold-face family. Every candidate's selected resistance value was also compared with all resistance corners. The cases include a singleton balanced domain and a fixed nomination coordinate. Four separate quadratic controls cover an interior maximum, an edge maximum, a vertex maximum, and a flat objective. Thirty further random trees verified zero-weight contraction and objective recovery with exact rational arithmetic.

These checks passed. The stationary enumeration uses floating-point linear algebra and linear programming and is evidence for the structural and algorithmic formulas, not an implementation of the exact rational bit algorithm or a replacement for proof review.
