# Independent audit: exact basic P-split relaxation of two balls

Date: 2026-09-04. Reviewer: `review_common_factor`.

**Verdict: the projected relaxation and exact Hausdorff-distance formula pass this independent mathematical audit.** Reviewed draft: [two translated balls](common-factor-p-split-balls.md). The result concerns the stated basic construction with tight global interval bounds over the common box, natural coordinate functions, and shared identical transverse auxiliaries. It does not cover arbitrary additional valid linking constraints or reformulations of those functions.

## Source and formulation scope

I checked Section 3, equations (2), (4), and (5), and Remark 1 in the [local published P-split paper](../literature/papers/kronqvist2026-p-split-formulations-a-class/original.pdf), local PDF pages 5–6. The source introduces epigraph links, bounds their component functions over `X`, moves the nonlinear links outside the disjunction, and convexifies the remaining auxiliary disjunction. Remark 1 and Assumption 3 require the minimal sharing convention for identical component functions. The same pages explicitly distinguish global bounds over `X` from possible stronger disjunct-specific bounds.

Here `t²` and `(t−d)²` are distinct components; every `w_i²` is identical across the two disjuncts and must be shared. Their tight global intervals are `[0,U]`, `[0,U]`, and `[0,r²]`, respectively, with `U=(d+r)²`. The common box contains both complete balls and is exactly their coordinate bounding box. Thus the draft's auxiliary model matches this source construction.

## Auxiliary hull and projection

Every point of either auxiliary disjunct satisfies the proposed inequalities. Conversely, fix `c≥0` with `Σc≤r²` and set `h=r²−Σc`. Since `0≤h≤r²<U`, the fixed-`c` union is the union of a horizontal and a vertical rectangle in `[0,U]²`. Its convex hull is exactly

```
0≤a,b≤U,  a+b≤U+h.
```

All vertices of this truncated square lie in one of the rectangles, including at `h=0`. Taking convex combinations at the same fixed `c` proves sufficiency in the full auxiliary space. The implied bound `c_i≤r²` recovers every original transverse interval bound.

The auxiliary hull is downward closed within the nonnegative orthant. Therefore an epigraph-feasible auxiliary vector can be decreased componentwise to `(t²,(t−d)²,w_1²,…,w_{n−1}²)`. This proves exact projection by substitution. The two surviving nonlinear inequalities reduce algebraically to

```
||w||≤r,
2(t−d/2)²+||w||²≤2(d/2+r)².
```

The second inequality implies `−r≤t≤d+r`, and the first implies the transverse box bounds. No original domain constraint was lost.

For the two-group partition, the transverse auxiliary starts with upper bound `(n−1)r²`; nonnegativity and either disjunct immediately strengthen it to `r²`. The same fixed-slice proof applies, giving the same projection. The assumption `n≥2` is material to the positive-loss statement; with one coordinate there is no nonzero transverse slice.

Every coarser basic coordinate partition contains this relaxation. Independently of the source's hierarchy theorem, aggregate the full-split auxiliaries over each coarse group. This affine aggregation maps each full-split auxiliary disjunct into the corresponding coarse one, preserves the summed epigraph links, and respects the additive global bounds. It therefore maps their convex hulls as well. Groups not containing `t` inherit the required shared auxiliary. This directly verifies the containment claim for this family.

## Distance to the true hull

The convex hull of equal-radius translated balls is the Minkowski sum of their center segment and the radius-`r` ball. Between the centers the relaxation's entire cylinder is inside this capsule. Reflection about `t=d/2` reduces the outer-region calculation to `t≤0`.

At fixed transverse norm `ρ`, the most distant feasible point from the first center has `t=−e(ρ)`, with

```
e(ρ)=sqrt((d/2+r)²−ρ²/2)−d/2>0.
```

The nearest point on the center segment is its first endpoint. At this outer boundary the distance to the capsule is `sqrt(e(ρ)²+ρ²)−r`. This expression is nonnegative: at `ρ=0` its radial norm is `r`, and the squared radial norm has strictly positive derivative in `u=ρ²`, namely

```
1/2+d/(4sqrt((d/2+r)²−u/2)).
```

Thus its maximum occurs at `ρ=r`, proving exactly the claimed distance `sqrt(r²+e²)−r`. The capsule is contained in the relaxation, so this directed distance also equals their ordinary Hausdorff distance. The point attaining it exists in every dimension `n≥2`.

Dividing the expression for `e` by `r`, or rationalizing its numerator, gives `e/r→1` as `d/r→∞`; the limiting relative loss is therefore `sqrt(2)−1`. The derivation is independent of dimension. It demonstrates a strict loss for every `d>2r` in this basic construction and does not restore the published universal nonexactness claim refuted by the separate truncated-domain example.

## Review limits

No mathematical correction was needed. I recommended making the phrase “tight global interval bounds over X” explicit to distinguish the scope from stronger local bounds. The auxiliary-hull calculation and geometric maximization are elementary and self-contained; their novelty remains unestablished. This audit does not claim that all strengthened P-split formulations have the same loss.
