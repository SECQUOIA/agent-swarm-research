# Independent audit of the parallel-path network extension

Date: 2026-09-04. Reviewer: `review_extension`. Status: passed. Literature novelty remains unestablished.

Reviewed [the candidate](common-factor-network-parallel-paths.md), including the complete subset-cut characterization, its maximum-flow separation, and its original flow/product coefficient claim. It correctly extends the cycle/theta result to arbitrarily many internally disjoint paths in each block.

## Structural reduction and state consistency

The circulation deviation is constant, with the appropriate orientation sign, on each conceptual terminal-to-terminal path. At the common terminals these signed path deviations sum to zero. Conversely, arbitrary path deviations summing to zero give a circulation on the block. Intersecting the signed arc bounds therefore gives exactly the box intersected with `sum_i delta_i=0` in equation (1).

The blockwise circulation splitting and refinement of different merged state sets remain valid for this higher-dimensional polytope. They rely on a Cartesian product of block domains and on positive homothetic copies of one convex block polytope, rather than on the domain's dimension. Thus a feasible matrix in (3) for each block yields one globally consistent flow in every original simplex state. Zero state weights force zero scaled deviations through their initialized bounds. Bridges retain their fixed values and affine observation equalities.

## Exact subset conditions

The local conditions are necessary. With a nonempty interval for each coordinate, `sum ell<=0<=sum u` is also sufficient for an individual column to have zero sum. Any feasible column has its sum on a path subset bounded both by that subset's upper endpoints and by the negative lower endpoints of its complement, proving necessity of (5).

For sufficiency, shifting by the lower endpoints gives capacities `C_ij=u_ij-ell_ij`, row targets `r_i=delta_i-sum_j ell_ij`, and column targets `c_j=-sum_i ell_ij`. The local checks give nonnegative capacities and column targets. The subset condition for the complement of a single row gives

```
-delta_i <= sum_j min{sum_(h!=i) u_hj,-ell_ij}
         <= -sum_j ell_ij,
```

so every row target is nonnegative as well. This implication is valid because aggregate deviations already sum to zero. No missing nonnegative-row-target assumption remains in the characterization.

Total row and column targets agree. In the standard source–rows–columns–sink network, fixing the source-side row set `S` and minimizing independently over each column's side gives

```
cut(S)=sum_(i notin S) r_i
       +sum_j min{sum_(i in S) C_ij,c_j}.
```

The first alternative puts the column on the sink side and pays row-to-column capacities; the second puts it on the source side and pays its column target. Requiring this cut to be at least the total row target is equivalent to the target inequality in the draft. Adding the lower endpoints inside `S` to each minimum converts its two alternatives to `sum_(i in S)u_ij` and `-sum_(i notin S)ell_ij`, respectively. This is exactly (5).

The [maximum-flow/minimum-cut theorem](https://www.cs.yale.edu/homes/lans/readings/routing/ford-max_flow-1956.pdf) therefore gives a matrix meeting every target and capacity. Undoing the shift proves sufficiency. The zero-total-target case is included: every nonnegative row and column target is then zero and the zero shifted matrix works. Empty and full subsets introduce no invalid special case; their conditions agree with the local feasibility requirements.

For three paths, substitute `delta_3=-s-t`. Singleton and complementary-subset inequalities give exactly the six tight supports in the theta formulation. Thus the extension is consistent with the independently audited planar case.

## Original-variable cuts and coefficients

The right side of (5) is concave piecewise affine: upper endpoints are minima of affine functions, negated lower endpoints are also minima of affine functions, sums preserve concavity, and taking the minimum of the two alternatives preserves concavity. Freezing active alternatives gives an affine majorant of the right side that agrees with it at the query point. The resulting inequality is valid on the hull and has the same violation. A negative shifted row target is separated by `delta_i>=sum_j ell_ij`; choosing active lower branches makes this a valid affine inequality too.

Every branch in one state uses either one endpoint from each path in `S` or one negated endpoint from each path in the complement. Consequently no observed product appears twice in that state contribution. Across states its state index differs. The same nonrepetition holds for local feasibility inequalities; an identical observation chosen on both sides cancels. The aggregate sum reads one signed representative arc per path in `S`, without repetitions. Therefore the finite expanded inequality family has flow and observed-product coefficients in `{-1,0,1}` as claimed.

This is an existence statement for the specified rational description. It does not constrain simplex coefficients, primitive integer normalization, or particular EC&R multipliers. In particular, it does not contradict coefficient obstructions for unrestricted network blocks.

## Separation, reconstruction, and scope

After checking the original linear constraints and local state conditions, a negative row target directly yields the preceding valid cut. Otherwise the transportation network is well defined with nonnegative rational capacities. If its maximum flow falls short of the common target total, a minimum cut yields a violated subset inequality after minimizing column sides for the returned row set. If it reaches the target, its matrix reconstructs the block state deviations and hence the full simplex-vertex decomposition.

With `k` paths and `a` observed states, there are `k+a+3` network nodes and `k(a+1)+k+a+1` arcs, matching the draft. Building all block networks has the stated input-plus-dense-state-matrix cost. A polynomial-time rational maximum-flow algorithm then gives polynomial bit complexity. The original augmenting-path method alone is not being claimed as a polynomial-time implementation. The earlier linear arithmetic bound is correctly withdrawn when path counts are unbounded.

The compact decomposition stores path-coordinate vectors for the observed states and one residual default per block. Its size may be proportional to the displayed dense transportation networks. Producing every full state flow can require `Theta(m|E|)` entries; this output cost is correctly retained.

I inspected the author's verification script. It compares exact rational evaluations of all subset inequalities with a separately assembled bounded-matrix LP solved numerically by HiGHS, on 300 small instances. This is useful independent-formulation evidence; it is not an exact certificate of the numerical LP statuses and does not test graph extraction or the max-flow implementation. The proof above establishes the result independently of those tests.

The allowed blocks can have unbounded cycle rank, but the theorem does not cover every series–parallel block. Equality balances and the parallel-path block structure must hold after any modeling transformations. Additional cross-block restrictions or nonlinear flow physics are outside the exact-hull claim. The extension is a correct application of classical capacitated transportation feasibility to this sparse bilinear model.
