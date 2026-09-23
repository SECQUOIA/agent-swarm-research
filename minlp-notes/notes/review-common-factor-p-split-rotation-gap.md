# Independent audit: unbounded coordinate dependence of basic P-split

Date: 2026-09-04. Reviewer: `review_common_factor`.

**Verdict: the two-dimensional orthogonal-coordinate comparison, its arbitrary auxiliary-only strengthening obstruction, and aligned exactness all pass the mathematical audit.** Reviewed draft: [P-split coordinate effect](common-factor-p-split-rotation-gap.md). The original comparison uses the precisely specified basic constructions; the subsequently audited Sections 5–6 establish the broader fixed-epigraph-map conclusions below. Publication novelty remains unestablished.

## Original coordinates

For centers `(0,0)` and `(D,D)`, the four squared-coordinate functions are distinct. Their tight global upper bound on `[-1,D+1]²` is `U=(D+1)²`. At `p=(2D/3,D/3)`, the draft's auxiliary vectors equal the actual squares and satisfy `2a_i,2b_i≤8D²/9≤U`.

The lifted vector is exactly the average of two auxiliary-disjunction points: `(0,2b)` in the first disjunct and `(2a,0)` in the second. The nonlinear epigraph links are imposed on the average, not separately on these disaggregated auxiliary points. This is precisely why the construction is feasible in the basic relaxation. It respects the source's sharing convention because no identical coordinate function is duplicated here.

The point projects orthogonally to `(D/2,D/2)` on the center segment, giving distance `D/(3sqrt(2))` to the segment and `D/(3sqrt(2))−1` to the capsule. The latter is positive for the stipulated `D≥5`. Since the basic relaxation is convex and contains both balls, it contains their hull; its directed outer distance is therefore its Hausdorff distance. Direct aggregation of auxiliaries also verifies the lower bound for the original one-group partition.

## Orthogonal coordinates and the unchanged domain

The stated map is orthogonal, so it preserves Euclidean distances and the full feasible geometry. Its determinant is minus one; “orthogonal coordinate change” is the literal description, while reversing the sign of `w` makes it a proper rotation without changing any calculation.

The retained domain becomes exactly the displayed diamond. Replacing that diamond by its coordinate bounding rectangle would change the proof, and the draft does not do so. The transformed quadratics share the same `w²` term. Consequently a single nonnegative auxiliary `c` appears in both auxiliary disjuncts, and each disjunct forces `c≤1`. Convexification preserves this inequality, giving `|w|≤1` in the projected relaxation. The tight global squared-coordinate bounds stated in the draft are correct, but the distance upper bound needs only this shared transverse restriction and the retained diamond.

Between the centers, every point in the resulting strip lies in the true capsule. For `t≤0`, the diamond gives `−t+|w|≤sqrt(2)`. Setting `ρ=|w|≤1`, the squared distance from the left center is at most

```
(sqrt(2)−ρ)²+ρ² ≤ 2.
```

The last inequality follows by maximizing the convex quadratic on `[0,1]`; its endpoint values are `2` and `4−2sqrt(2)`. Distance to the unit ball is therefore at most `sqrt(2)−1`; points already inside it have distance zero. The upper diamond faces yield the identical argument beyond the right center. This proves the uniform Hausdorff upper bound.

The diamond is not a box, so the source's additive-bound partition hierarchy cannot simply be imported after transformation. The draft explicitly avoids that claim. Its comparison uses the designated two-coordinate construction on both sides, which is sufficient.

## Rational-data strengthening checked independently

The same effect does not require algebraic input data. Take centers `(0,0)` and `(3D,4D)`, retained box `[-1,3D+1]×[-1,4D+1]`, and point `p=(2D,4D/3)`, for rational `D≥2`. Use the rational orthogonal map

```
t=(3x_1+4x_2)/5,
w=(4x_1−3x_2)/5.
```

For each original coordinate, both its value at `p` and its difference from the corresponding center coordinate have magnitude at most two thirds of that center coordinate. The same half-weight auxiliary lift is therefore feasible, because `2(2c_i/3)²≤(c_i+1)²`. The transformed center is `(5D,0)`, while `t(p)=34D/15` lies between the centers and `|w(p)|=4D/5`. The original Hausdorff error is at least `4D/5−1`.

After transformation, required sharing again forces `|w|≤1`. For `t≤0`, the inverse map gives `x_1=(3t+4w)/5≤4/5` and `x_2=(4t−3w)/5≤3/5`; the retained domain gives `x_i≥−1`. Hence both original coordinates lie in `[-1,1]`, and the distance to the first center is at most `sqrt(2)`. Beyond the second center, subtract `(3D,4D)` and use the upper box faces to obtain the same bound. Between centers the strip is contained in the capsule. Thus the transformed Hausdorff error is again at most `sqrt(2)−1`, using rational centers, bounds, and coordinate coefficients.

This variant was derived independently during the audit, incorporated by the author as Section 4, and then checked against that written section. Reversing the transverse sign gives a proper rational rotation if desired.

## Scope of the conclusion

The comparison establishes an unbounded absolute improvement as center separation increases, even with two variables and two unit balls. The retained domain changes only by the same orthogonal map as the disjuncts. The later Sections 5–6, reviewed below, show that the lower bound also survives valid auxiliary-only links and disjunct-specific auxiliary bounds. Constraints coupling original and auxiliary variables, changed function maps, equality identities replacing epigraph links, and the full perspective hull remain outside this obstruction. The common-function sharing is an essential part of the mechanism, not an omitted modeling detail.

No correction to the displayed inequalities was needed. The source conventions had also been checked directly in the [earlier two-ball audit](review-common-factor-p-split-balls.md). The witnesses and bounds here are symbolic and do not depend on numerical optimization.

## Final audit of Sections 5–6: strongest auxiliary convexification

This addendum was completed after the instruction to finish current work and stop. Both new sections were checked against their written proofs; no new research direction was started.

### Obstruction under every valid auxiliary-only strengthening

For `F(x)=(x_i²,(x_i−v_i)²)_i`, the half-average of the two genuine center images is `(v_i²/2,v_i²/2)_i`. Any convex auxiliary set containing those images must contain this average. At either witness, the actual squared components are at most `4v_i²/9`, strictly below the average. Thus the same witness satisfies the coordinate epigraph links with this auxiliary value.

This argument is stronger than the earlier inactive-copy construction: both mixed auxiliary points now come from genuine feasible original points. Therefore it survives every auxiliary-only restriction valid for the original function images, including exact convexification of those images, valid auxiliary linking inequalities, and valid disjunct-specific bounds. If a convex set merely contains the two center images, the witness conclusion still holds, even if that set does not preserve the rest of the disjuncts. For an actual valid relaxation, preservation of all feasible images supplies the additional inclusion of the true hull.

The stated exclusions are necessary. The proof keeps the coupling exactly `F(x)≤α`. An identity involving `x` and `α`, an original-space cut, or a different lift can remove the witness, and is not an auxiliary-only modification in this sense.

### Exactness after aligning the center segment

For the aligned lift `F'(t,w)=(t²,(t−d)²,w²)`, every actual image has `0≤c≤1`. At fixed `c`, the feasible longitudinal values lie in the two intervals with half-width `sqrt(1−c)`. Thus both squared longitudinal components are bounded above by

```
f(c)=(d+sqrt(1−c))²=d²+1−c+2d sqrt(1−c).
```

This function is concave, continuous on `[0,1]`, and decreasing. Its two hypographs are convex and contain all actual images, so their inequalities remain valid on the full convex image hull. Endpoint `c=1` is covered by continuity and presents no exceptional case.

With the epigraph links, `w²≤c` and monotonicity give

```
t²≤f(w²),  (t−d)²≤f(w²),  |w|≤1.
```

Taking square roots and intersecting the resulting longitudinal intervals gives exactly `−sqrt(1−w²)≤t≤d+sqrt(1−w²)`. This is the capsule. Conversely, the epigraph relaxation is convex and contains both complete balls, so it contains their capsule. The retained transformed domain also contains the capsule, since it is convex and contains both balls. Hence it does not interfere with the equality.

The two hypograph inequalities alone, with the epigraph links and `0≤c≤1`, already suffice. Their proposed conic representation is exact: existence of `s≥0` with `s²+c≤1` and `a+c−d²−1≤2ds` is equivalent to `a≤f(c)`, since the largest allowed `s` is `sqrt(1−c)` and `d>0`. The same reasoning applies to `b`. A common `s` may be used for both, or separate copies, because the largest admissible value satisfies both whenever the hypograph inequalities hold.

Therefore the strongest convexification restricted to the original coordinate function space can have unbounded error, while the strongest convexification after the fixed rational orthogonal change is exact. The variable transformation changes the functions and their sharing, while preserving the form of their epigraph links and the complete feasible geometry. This conclusion is mathematically verified; priority remains unchecked beyond the author's bounded literature search.

**Final status:** all assigned claims in the current draft pass. Audit complete; no further work undertaken after this record.
