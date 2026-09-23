# Second independent audit of discrete flow realization and capacity existence

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-discrete-flow-realization.md) proves NP-completeness of prescribed rational flow realization with finite resistances, including the restricted single-cycle construction. Its existential unit-capacity consequence, precision gap, and interval-feasibility contrast are valid. The discrete linear-feasibility mechanism is elementary and already credited; novelty is not determined by this review.

## 1. Arbitrary-graph realization and certificates

For an explicitly specified rational target `x_bar`, conservation `A x_bar=b` is directly checkable. Every coefficient `t_e=x_bar_e|x_bar_e|` is rational with polynomial binary size. With fixed resistance choices, physical consistency is exactly the existence of potentials solving

```
A^T pi=(t_e beta_e)_e.
```

This rational linear system can be checked by spanning-forest potential integration and consistency checks on remaining edges, or by rational linear algebra. Zero target flows correctly impose zero potential difference. A reference in each connected component removes additive ambiguity. Positive resistances ensure that a conserved target satisfying these equations is the physical flow, rather than merely a formal alternative state.

A certificate consists of one input option index per edge. Because the lists are explicit, its total encoding length is polynomial. No algebraic state witness is needed: the target and resulting edge drops are rational. This proves NP membership even when the graph's cycle rank grows.

For continuous intervals, both the potentials and resistances are continuous variables and the same equations, together with resistance bounds, form rational linear feasibility. Products with `t_e` are multiplication by fixed rational data. Thus arbitrary-graph interval realization is polynomial-time solvable. This claim concerns a fixed target flow, not a flow vector being optimized together with the resistances.

## 2. Exact single-cycle encoding

For `n>=2`, a directed path of `n` edges from source to sink and a direct arc between those endpoints form a simple cycle with an acyclic orientation. The graph has `n+1` vertices and edges and maximum degree two. The two source-to-sink routes are distinct, so prescribing one on every edge gives source injection two, sink withdrawal minus two, and zero internal nominations.

The long path's drop is `n+selected_sum` at that target; the direct drop is `D=n+K`. Equality of these drops is the only independent cycle constraint. Consequently the target is physical exactly when the selected integers sum to `K`. All edge resistances are positive integers with polynomial binary length, and each uncertain edge has exactly two options.

Positive source instances with `n<2` and the usual trivial thresholds can be decided during preprocessing. The stated fixed triangle outputs are valid: long-edge options `{1,2}` on both edges produce total three, matching direct resistance three. Options `{1,3}` on both long edges produce only totals two, four, and six, so direct resistance three cannot match. Both outputs preserve the all-one target and nominations `(2,-2)`.

This establishes the claimed restricted NP-hardness; the arbitrary-graph certificate gives NP-completeness.

## 3. Unit capacity existence and its membership scope

Let the physical route flows be `p` and `z`. Conservation gives `p+z=2`. Both are strictly positive: they have the same signed terminal drop under strictly increasing passive path laws, so they have the same sign, and their sum is positive. Every long-path arc carries `p` because all internal nominations are zero.

If all arc upper capacities are one, then `p<=1`, `z<=1`, and `p+z=2` force `p=z=1`. Conversely, that target satisfies every capacity. Absolute capacity constraints yield the same equivalence because all physical flows are positive on this construction. Thus a capacity-feasible resistance choice exists exactly when the target is realizable.

For the broader fixed-nomination single-cycle class, membership is also valid. After guessing finite resistance options, bridge flows are rational cut sums and cycle flows are `q+d_e` after consistent orientation. The unique scalar cycle root is obtained from a strictly increasing piecewise rational quadratic equation. Its exact degree-at-most-two representation permits polynomial-time comparison of every resulting flow with rational upper or absolute capacities. Breakpoint roots, repeated breakpoints, and zero flows do not invalidate this computation. This verifies the guessed design in polynomial time. The claim is confined to one global cycle; the candidate correctly avoids general-rank capacity-design membership.

Robust capacity validation has a different quantifier: it asks whether every resistance scenario satisfies each arc bound. The reviewed single-arc extremum method evaluates those worst-case bounds in polynomial time on the single-cycle class. It is consistent for universal validation to be tractable while the existence of a scenario satisfying all capacities is NP-complete.

## 4. Exact deviation formula and precision

Equality of the positive terminal drops is `theta p^2=D z^2`, with `z=2-p`. Hence

```
p=2sqrt(D)/(sqrt(theta)+sqrt(D)),
|p-1|=|sqrt(D)-sqrt(theta)|/(sqrt(D)+sqrt(theta))
     =|D-theta|/(sqrt(D)+sqrt(theta))^2.
```

These identities have the correct numerator and denominator. In a no instance, `D` and `theta` are unequal integers, so the numerator is at least one. With `M=n+S+K`, both positive values are at most `M`; the denominator is at most `4M`. Therefore `|p-1|>=1/(4M)` for every resistance choice in a no instance.

The maximum arc load is exactly `max(p,2-p)=1+|p-1|`. The maximum deviation from the all-one target is exactly `|p-1|`. Thus the stated yes values and no gaps are correct for both minimization objectives. An additive estimate at tolerance, for example, `1/(16M)` distinguishes the cases. Its accuracy parameter has polynomial binary length because `log M` does. Polynomial dependence on accuracy bits would therefore imply a polynomial Subset-Sum algorithm.

The objectives are convex functions of the flow vector, but their feasible finite scenario set is generally nonconvex. This creates no contradiction with endpoint results for convex maximization over the convexified flow region. The precision gap is allowed to be small in the binary input length; the candidate does not claim strong hardness or a fixed-error barrier under the stated normalization.

## 5. Why the interval relaxation answers a different question

The independent intervals `[1,1+a_i]` give every total long-path resistance in `[n,n+S]`. For a nontrivial target with `0<=K<=S`, `D=n+K` belongs to this interval, so an interval-resistance target realization always exists. In a no Subset-Sum instance, the all-one target is therefore in the interval attainable flow region but in no original finite scenario.

It is also in the finite scenario convex hull. One can see this directly without invoking the broader cactus theorem: choosing all lower or all upper path resistances gives scalar route flows on opposite sides of one, or at one at an endpoint. The conserved two-route flow vector is affine in `p`, so their convex hull contains the all-one target. This verifies the asserted relaxation discrepancy even in the smallest relevant topology.

Containment of a finite flow set in a convex capacity set is equivalent to containment of its convex hull. Existence of an intersection with that set is not preserved by convexification. The candidate distinguishes these two statements correctly and appropriately restricts the earlier polynomial membership claim to the interval region or finite-scenario convex hull.
