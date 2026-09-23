# Independent audit of cycle/theta network–simplex hulls

Date: 2026-09-04. Reviewer: common-factor audit agent, independent of the author.

Scope: [Exact sparse network–simplex hulls for cycle and theta blocks](common-factor-network-positive.md). The corrected written theorem passes this audit, including degenerate blocks, zero state weights, sparse-state merging, simultaneous gluing, and the separation bound. One omission in the theorem statement was corrected during review: cycle-state nonemptiness must be required separately from aggregate interval membership.

## 1. Reference flow and block coordinates

An arbitrary solution of `Av=b` is sufficient; it need not satisfy capacity bounds. The difference of any two equality-feasible flows is a circulation. A spanning-forest balance solve produces a reference in linear arithmetic time whenever each weak component has zero total prescribed imbalance. Self-loops contribute independent scalar coordinates and do not obstruct that solve.

The circulation space is the direct sum of the undirected blocks' circulation spaces. In particular, an articulation vertex cannot transfer a nonzero net circulation imbalance between otherwise disjoint blocks. Bridges have zero circulation coordinate, cycle blocks have one signed coordinate, and theta blocks have two independent path coordinates with the third equal to their negative sum. Actual arc orientations only change signs. Parallel arcs are correctly covered by the multigraph interpretation.

Bounds on each path reduce to an interval in its path coordinate. Hence the full bounded flow set is an affine image of a Cartesian product of intervals and the stated three-direction polygons, with bridges fixed. This also identifies emptiness: include the fixed bridge bounds as well as the block tests. No claim for balance inequalities is imported by adding slack arcs without rechecking the resulting graph class.

## 2. State restrictions and degeneracies

For a state of weight `lambda`, its flow is `lambda v+C theta`. Therefore an observed product fixes its signed block coordinate to `epsilon_e(z_ej-lambda v_e)`, exactly as in formula (4). Multiple observations of the same path coordinate must agree; the maximum/minimum intersections enforce this automatically. When `lambda=0`, all scaled base bounds are zero, so the state coordinate is zero and every corresponding observed product must be zero.

The five theta-state feasibility inequalities are necessary and sufficient. The first two coordinate intervals form a rectangle whose attainable sum interval is `[ell_s+ell_t,u_s+u_t]`; this must intersect the nonempty interval `[ell_d,u_d]`. The five inequalities express precisely these conditions. Directly fixing one coordinate and checking the remaining interval gives all six support formulas in (8). Their extrema are attained because the state polygon is compact.

The formulas remain valid for a point or a segment, for zero-width bounds, and for negative coordinate intervals arising from an infeasible reference vector. The reference shift does not change the normal directions.

For cycle blocks, each individual state must satisfy `ell_s,j<=u_s,j`. Aggregate inequalities alone cannot replace this. For example, an impossible state interval `[0.6,0.5]` and a second interval `[0,0.5]` have formal summed bounds `[0.6,1]`, which contain feasible aggregate coordinates even though the first state is empty. The author has explicitly added state feasibility to the theorem statement.

## 3. Why six aggregate supports suffice

Every full-dimensional state polygon has edge directions among the three lines `s=0`, `t=0`, and `s+t=0`. A one-dimensional state polygon also has one of these directions: some defining inequality must hold identically along that segment. A point creates no new direction.

For any nonzero supporting normal, the exposed face of a Minkowski sum is the sum of the corresponding exposed faces. A one-dimensional sum face can contain only parallel nontrivial segment faces. Therefore an edge direction of the sum must already occur in a summand. Its facet normals belong to the six stated normal directions, and its support values in those directions are the sums of the individual support values. These facts prove the aggregate criterion for two-dimensional sums.

If the sum is a segment, its direction is still one of the allowed directions. The two normals perpendicular to it fix its line, and the other listed normals bound its two endpoints. If the sum is a point, the positive and negative coordinate supports already specify that point. Thus no nondegeneracy assumption is needed.

## 4. Sparse-state merging and simultaneous gluing

For one block, every unobserved simplex state has feasible coordinate set `lambda_j P_B`. Their sum is `(sum_j lambda_j)P_B` by convexity, including when `P_B` does not contain the origin. If the merged weight is positive, its chosen coordinate divides proportionally among those states; if the weight is zero, every constituent weight and coordinate is zero.

Different blocks may merge different subsets of the simplex states. This does not create a coupling defect. Refine each block's merged state back to the original state labels using the same global weights. For each original label, assemble its independently feasible block coordinates and its fixed bridge coordinates into `lambda_j v+C theta_j`. The Cartesian-product structure makes this a feasible scaled network flow. Summing labels returns the original aggregate `x`, and all observed products are retained on their explicit block states. This proves global sufficiency, not merely independent local feasibility.

## 5. Linear separation and operation count

Each lower interval endpoint is a maximum of affine expressions, and each upper endpoint is a minimum. Every tight lower support remains convex piecewise affine, because its formulas use maxima, addition of lower supports, or subtraction of an upper support. Tight upper supports are concave by the corresponding argument.

If a state or aggregate condition is violated, fixing the active choices supplies an affine lower estimate on the lower side and an affine upper estimate on the upper side, both equal to their respective values at the query. The selected inequality is therefore globally valid and retains the same violation. Ties may be resolved arbitrarily. This is exact linear separation in the original coordinates.

The number of explicit block states is at most the number of observations. Each block adds one residual state, and each state uses a constant number of support calculations. Together with graph-flow and simplex checks, this gives the stated `O(|V|+|E|+m+|O|)` rational-arithmetic bound for grouped indices. The stated extra comparison-sorting allowance for ungrouped observations is safe. A feasible reference flow LP is unnecessary.

All affine coefficients and query values are formed from input/reference values by linear sums and products with candidate coordinates. Their bit lengths remain polynomial. The arithmetic count is not a claim that arbitrary-precision operations have unit bit cost.

## 6. A further coefficient observation

After active choices are expanded, the displayed family can be written with every original flow and observed-product coefficient in `{0,1,-1}`. An aggregate `s` or `t` uses one representative arc; an aggregate `d=s+t` uses two distinct representative arcs. Within one state, a support expression contains at most two observations from distinct path types. Different states have different product-coordinate indices. State-feasibility comparisons either use distinct path types or cancel a repeated observation, so they do not create coefficients of magnitude two.

The simplex-coordinate coefficients contain reference values and capacity data and need not be unit. With integer balances and capacities, an integer reference can be chosen, making the whole family integral. Any member having a nonzero flow or product coefficient then already contains a coefficient of magnitude one. This is a statement about the explicit inequality family and suitable facet representatives; it does not automatically identify EC&R aggregation multipliers.

The author has been informed of this additional checked consequence and can decide whether to include it as a corollary.

## 7. Validation reviewed

The author's [verification script](../code/common-factor-network-positive-verify.py) computes the state and aggregate formulas using exact rational arithmetic and compares them against an independent LP retaining every simplex state in every block. Its 400 classifications include zero weights, repeated observations, degenerate polygons, and different observed-state sets across blocks. The LP is solved in floating point; graph block extraction is not tested by this script. I inspected this distinction and the LP formulation.

The illustrative theta obstruction is correct: two observed states of weight `1/3` each cannot both allocate their full flow to the third path when its aggregate flow is only `1/3`. The residual state's sum-coordinate upper bound yields exactly the displayed separating inequality.

The corrected theorem has no unresolved mathematical issue from this review. The standard disaggregation and planar Minkowski-sum ingredients, and the application-level novelty question, remain clearly distinguished.
