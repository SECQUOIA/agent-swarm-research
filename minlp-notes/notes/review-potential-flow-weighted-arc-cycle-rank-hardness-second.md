# Second independent audit of weighted arc-flow hardness at rank two

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-weighted-arc-cycle-rank-hardness.md) gives a valid discrete-resistance reduction with two weighted arc flows, fixed small nominations, and global cycle rank two. The gap, scaling, fixed-rank membership, and rank-one positive boundary pass independent verification. This audit does not establish novelty.

## 1. Physical gadget and objective

With incidence positive at the tail, the stated nominations imply

```
x_21=a+3-q,  x_03=4-a,  x_31=1-a+q.
```

The outer-cycle pressure equation simplifies to

```
a^2-(2q+18)a+(q^2+10q+9)=0,
```

whose stated branch is `a=q+9-2sqrt(2q+18)`. On `[0,3]`, its derivative is `1-2/sqrt(2q+18)`, strictly between zero and one. The four outer flows are all positive: the lower endpoint of `a` is `9-6sqrt(2)>0`, its upper endpoint is `12-4sqrt(6)<4`, and the other two expressions have the positive bounds given in the candidate.

The pressure difference across the cross edge is `(4-a)^2-a^2=16-8a`. Therefore `f(q)=theta q^2+8a(q)-16` is strictly increasing for `q in [0,3]`, negative at zero and positive at three. Its unique root lies in `(0,3)`. Conservation and the two independent cycle equations hold at this root. Positive resistances make the passive energy strictly convex, so this constructed state is the unique physical flow; no competing sign branch was discarded by assumption.

Putting `u=sqrt(2q+18)` gives exactly

```
-9a+5q=-9/2-2(u-9/2)^2.
```

Equality at the upper bound is equivalent to `u=9/2`, then `q=a=9/8`, and then `theta=448/81`. Both displayed endpoint triples also satisfy the outer and cross equations exactly and have objective `-37/8`. The interior advantage is `1/8`. This concave performance curve belongs to a linear combination of two physical arc flows; it does not contradict single-arc monotonicity results.

## 2. Discrete encoding and graph restrictions

Replacing the cross edge by a zero-nomination path makes every segment carry the same `q`, and its effective quadratic resistance is the sum of the segment resistances. The allowed options therefore give

```
theta=(224/81)(1+selected_sum/K).
```

The unique peak resistance is available exactly when `selected_sum=K`. Positive Subset-Sum inputs have `K>0`; targets exceeding the total are harmless fixed no instances. Taking the first path segment as the second objective arc preserves coefficients `(-9,5)`.

The original graph has four vertices and five edges. Subdividing one edge preserves connectedness and cycle rank two, introduces only degree-two vertices with zero nomination, and creates no parallel edge. The maximum degree remains three. Every nonzero nomination remains one of `(4,-4,3,-3)` at the original vertices. Fixed trivial outputs may use the displayed peak or nonpeak rational cross resistance.

## 3. No-instance gap and scaling

For a nonmatching subset, `|theta-theta*|>=224/(81K)>2/K` and `theta<=3(1+S/K)`. Subtracting cross-edge equations gives precisely

```
(theta-theta*)q*^2
 =-(q-q*)[theta(q+q*)+8(a-a*)/(q-q*)].
```

The denominator is positive, its secant term is in `(0,1)`, `q+q*<5`, and `q*^2>1`. Thus with `H=23K+15S`,

```
|q-q*|>2/[K(5theta+8)]>=2/H.
```

The relation `u^2-u*^2=2(q-q*)` and the bound `u+u*<10` imply `|u-u*|>2/(5H)`. Consequently the objective deficit is strictly larger than `8/(25H^2)`, which is larger than `Delta=1/(4H^2)`. The claimed conservative gap and all inequality directions are correct.

At `J=-9/2-Delta/2`, a matching subset strictly violates the upper bound, and every nonmatching subset is strictly below it. This proves the robust-bound reduction with the correct complement direction. A value error below `Delta/4` separates both cases. A returned discrete choice within that additive optimality tolerance on a yes instance must match the target, since every nonmatching choice loses at least `Delta`.

Multiplying every resistance by `81nK` gives exactly the asserted integer options. Common resistance scaling preserves all physical flows by uniqueness while scaling potentials, so the flow objective and gap are unchanged. All integer encoding lengths are polynomial. The separate nomination scaling by `16H^2` scales flow and its linear objective by that factor, making the gap at least four. An absolute error at most one is then separated by the scaled peak minus two. This last operation enlarges the nominations, as the candidate explicitly states. It does not establish fixed-small-nomination constant-error hardness or strong hardness.

## 4. Exact membership at fixed global rank

After guessing one listed resistance option per edge, all numerical data are rational. With fixed balanced nominations, a spanning-tree particular flow and fundamental cycle basis express all flows using the fixed number `r` of chord variables. Bound these by the total possible through-flow from the fixed nominations. On each flow-sign cell, cycle consistency is a system of rational quadratic equations in those fixed variables. These equations together with conservation are sufficient for potential consistency, since the cycle basis spans the kernel of incidence.

A rational threshold for any linear flow objective is an affine inequality in the same variables. Fixed-dimensional real-algebraic decision therefore checks both weak attainment and strict upper-bound violation in polynomial bit time, including equality cases. This yields a deterministic polynomial verifier for the guessed resistance choices without requiring rational physical states. Robust upper satisfaction is its coNP counterpart. Rank-two hardness and the gap give the claimed NP- and coNP-completeness, respectively.

For continuous resistance intervals, the circulation vector remains the fixed-dimensional core; cycle consistency gives only `r` aggregate equations; each resistance is a scalar interval leaf with quadratic core coefficients. The objective is affine in the core. Compact bounds and the reviewed fixed-core theorem therefore give exact algebraic optimization. Finite resistance choices cannot be substituted as polyhedral leaves; the candidate makes this distinction correctly.

## 5. Independent rank-one boundary argument

The cited single-arc theorem applies: with one cycle and fixed nominations, bridge flows are fixed and every weighted arc objective is `Aq+C` for rational constants. Optimizing it reduces to maximizing or minimizing a cycle arc flow. The graph is series-parallel with bounded block rank, as required by that theorem.

There is also a direct proof confined to this setting. Orient the unique cycle consistently. Its flows have the form `x_i=q+d_i` with rational offsets; off-cycle flows are fixed. For fixed resistance choices, cycle consistency is

```
H_beta(q)=sum_i beta_i(q+d_i)|q+d_i|=0.
```

This is a continuous strictly increasing function with a unique zero. Define

```
H_min(q)=sum_i min_{beta_i allowed} beta_i(q+d_i)|q+d_i|.
```

Each summand is continuous and strictly increasing: it uses the smallest allowed resistance for a nonnegative argument and the largest for a negative argument. The zero of `H_min` is the maximal attainable circulation, because every `H_beta>=H_min`, and independently selecting endpoint values attaining the minima at that zero realizes it. The analogous `H_max` gives the minimal circulation.

Sort the rational breakpoints `-d_i`. On each interval the selected endpoints and signs are fixed, so either envelope is a rational quadratic polynomial. Exact root isolation and interval comparison compute its unique root in polynomial bit time. This confirms the rank-one boundary independently, including arbitrary fixed rational nominations, finite choices, coincident breakpoints, and zero cycle flows. Growing numbers of independent cycles would not preserve this scalar argument.

## Verification

I independently derived the physical identities, peak, gap, and both scaling rules, and checked the referenced positive algorithm and fixed-core hypotheses. Rerunning `weighted_arc_cycle_rank_hardness_checks.py` passed three symbolic identities, three exact rational theta states, and 1,778 scenarios over 40 instances, including 43 matching subsets. The maximum complete-state residual was `9.603033e-83`. These checks support the formulas but do not replace the fixed-rank algebraic decision proof or establish literature priority.

## Reviewed positive-coefficient and unit-total-flow corollaries

The author's positive-coefficient corollary passes: conservation at vertex zero gives `x_02+x_03=4`, so

```
9x_03+5x_23=(-9x_02+5x_23)+36.
```

Its peak is `63/2` and every gap is unchanged. Both selected flows are positive in the constructed scenarios, and both coefficients are positive. Under common nomination scaling by `T`, the offset becomes `36T`. This equality holds on the theta and its zero-nomination subdivisions; it should not be used without adjustment after arbitrary extra edges are restored at vertex zero.

The separate unit-total-flow corollary also passes. Replace the `0->3` segment by `9n+1` edges of total resistance one. Keep the other three outer segments as single edges. Replace `2->3` by `5n` edges: `4n` fixed edges of resistance `28/(81n)` and `n` uncertain edges with options

```
112/(81n),   112/(81n)+224a_i/(81K).
```

The total cross resistance is still `(224/81)(1+selected_sum/K)`. There are `14n+4` edges and `14n+3` vertices, so the graph retains global rank two, simplicity, and maximum degree three. Summing **all** arc flows gives

```
(9n+1)(4-a)+a+(a+3-q)+(1-a+q)+5nq
   =n(-9a+5q)+36n+8.
```

Its peak is `(63n+16)/2`, and its no-instance gap is at least `nDelta`. Thus all objective coefficients can equal one, at the cost of objective support growing with the input. All flows are positive for every positive effective cross resistance; subdivisions preserve the directed acyclic orientation. The total signed flow therefore equals the sum of absolute edge flows on every allowed scenario.

Scaling all resistances by `81nK(9n+1)` yields positive integer data: each `0->3` edge becomes `81nK`, each fixed cross edge becomes `28K(9n+1)`, and each uncertain cross edge becomes `112K(9n+1)` or that value plus `224na_i(9n+1)`. The other outer edges are integer multiples of the same scale. Flows and objective values are unchanged. The fixed small nominations are retained; no constant-gap, strong-hardness, or relative-approximation conclusion is inferred from this subdivision alone.
