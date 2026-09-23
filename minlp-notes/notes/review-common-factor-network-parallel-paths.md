# Independent audit: parallel-path network blocks

Date: 2026-09-04. Reviewer: `review_common_factor`.

**Verdict: the candidate theorem, coefficient assertion, and separation construction pass this independent mathematical audit.** Reviewed draft: [parallel-path extension](common-factor-network-parallel-paths.md). The result applies to blocks consisting of internally vertex-disjoint paths between two terminals. It does not cover every series–parallel block. The transportation and minimum-cut ingredients are classical; this audit does not establish novelty of their sparse network application.

## Structural reduction and disaggregation

Subtracting a reference flow `v` with `Av=b` leaves a circulation. Within a parallel-path block, each signed path deviation is constant and the terminal balance is `Σ_i δ_i=0`. Finite arc bounds intersect to give one finite interval for each path. Different biconnected blocks have independent circulation coordinates, as in the previously reviewed cycle/theta theorem. Reference feasibility with respect to capacities is unnecessary.

At simplex state `j`, the scaled path deviations have sum zero, bounds `λ_j[L_i,U_i]`, and affine equality values determined by observed products. Intersecting all equalities and bounds gives exactly `[ℓ_ij,u_ij]`. Multiple observations on one path cause no ambiguity: inconsistent values violate `ℓ_ij≤u_ij`.

For a fixed block, all unobserved simplex states are scaled copies of the same convex bounded path polytope. Their Minkowski sum is the copy scaled by the sum of their weights. A merged state can therefore be refined proportionally. Block coordinates then assemble into a flow separately in every original simplex state. This validates simultaneous gluing despite different blocks observing different sets of state labels.

At a zero-weight state, the original finite bounds force every scaled path deviation to zero. Feasible observation intervals then force the observed products to zero as well. Constructive refinement divides only by positive state weights; zero-weight states can be discarded.

## Exact subset characterization

State feasibility requires the interval inequalities and `Σ_i ℓ_ij≤0≤Σ_i u_ij`. For a column with sum zero, the maximum possible sum on a subset `S` is

```
min{Σ_{i∈S} u_ij, −Σ_{i∉S} ℓ_ij}.
```

Both bounds are necessary. The proposed proof correctly proves their simultaneous sufficiency across all columns and prescribed row sums by transportation, rather than assuming that separately valid supports automatically describe a Minkowski sum.

Under the shift `g_ij=d_ij−ℓ_ij`, capacities are `C_ij=u_ij−ℓ_ij`, row targets are `r_i=δ̄_i−Σ_jℓ_ij`, and column targets are `c_j=−Σ_iℓ_ij`. Local feasibility gives nonnegative capacities and column targets. The subset inequality for the complement of row `i`, together with `Σ_iδ̄_i=0`, gives `r_i≥0`. Total row and column targets agree.

For source-side rows `S`, independently optimizing the side of each column gives minimum cut capacity

```
Σ_{i∉S}r_i + Σ_j min{Σ_{i∈S}C_ij,c_j}.
```

Requiring this to be at least the total target, then adding back `Σ_{i∈S,j}ℓ_ij`, gives exactly the displayed subset inequality in the draft. Thus the max-flow/min-cut theorem proves sufficiency. The empty and full subsets are consistent with local feasibility and zero aggregate sum; no omitted sign or total-balance condition remains.

The classical ingredient is appropriately attributed to the [Ford–Fulkerson primary paper](https://www.cs.yale.edu/homes/lans/readings/routing/ford-max_flow-1956.pdf). The draft supplies the specific network and cut algebra, so the mathematical implication is explicit.

## Coefficients and separation

Every right-hand side in a subset inequality is concave piecewise affine: upper endpoints are minima of affine functions, negated lower endpoints are minima of negated affine functions, and the remaining minimum and sums preserve concavity. Expanding all branches therefore gives a finite, complete family of linear inequalities. Freezing active branches at a candidate gives a globally valid affine upper bound, equal to the nonlinear right-hand side at that candidate. A violation is consequently preserved.

For one state, a branch uses upper endpoints only from paths in `S`, or negated lower endpoints only from its complement. Each selected observed product belongs to one path and one state and is used at most once. Local state-feasibility branches have the same property; an observation selected on both sides of one interval inequality cancels. The aggregate left-hand side uses one signed representative arc from each selected path. Its arcs are distinct. Hence every resulting `x` or `z` coefficient is zero, one, or minus one. Simplex coefficients contain reference-flow and bound data and are not subject to this restriction.

This is an existence assertion for a complete linear inequality family in the stated normalization. It neither bounds primitive integer normalizations of rational facets nor implies bounds on EC&R aggregation multipliers.

If a shifted row target is negative, freezing active lower endpoints gives a valid separating row lower-bound inequality. Otherwise a deficient maximum flow gives a subset violation by the cut argument. A full flow constructs all state deviations. The stated transportation-network counts are correct: `k+a+3` nodes and `k(a+1)+k+a+1` arcs for `a` observed labels and one residual column.

Rational max-flow supplies polynomial bit complexity; the explicit dense path-by-state matrices can have quadratic size in the sparse original input. The draft correctly withdraws the earlier linear-arithmetic separation claim for unbounded numbers of paths. Compact default-state storage and the possible `Θ(m|E|)` size of fully written decompositions are distinguished correctly.

## Supplemental verification and limitations

I inspected [the supplied verifier](../code/common-factor-parallel-paths-verify.py). It enumerates the entire subset family with exact rational arithmetic and compares feasibility against the original unshifted bounded-matrix LP. Its test formulation is independent of the cut transformation. Negative interval endpoints, invalid local intervals, and perturbed aggregate targets are covered. The author reports 300 passing comparisons. The LP side uses floating-point HiGHS; this is numerical corroboration, not an exact LP certificate. The verifier does not test graph decomposition, state merging, coefficient expansion, or a max-flow implementation; those parts were checked analytically above.

The result is a concrete extension to blocks with unbounded cycle rank. Its transportation feasibility oracle and the general existence of a sparse disaggregated extended hull are not new complexity conclusions. Priority for the complete unit flow/product coefficient family remains a separate literature question.
