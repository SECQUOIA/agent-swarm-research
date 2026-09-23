# Exact quadratic arc comparison on series-parallel graphs contains Square-Root Sum

Date: 2026-09-05. Status: corollary passed two independent full mathematical and primary inequality-convention audits. It builds on the reviewed cactus arithmetic reduction and the known series/parallel resistance formula. This is an exact-arithmetic barrier, not an NP-hardness claim; novelty remains a qualified claim for the precise flow restriction.

## Theorem

For common quadratic passive laws, exact comparison of the flow on one prescribed edge with a rational threshold is Square-Root-Sum hard on simple series-parallel graphs of maximum degree three. The nominations are fixed at one unit of injection and one unit of withdrawal, all other nominations are zero, and every resistance is a fixed positive integer. No uncertainty or optimization variables are needed. The lower-comparison problem `x_a>=1/2` already suffices.

The restricted family consisting of a two-terminal cactus with two terminal bridges and one parallel probe edge has a lower-comparison problem polynomial-time many-one equivalent to Square-Root Sum. No upper bound of this strength is claimed for general series-parallel graphs. Block cycle rank in the lower-bound construction grows with the input; this does not conflict with the reviewed fixed-block-rank exact arc algorithm.

The weak `<=` convention used here is explicitly the SQRT-SUM definition in [Etessami and Yannakakis, *On the Complexity of Nash Equilibria and Other Fixed Points*, Section 1](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf), PDF page 4, and is repeated in Section 3, PDF page 22. No reduction from a complementary inequality convention is assumed.

## 1. Start from the reviewed cactus threshold encoder

Use [the reviewed cactus Square-Root-Sum reduction](../results/potential-flow-cactus-square-root-sum.md). For binary positive integers `a_i,K`, the source decision asks whether `sum sqrt(a_i)<=K`. Its output is a simple maximum-degree-three chain of triangle blocks, with positive integer resistances, unit-demand effective quadratic resistance `D>0`, and a positive integer threshold `H` satisfying

```
sum sqrt(a_i)<=K  iff  D>=H.
```

The preprocessing in that result handles removed zero/one radicands and nonpositive thresholds by fixed yes/no instances. Thus nontrivial outputs have `H>0`, and all graph and integer data have polynomial binary encoding length. The cactus source and sink have degree two.

## 2. Add a probe without parallel graph edges

Create new terminals `S,T`. Attach `S` to the old source and the old sink to `T`, each by a resistance-one bridge. The enlarged cactus has effective resistance

```
D'=D+2.
```

Add a direct target edge `a=(S,T)` of resistance

```
beta_a=H+2.
```

The two extra terminals ensure that this new edge does not duplicate an existing edge, including in the one-triangle case. The graph is simple and remains maximum degree three. The extended cactus is a two-terminal series-parallel network, and the probe is a parallel composition with a single edge; hence the resulting graph has no `K4` minor. The resulting nontrivial graph is biconnected and has one more cycle than the old cactus, so its block cycle rank is unbounded over the reduction family.

Fix `b_S=1,b_T=-1` and zero nominations elsewhere. Write `x` for the target flow and `q` for the flow through the extended cactus. Since the source-to-sink drop is positive, both are positive; conservation gives `q+x=1`. Quadratic homogeneity gives

```
D' q^2=(H+2)x^2,
x=sqrt(D')/[sqrt(D')+sqrt(H+2)].
```

Therefore, including equality,

```
x>=1/2  iff  D'>=H+2  iff  D>=H.
```

Every new resistance is a positive integer with polynomial binary encoding length. No square roots are computed in constructing the graph. To keep trivial outputs inside the same literal family, use an old triangle with direct resistance two and alternate-path resistances one and one; its effective resistance is `1/2`. Add the two unit terminal bridges, giving cactus-branch resistance `5/2`, and use probe resistance one for a fixed yes output or nine for a fixed no output. Both use threshold `1/2` and fixed unit demand, and all graph data remain positive integers.

## 3. Matching upper bound on the probe-cactus family

For any input in this family, write `R>0` for the effective resistance of the cactus branch and `beta>0` for the fixed probe resistance. Its unit-demand target flow lies strictly between zero and one. Comparisons `x>=c` are therefore trivial for `c<=0` and `c>=1`, with equality at one impossible. For `0<c<1`,

```
x>=c  iff  R>=beta [c/(1-c)]^2.
```

The right side is a rational threshold comparison of the unit-demand effective resistance of a cactus. The reviewed reverse reduction maps precisely this weak lower pressure comparison to Square-Root Sum in polynomial time. This proves completeness for the restricted family. The weak inequality direction is explicit; no claim about a strict capacity-violation convention is inferred by silently changing equality cases.

## Consequences and scope

The [reviewed envelope theorem](potential-flow-series-parallel-envelope-optimization.md) supplies additive polynomial-bit extrema on arbitrary series-parallel graphs with fixed nominations and uncertain resistances. The present reduction explains why its statement should remain additive: exact arc thresholds already contain Square-Root Sum when there is no resistance uncertainty. The argument also separates the reviewed fixed-rank exact theorem from unbounded block rank.

Square-Root Sum is not known to be NP-hard or polynomial-time decidable. This reduction is not an ordinary NP-hardness result, and it does not obstruct approximation with a prescribed additive tolerance. It adds one parallel probe to the existing arithmetic encoder; the parallel physical formula and the underlying encoder must be credited rather than presented as new standalone ingredients.

Both full independent reviews passed: [first audit](../notes/review-potential-flow-series-parallel-exact-arc-barrier.md) and [second audit](../notes/review-potential-flow-series-parallel-exact-arc-barrier-second.md). They checked the direct and restricted-family reverse reductions, weak inequality and equality conventions, literal-family trivial outputs, simple degree-three graph structure, integer encoding, and the reproducible checks. Both directly verified the primary `<=` SQRT-SUM definition.

The [cactus arithmetic source audit](../notes/potential-flow-cactus-arithmetic-novelty.md) found no matching potential-flow SRS classification, while crediting the known effective-resistance formula. The present one-probe transfer is a short further consequence with a sharper arc-flow scope. A separate exhaustive search for every equivalent old circuit threshold formulation has not been completed. The exact flow arithmetic guarantee is kept distinct from the [classical nonlinear tolerance novelty caveats](../notes/potential-flow-series-parallel-envelope-novelty.md).

## Reproducible encoder checks

[`series_parallel_exact_arc_barrier_checks.py`](../code/potential_flow_mpd/series_parallel_exact_arc_barrier_checks.py) passed 48 complete graph, conservation, pressure, and threshold checks at 90-digit precision, plus 20 nonpositive-threshold preprocessing cases and three exact-equality cases. The graphs were simple, biconnected, maximum degree at most three, with all positive integer resistances. The largest complete-state potential residual was `9.89e-83`. These checks support the rational encoder and equality convention; the complexity claim depends on the written reduction.
