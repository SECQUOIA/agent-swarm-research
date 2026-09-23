# Second independent audit of continuous cactus convex design

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-cactus-convex-design.md) gives a polynomial-bit additive algorithm returning rational resistance choices for a rational convex quadratic flow objective, at arbitrary cactus rank. The surrogate interval construction, convex optimization oracle, exact resistance interpolation, and error budget are sound. Finite resistance choices and extra exact operating constraints remain excluded.

## 1. Flow coordinates and objective bounds

The inherited attainable region is `x=x0+Zq`, with independent quadratic-algebraic intervals for cycle circulations. Cycle columns have disjoint edge supports and entries of magnitude one. Bridge flows are fixed. Thus a circulation-coordinate error affects only its own cycle edges and introduces no sum of different coordinate errors on one edge.

For the fixed balanced nomination, every passive physical flow is bounded by total positive injection and hence by `B=sum_v |b_v|`. With `Q` symmetric positive semidefinite, the gradient is `Qx+d`. On `[-B-1,B+1]^m`, its infinity norm is bounded by the displayed rational `L`. Integrating the gradient along a segment in this box proves `|f(x)-f(y)|<=L||x-y||_1`. This applies whether or not either point is physically attainable.

The edgeless and zero-nomination cases are immediate. A tree with nonzero nominations has no free cycle coordinates, but its physical flow is rational and the zero-dimensional procedure still works.

## 2. Retained intervals and freezing

If `l^+<=u^-`, the retained interval lies inside the true interval. Projection of a true feasible scalar into it moves the scalar by at most `eta`: its two potentially excluded endpoint strips have widths at most the respective enclosure widths.

If `l^+>u^-`, then

```
u-l=(u-u^-)+(u^--l^+)+(l^+-l)<2eta.
```

The frozen scalar is `l^+`, whose distance from the actual lower endpoint is at most `eta`. Every true interval point is within the claimed `2eta` of it. The claim is conservative; the crossing-enclosure condition even gives an `eta` bound, but that improvement is not needed.

An optimal true flow can therefore be mapped to the surrogate box with total flow error at most `2m eta`. Conversely, every surrogate vector is within at most `eta` on each frozen-cycle edge of a true attainable flow: retain its retained coordinates and replace each frozen coordinate by the true lower endpoint. Block independence makes that nearby flow jointly attainable. Hence all surrogate flows lie in the expanded box `[-B-1,B+1]^m` because `eta<=1`.

The Lipschitz estimate applies to both these comparisons. It follows that the surrogate optimum is at most the true optimum plus `2mL eta`. The surrogate need not be a subset of the attainable region; its controlled distance and later recovery are exactly what the proof uses. In particular, an irrational singleton cycle interval is handled by freezing and does not require a rational physically attainable target circulation.

## 3. Polynomial-bit convex optimization

After discarding fixed coordinates, transform the remaining rational intervals affinely to a cube. The resulting function is a rational positive-semidefinite quadratic plus a rational affine term. All coefficients have polynomial bit length: interval enclosures have the requested precision, and only rational affine substitution is used. Very short intervals cause no condition-number requirement for this existence/bit algorithm.

A rational positive-semidefinite matrix admits a rational LDL decomposition with nonnegative diagonal entries and polynomial-bit factors. Zero pivots can be skipped: in a positive-semidefinite Schur complement, a zero diagonal entry has a zero row and column. Alternatively use a rational symmetric permutation. No square roots or common algebraic field are needed. Consequently the quadratic part can be written as a sum of nonnegative rational multiples of squares of rational linear forms.

For each form `a^T t`, take a rational `R` at least its maximum absolute value on the cube, for example `1+||a||_1`. Replace the scalar square by

```
psi_R(s)=s^2                      if |s|<=R,
         2R|s|-R^2                otherwise.
```

This function is convex, agrees with the square on the required interval, and is globally `2R`-Lipschitz. Composing with the linear form and summing with nonnegative weights preserves convexity. Adding the affine objective term also preserves global Lipschitz continuity. A valid rational Euclidean Lipschitz upper bound is obtained using `||a||_2<=||a||_1`, summing the resulting weighted `2R||a||_1` bounds and the affine gradient bound. Its magnitude may be large, but its binary encoding length is polynomial.

Exact evaluation and subgradient calculation at rational query points use only polynomially many rational operations and comparisons with polynomially bounded output encoding. The function agrees with the original transformed objective everywhere on the cube. The cube has a rational center, unit inner radius, a rational outer-radius bound, and an exact membership oracle. Thus all hypotheses of the cited convex optimization result are met.

I directly reread Dadush's Theorem 2.5.9, printed page 48, and the preceding encoding convention. It provides a rational point **in** the convex body and an additive objective guarantee for a globally Lipschitz convex function with rational approximate evaluation oracle. The preceding discussion makes polynomial dependence refer to the lengths of the input guarantees. These are precisely the properties required here. [Primary thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf).

This supplies the rational `epsilon/2`-optimal surrogate point in polynomial bit time without fixing the number of cycles. If no variable remains, direct evaluation replaces this step.

## 4. Exact resistance interpolation

At a retained rational circulation, all cycle flows are rational. Let `a=H_min(q)<=0` and `b=H_max(q)>=0`, and let `beta_min,beta_max` be profiles attaining those values termwise. When `b-a>0`,

```
lambda=-a/(b-a) in [0,1],
beta=(1-lambda)beta_min+lambda beta_max
```

lies in the input resistance box and satisfies cycle consistency exactly, since the fixed-flow cycle equation is linear in beta and `a+lambda(b-a)=0`. The sign and direction of interpolation in the candidate are correct. If the difference is zero, both values are zero and either profile suffices. Zero edge flows allow either endpoint and introduce no division by a flow.

All terms, lambda, and recovered resistances are rational with polynomial bit size. A very small nonzero denominator does not cause an encoding problem: it is already the difference of polynomial-bit rational numbers. Each frozen coordinate instead uses its stored rational endpoint profile, whose physical circulation is the exact algebraic lower endpoint. Independent cycle consistency plus conservation guarantees a globally physical state; bridge resistances are arbitrary permitted endpoints.

Only frozen-cycle flows differ from the surrogate. Their coordinate error is at most `eta`, so recovery adds at most `mL eta` to the objective. This also explains why rational resistance output does not require every returned physical flow to be rational.

## 5. Total guarantee and limitations

Combining projection, surrogate optimization, and physical recovery gives

```
f(returned physical flow)-true optimum
 <=2mL eta+epsilon/2+mL eta
 <=3epsilon/16+epsilon/2=11epsilon/16<epsilon.
```

The bound holds in both branches of `eta=min(1,epsilon/(16mL))`. Every point compared lies in the expanded box on which the same L is valid.

The returned objective can be approximated by enclosing each separate quadratic cycle root, constructing rational approximations to all flow coordinates, and evaluating the rational quadratic. The gradient bound controls this error, including cross-cycle terms in Q. This needs no exact sum or common algebraic field across cycles and makes no exact scalar threshold claim.

Continuous intervals are essential to the interpolation step. It generally produces resistances absent from an original finite set, so this proof cannot support the finite-resistance design problem. Extra exact operating constraints could be violated by the rational surrogate or by the small recovery displacement; they are expressly outside the theorem. Within the stated unconstrained passive scenario set and additive objective guarantee, no correction is required.
