# Second independent audit of nonlinear power-law region convexity

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-power-law-region-convexity-extension.md) proves the qualitative universal classifications for every fixed real exponent `p>0`, `p!=1`: cacti for convex flow regions, and trees for convex normalized potential or joint regions, on connected simple graphs. The argument covers `0<p<1`. It establishes existence of rational resistance data for the counterexamples, without claiming a uniform encoding bound or a polynomial-time construction. This review checks correctness, not literature priority.

## 1. The theta curvature calculation

The displayed outer flows satisfy conservation with nominations `(2,-2,0,0)`. At `(a,q)=(1,0)` all four outer flows equal one, so their real powers are smooth for every positive p. The outer cycle equation has

```
F_a=8p, F_q=-5p,
a'(0)=-F_q/F_a=5/8.
```

The second directional derivative along `(a',1)` is

```
p(p-1)[(a')^2+3(a'-1)^2-2(a')^2-2(a'-1)^2]
=p(p-1)[1-2a']=-p(p-1)/4.
```

Dividing its negative by `F_a` gives `a''(0)=(p-1)/32`. Hence the implicit curve has a persistent nonzero curvature sign in a neighborhood when p differs from one.

The deleted-cross-edge potential drop is `P(q)=2(2-a(q))^p-a(q)^p`, with `P(0)=1`. Select a compact interval of sufficiently small strictly positive q. Then all outer flows remain positive, P remains positive, and `beta=P(q)/q^p` is finite and positive. The proof does not claim a finite resistance realizes q=0 in the original five-edge network. It also does not differentiate the cross law at zero. This distinction is essential for, and correctly handles, powers below one.

The remaining-network monotonicity identity makes P strictly decreasing. Since q is positive on this selected interval, `P(q)/q^p` is strictly decreasing too. Thus its image is a nontrivial resistance interval and every selected q is exactly the physical state for the corresponding resistance. The implicit outer equation and the cross drop equation together enforce both independent cycle equations.

The `(q,a)` graph has strict curvature. Its deviation from its endpoint secant has a strict sign at every interior point. Choosing the sign gives a linear flow functional with strict interior advantage over both endpoint values; dropping its constant term leaves the comparison unchanged. The full flow curve is nonconvex because q is a linear coordinate with exactly one state above it, and convexity would force the curve to equal its endpoint segment.

## 2. The potential triangle

The flows `a,a+1,2-a` give the stated nominations. For `0<a<2` they are positive. The direct resistance is the ratio of a positive strictly increasing numerator to a positive strictly decreasing denominator, and hence is strictly increasing and continuous.

With `pi_2=0`, the potential coordinates follow by summing path drops. Their derivatives give

```
d pi_0/d pi_1=1+(a/(a+1))^(p-1).
```

The derivative of this expression with respect to a is

```
(p-1)(a/(a+1))^(p-2)/(a+1)^2,
```

which is nonzero and has fixed sign for p different from one. Since `d pi_1/da=p(a+1)^(p-1)>0`, this proves strict curvature when the curve is graphed above the linear coordinate pi1. Its secant gives the stated strict linear objective advantage and its potential image is nonconvex. A convex joint region would have convex potential projection, so the joint conclusion has the correct direction.

All differentiations in both base constructions occur at positive flow arguments, where fractional powers are smooth. Nothing here requires differentiability of the signed power at zero.

## 3. Subdivisions and graph topology

A noncactus connected simple graph contains a theta subgraph. At most one of the three internally disjoint paths between its branch vertices is a direct edge, since the graph is simple. Choose an internal nomination terminal on each of the other two paths. Their two sides give the four outer links, and the remaining branch-to-branch path gives the cross link. This realizes a subdivision of precisely the proposed two-nomination theta gadget, with the branch vertices themselves carrying zero nominations.

A simple cycle has at least three vertices and can similarly be divided into three nonempty paths for the triangle gadget. Zero nominations at new subdivision vertices force a common signed flow along a consistently oriented path. For the common exponent p, its pressure drops sum by adding the positive resistance coefficients. Thus fixed rational link totals can be split into rational positive shares.

If the varying link has several edges, choose a rational fixed total smaller than its positive interval lower endpoint and assign the remaining resistance to one edge. This preserves one varying coordinate. That edge remains cyclic after adding the other graph edges. The two-nomination theta and three-nomination triangle scopes are preserved by adding zero nominations elsewhere.

## 4. Restoration, including powers below one

For any p>0, the energy `sum beta_e |x_e|^(p+1)/(p+1)` is differentiable, strictly convex, and coercive on conserved flows. Its derivative is the continuous signed power law even when that law has an unbounded derivative at zero. Minimization gives the unique physical flow, and no second derivative is needed.

A selected-subgraph feasible flow extended by zero is feasible on the whole graph. Over a compact uncertain resistance interval its energy has a uniform finite bound independent of the large resistance R assigned to added edges. The full minimizer therefore satisfies `|x_e|<=C R^(-1/(p+1))` on each added edge. This estimate is valid on either side of p=1.

Independently, every physical edge flow is bounded by total positive nomination. Orient the nonzero flows in their positive direction. Strictly positive drops rule out a directed cycle, and the resulting conserved acyclic flow decomposes into source-to-sink paths of that total amount. Thus full and selected flows are uniformly bounded independently of R.

Here is a direct justification for the claimed uniform convergence. In a contrary sequence with R tending to infinity, extract a convergent subsequence of selected flows and the compact uncertain resistance parameter. The vanishing added-edge flows make selected conservation converge to the original nomination. Every selected cycle equation passes to the limit by continuity of the signed power. These are the conservation and potential-consistency equations for the selected graph. Strict convexity identifies their flow uniquely with the selected physical state. Continuous dependence of that state on its parameter then contradicts failure of uniform convergence. This argument makes no local Lipschitz or derivative assumption at zero.

Normalize potentials at a selected vertex and recover each selected potential by summing drops along selected paths. Bounded selected resistances and converging flows give uniform convergence of these potentials. Potentials at other vertices need not be uniformly bounded in R; they receive zero objective coefficients, so the proof does not need that property.

Consequently each chosen strict interior objective advantage survives for some finite sufficiently large R. This is an existential restoration estimate, as stated.

## 5. Why the restored curve remains nonconvex

Delete the varying cyclic edge, oriented from u to v. The remaining graph is connected. Prescribing its missing-edge flow q changes the remaining nomination to `b-q a_e`. For two different values, the remaining flows differ. Strict monotonicity gives the finite-difference identity

```
0 < sum_f (g_f(x_f')-g_f(x_f))(x_f'-x_f)
  = -(q'-q)(P(q')-P(q)),
```

where P is the missing-edge terminal drop. Hence P is strictly decreasing, with no differentiability assumption. Physical consistency is `P(q)=beta sign(q)|q|^p`.

If q is zero for one resistance, then P(0)=0 and the same zero own-edge flow solves the consistency equation for every resistance. The remaining nomination and all its normalized state data are fixed, so the entire state is constant. Otherwise the sign of q is fixed by P(0), and comparing the decreasing P with the strictly increasing signed power shows a strictly monotone dependence of q on beta. P(q) is then also an injective scalar coordinate.

The preserved strict objective advantage excludes the constant case. For the flow curve use q; for the potential curve use the linear terminal-drop functional P. In either case, convexity and uniqueness above the scalar coordinate would force the image to be the endpoint segment. Such a segment cannot contain a state with the preserved strict linear advantage. This supplies the needed argument after restoration: the advantage alone would not exclude convexity for an arbitrary higher-dimensional image.

## 6. Rational data, positive cases, and exclusions

After choosing a finite restoration resistance, the strict comparison at three parameter settings persists under sufficiently small perturbations by continuous dependence. Positive rational endpoint and interior resistance values can be chosen with the same ordering, and R can itself be rational. The fixed gadget resistances, nomination values, and subdivision shares are rational already. Thus rational data exist even when the fixed exponent is irrational. Density and openness establish existence only; they do not provide a uniform bit bound.

On a cactus, conservation gives one scalar circulation for each edge-disjoint cycle and fixed bridge flows. The energy and cycle consistency separate over those circulations. Each independent compact connected resistance box has a continuous interval image in its scalar coordinate, so the full flow image is an affine product of intervals. This includes degenerate intervals and zero flows.

On a tree the entire flow is fixed by conservation. Each drop is its fixed signed power multiplied by beta; normalized potentials and the joint state are therefore affine images of the resistance box. This remains true if the fixed power values are irrational, since convexity does not require rational affine coefficients.

The negative statements are universal graph classifications: they need one counterexample box and nomination vector per excluded graph, not nonconvexity for every box. At p=1 both displayed curvature obstructions vanish, so the proof correctly makes no negative classification claim for that exponent. The simple-graph assumption is material to the triangle subdivision and the stated tree boundary. No arithmetic complexity or novelty conclusion is inferred from this qualitative proof.
