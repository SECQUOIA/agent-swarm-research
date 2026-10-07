# Discrete resistance choices make arc-capacity validation hard at block rank three

Date: 2026-09-05. Status: theorem passed two independent full proof audits. The precise restricted reduction is a candidate new result; broad circuit-extremum hardness is known, and the source qualifications below remain material. The rank-two pressure gadget alone does not prove edge-flow hardness.

## Theorem

For the common quadratic passive law `pi_u-pi_v=beta_e x_e|x_e|`, deciding whether some independent two-point resistance choice makes a prescribed signed edge flow exceed a rational threshold is NP-complete. Equivalently, robust validation of rational arc-flow capacities over all such choices is coNP-complete.

This holds with fixed small integer nominations on simple graphs of maximum degree three whose entire graph is one biconnected block of cycle rank three. Every uncertain resistance has two positive rational options. The reduction has a positive rational gap of polynomial binary encoding length, so polynomial-time additive arc-extremum optimization in input and requested precision bits would imply `P=NP`. The resistances can also all be made integers by a common polynomially encoded scaling. No strong NP-hardness claim is made. The membership argument below also permits finite rational nomination boxes and arbitrary explicitly listed finite positive resistance choices at every edge, at fixed maximum block cycle rank.

All physical scenarios are unrestricted passive states; capacity validation is the subsequent worst-case comparison. No separate potential or flow bounds restrict which parameter choices are evaluated.

## 1. Reviewed pressure gadget

Use the graph and fixed nominations of [the discrete pressure theorem](../results/potential-flow-discrete-resistance-hardness.md). For positive Subset-Sum integers `a_i,K`, let `S=sum_i a_i`, preprocessing trivial `K>S` cases. Its uncertain cross-path resistances have effective sum

```
tau = 1/2+sum_i a_i sigma_i/(2K).
```

Its two cycles have cross flow `q in(0,2)`, where

```
(12tau+1)q²+10q-23=0.
```

There is also a leaf edge `4->1` of resistance `3` carrying one unit. The nominations on the five distinguished vertices are `(4,-5,3,-3,1)`, with zero at all subdivision vertices. The objective-terminal drop is

```
F_0 = pi_4-pi_0 = 1-(q-1)²/6 in(5/6,1].
```

A target subset gives `F_0=1`; otherwise every resistance choice has

```
F_0 <= 1-Delta,  Delta=6/(31K+18S)².
```

In particular `0<Delta<1`.

## 2. Add a weakly conducting objective edge

Define the positive integer and rational numbers

```
D = ceil(10000/Delta),
H = 1-Delta/2,
M = H D²,
c = 1/D.
```

Add the edge `e=(4,0)` with fixed resistance `M`. Its signed flow is denoted `t`. The old leaf edge and this new edge form an ear joining vertices `1,0` of the theta block. Hence the new graph is biconnected, and its cycle rank is exactly three. Vertices `0` and `4` have degrees three and two; the existing maximum degree three is preserved. Nominations remain unchanged.

For a fixed discrete resistance choice, remove the new edge and let `F(t)` be the old-network terminal drop under the balanced nomination vector

```
b(t)=b+t e_0-t e_4.
```

Conservation shows that the restriction of a full-network physical state to the old graph has exactly these nominations. Therefore its new edge flow solves

```
F(t)=M t|t|.                                  (1)
```

## 3. A monotone perturbation bound

The scalar function `F` is strictly decreasing. To see this, take two old-network physical states with nominations `b(s),b(t)`, flows `x(s),x(t)`, and potentials `pi(s),pi(t)`. Conservation and the constitutive law imply

```
[b(t)-b(s)] dot [pi(t)-pi(s)]
 =sum_e beta_e [x_e(t)|x_e(t)|-x_e(s)|x_e(s)|]
                   [x_e(t)-x_e(s)] >0          (2)
```

whenever `t!=s`. The strict inequality follows from strict increase of the scalar law and the fact that distinct nominations require distinct flow vectors. The left side of (2) is `-(t-s)[F(t)-F(s)]`, proving the claim.

Since `F(0)=F_0>0`, equation (1) has `t>0`: for `t<=0`, the left side is positive and the right side nonpositive. Monotonicity gives

```
0<M t²=F(t)<=F_0<=1,
t<=1/sqrt(M)<=2/D<1.                          (3)
```

The last inequality uses `H>=1/2` and `D>=10000`. Thus the induced old nominations at vertices `0,4` lie in `[4,5]` and `[0,1]`, respectively. Both the original and induced nominations belong to a rational box with total absolute load bound at most `18`. The objective path `4->1->2->0` has total resistance `3+1/6+1/2=11/3`, independently of the uncertain cross path. The reviewed quadratic nomination Lipschitz bound therefore gives the safe sensitivity constant

```
C_b=2*18*(11/3)=132.
```

Because `||b(t)-b||_1=2t`,

```
0<=F_0-F(t)<=264t<=528/D<Delta/8.             (4)
```

This argument works uniformly for every discrete resistance choice. It avoids a hidden dependence on the possibly large effective cross resistance `tau`.

## 4. Rational threshold and separation gap

By construction `M c²=H`. If a target subset exists, choose it. Its old pressure is `F_0=1`, so (4) gives

```
M t²=F(t)>1-Delta/8>H,
t>c.
```

If no target subset exists, every choice has `F_0<=1-Delta`. Since `F(t)<=F_0`,

```
M t²=F(t)<=1-Delta<H,
t<c.
```

Thus a resistance scenario violating the single upper arc capacity `c` exists if and only if the Subset-Sum instance is feasible. Robust satisfaction of that capacity holds if and only if the source instance is infeasible, proving coNP-hardness.

There is a polynomially encoded flow gap. In a target-subset scenario, `F(t)-H>3Delta/8`; in a non-target scenario, `H-F(t)>=Delta/2`. By (3), `t+c<=3/D<4/D`, while `M<=D²`. Therefore

```
|t-c| = |F(t)-H|/[M(t+c)] >= 3Delta/(32D).     (5)
```

An additive extremum-value estimate with error less than `Delta/(64D)` separates yes and no cases. The required precision is polynomial in the Subset-Sum input size. An additive near-optimal discrete scenario with sufficiently small error likewise reveals a target subset on yes instances, which can be verified by integer arithmetic without evaluating the flow.

If a validator expects capacities on every arc, give all other arcs the bounds `[-16,16]`; the fixed nomination vector has total absolute magnitude `16`, so these bounds are automatically satisfied by the acyclic passive-flow bound. The new edge can have lower bound `-16` and upper bound `c`.

## 5. Encoding and scaling

The values `Delta,D,H,M,c` have polynomial rational binary encoding length. The graph has linearly many edges and vertices, and the old uncertain resistance options already have polynomial encoding length. For an explicit common scaling, set `A=31K+18S`; then `H=(A²-3)/A²`. Multiplying every resistance by `6nK A²` makes all resistances positive integers with polynomial encoding length, including the new value `6nK(A²-3)D²`. Common resistance scaling changes potentials by the same factor and leaves all flows and the rational flow capacity `c` unchanged.

The graph still has no active elements or optimized nomination variables. This establishes a discrete-versus-continuous distinction: the reviewed joint continuous-box theorem gives exact arc-flow extrema and capacity validation for every fixed block cycle rank, while independent two-point choices already create NP/coNP hardness at rank three.

## 6. Membership and complete classifications

For any fixed maximum block cycle rank, allow each edge an explicitly listed finite set of positive rational resistances and allow nominations in a finite rational box intersected with balance. A certificate for a possible capacity violation selects one resistance option for each edge, using polynomially many bits. Hold that chosen resistance vector fixed. The reviewed [exact arc-flow algorithm](../results/potential-flow-exact-arc-capacity.md) then computes the exact maximum and minimum signed flow on any edge over the continuous nomination box in polynomial bit time. Comparing these algebraic values with the rational capacities verifies whether a violating nomination exists. The verifier need not be given a rational physical-state witness or an exact nomination witness.

Thus existence of a violating resistance/nomination scenario belongs to NP, and universal arc-capacity satisfaction belongs to coNP. Combined with the rank-three reduction, the former is NP-complete and the latter coNP-complete on the stated graph class. The hardness already uses fixed nominations and two options per uncertain edge; the membership covers the larger explicitly finite resistance-choice model. This argument concerns arc capacities only. It does not transfer NP membership to arbitrary multi-block pressure threshold comparisons, which have a separate exact-arithmetic issue.

## Independent verification and literature scope

Two full independent audits passed: [first audit](../notes/review-potential-flow-discrete-arc-hardness.md) and [second audit](../notes/review-potential-flow-discrete-arc-hardness-second.md). They checked the new-edge orientation, induced nominations, strict monotonicity, constants, rational gap, graph topology, common integer scaling, and NP/coNP membership via the exact fixed-resistance verifier. The second reviewer also independently solved 378 full three-cycle physical scenarios at 70-digit precision; all threshold and gap checks passed, with maximum equation residual `3.0321e-66` in [`discrete_arc_second_review_checks.py`](../code/potential_flow_mpd/discrete_arc_second_review_checks.py).

The [discrete-resistance literature audit](../notes/potential-flow-discrete-resistance-hardness-novelty.md) records established general circuit-extremum hardness and prior discrete pipe-sizing hardness on trees. Their models and objectives differ from this unrestricted fixed-nomination common-quadratic target-flow problem. The proposed contribution is the precise maximum-degree-three, block-rank-three, two-point-resistance restriction and the exact discrete-versus-continuous classification. The audit did not locate an equivalent restricted theorem, but it does not establish exhaustive novelty for every current-extremum formulation. The directly relevant Hasler–Wang 1993 nonlinear tolerance paper remains unread and is a residual source gap. No claim of strong hardness, constant-accuracy hardness, or an FPTAS impossibility follows from the small rational gap.

## Reproducible evidence

[`discrete_arc_hardness_checks.py`](../code/potential_flow_mpd/discrete_arc_hardness_checks.py) independently writes the coupled physical equations for the added edge. It solves for the cross-path flow `q` and the scaled new-edge flow `v=D t`, so the very small physical edge flow does not undermine numerical precision. The script verifies five exact symbolic conservation identities and 296 physical scenarios at 90-digit precision, including 13 target-subset scenarios. All threshold directions and rational gaps passed. The largest observed pressure loss divided by `Delta` was `0.000701`, below the proven `1/8`; the smallest observed flow gap divided by its stated bound was `2.66`. Exact topology checks confirm biconnectivity, cycle rank three, and maximum degree three; the integer scaling is checked exactly.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/discrete_arc_hardness_checks.py`. These checks supplement the mathematical proof and do not themselves establish the worst-case complexity claim.
