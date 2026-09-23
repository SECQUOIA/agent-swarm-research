# Independent audit: trees characterize universal weighted-potential resistance hulls

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**Verdict: PASS.** The equivalence and explicit restoration argument in [the candidate](potential-flow-weighted-potential-tree-characterization.md) are correct. No correction is required. This is a mathematical audit, not a novelty clearance.

## Positive direction and quantifiers

On a tree, conservation uniquely fixes every edge flow at fixed balanced nominations. With the incidence convention used throughout the repository, the unique cut-flow vector `w` satisfying `Aw=c` gives

```
c^T pi = w^T A^T pi = sum_e w_e beta_e x_e |x_e|.
```

Thus the objective is affine in all resistances simultaneously. Coefficient signs do not change with resistance, including when a coefficient is zero. This proves separate monotonicity for every permitted nomination and objective, with no rationality restriction needed for the structural statement.

Separate monotonicity on a box suffices for endpoint-hull equality: starting from any box point, successively replace each coordinate by an endpoint that does not decrease the objective. The resulting vertex is in the original product of compact sets. Reversing the inequality gives the minimum statement. This argument does not require the monotonicity direction of a coordinate to be independent of the other coordinates.

Extrema are attained. On a compact product of positive resistance sets, all coefficients are uniformly positive. The strictly convex coercive flow energy gives a unique conserved physical flow; its response is continuous in resistance. For example, bounded physical flows and the minimizing inequalities show that every convergent-parameter subsequence has the unique limiting minimizer. Normalized potentials then vary continuously by path summation. This also checks the compact-parameter formulation in property 3.

## Triangle and subdivisions

The triangle is the previously independently audited obstruction from [the cycle result](../results/potential-flow-weighted-potential-cycle-hardness.md). The roots `-3/8,-1/4,-1/8` at resistance totals `16/3,24,144` satisfy the signed quadratic cycle equation. Their objective values are `-423/16,-105/4,-423/16`, so the strict interior improvement is `3/16`.

Every cycle of a simple graph has at least three vertices. Choosing three of its vertices partitions it into three nonempty paths. Zero internal nominations make each path flow constant, so its effective quadratic resistance is its sum of edge resistances. On the uncertain path, the fixed offset `d=8/3`, when used, is strictly less than the lower total `16/3`. Therefore both endpoint values and the interior value of the single varying edge remain positive. All other path resistances are positive as well. The subdivision exactly preserves the three branch potentials up to a constant and hence preserves the weighted objective.

## Restoring additional edges

For every one of the three resistance settings, the comparison flow with circulation `q=-1/4` has conserved branch flow `(7/4,-5/4,-1/4)` and zero extra-edge flow. It is feasible on the full graph, including extra vertices with zero nomination. Subdivision does not change its energy, which is

```
(468+theta)/192 <= 612/192 < 4.
```

The physical minimizer has no greater energy. Each extra edge of resistance `R` therefore carries flow of magnitude strictly less than `(12/R)^(1/3)`; using a weak inequality as in the candidate is safe.

The full graph's total positive nomination is three. Orienting every nonzero physical flow by its sign yields an acyclic graph because potential strictly decreases along each such edge. Flow decomposition then bounds each edge magnitude by three.

Restrict the full physical flow and potentials to the selected cycle. Conservation there defines a balanced induced nomination `b'`; balance follows directly by summing the cycle incidence equations. The restricted state satisfies every original cycle law and is consequently the unique physical state for that induced nomination and the same cycle resistances. This justifies applying the nomination sensitivity theorem to it. It is not an approximation that ignores the restored edges.

Each cycle vertex has two incident cycle edges, so `|b'_v|<=6`. The box `[-6,6]` at all cycle vertices also contains the original nomination and has total absolute load bound at most `6m`. At each cycle vertex, `b'-b` is minus the signed contribution of extra incident edges. Summing their absolute values counts each extra edge at most twice, giving `||b'-b||_1<=2m u`.

The two fixed paths used in the objective each have resistance sum one. The reviewed nomination bound for their pressure differences therefore gives

```
|F(b')-F(b)|
<= (5+7) 2(6m) ||b'-b||_1
<= 288m^2 u.
```

The decomposition `F=-5(pi_0-pi_1)+7(pi_1-pi_2)` has the stated signs. It uses fixed-resistance paths, so the large uncertain-path resistance does not enter this sensitivity constant.

For `R=12(10000m^2)^3`, one has exactly `u=1/(10000m^2)`. Each objective changes by at most `288/10000<3/64`. Thus the restored interior value exceeds each restored endpoint by at least `3/16-576/10000=1299/10000`, which is strictly greater than the candidate's conservative `3/32` gap.

## Scope and conclusion

All restored data are rational with polynomial encoding length; indeed the common integer `R` has `O(log m)` bits apart from a fixed constant. Only one resistance remains uncertain. Taking its two endpoint values as the compact finite set yields a product whose maximum is strictly below that on its interval hull. This disproves property 3 on every non-tree simple graph and, because the same one-dimensional section has an interior value exceeding both endpoints, also disproves property 2.

The proof therefore gives the universal equivalence for finite connected simple graphs, including the trivial one-vertex tree. It does not assert a corresponding multigraph boundary: two-vertex parallel-edge examples lie outside the hypothesis. It also does not infer the same theorem for fixed linear Ohmic laws or for scenario sets restricted by additional physical capacities or potential constraints.

The structural argument uses fixed nominations and arbitrary zero-sum weighted potential objectives. The related discrete-resistance computational hardness and the hierarchy for other objective classes remain separate statements. No new numerical large-resistance solve was needed for this audit; the triangle identities were checked in the earlier cycle audit and the restoration follows from explicit energy and sensitivity inequalities.
